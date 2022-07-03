package eu.europa.esig.dss.web.controller;
import eu.europa.esig.dss.enumerations.*;
import eu.europa.esig.dss.model.DSSDocument;
import eu.europa.esig.dss.model.InMemoryDocument;
import eu.europa.esig.dss.model.MimeType;
import eu.europa.esig.dss.model.ToBeSigned;
import eu.europa.esig.dss.spi.DSSUtils;
import eu.europa.esig.dss.utils.Utils;
import eu.europa.esig.dss.web.WebAppUtils;
import eu.europa.esig.dss.web.editor.ASiCContainerTypePropertyEditor;
import eu.europa.esig.dss.web.editor.EnumPropertyEditor;
import eu.europa.esig.dss.web.model.CMDOTPForm;
import eu.europa.esig.dss.web.model.Encoding;
import eu.europa.esig.dss.web.model.PrivKeySignatureDocumentForm;
import eu.europa.esig.dss.web.service.PrivKeyService;
import eu.europa.esig.dss.web.service.SigningService;
import jdk.internal.net.http.common.Log;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.springframework.web.multipart.MultipartFile;

import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;
import javax.xml.ws.soap.SOAPFaultException;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.Charset;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.Security;
import java.security.SignatureException;
import java.security.cert.CertificateException;
import java.security.spec.InvalidKeySpecException;
import java.util.Base64;
import java.util.Date;
import java.util.List;

@Controller
@SessionAttributes(value = { "signatureDocumentForm", "signedDocument" })
@RequestMapping(value = "/privKey-sign-a-document")
public class PrivKeySignatureController {
    private static final Logger LOG = LoggerFactory.getLogger(PrivKeySignatureController.class);
    private static final String SIGNATURE_START = "privKey-signature";
    private static final String SIGNATURE_SIGNED = "privKey-signature-signed";

    private static final String[] ALLOWED_FIELDS = { "documentToSign", "privateKey", "certificate", "containerType", "signatureForm", "signaturePackaging",
            "signatureLevel", "certificateFormat", "privateKeyFormat", "digestAlgorithm", "signWithExpiredCertificate", "addContentTimestamp" };

    @Value("${default.digest.algo}")
    private String defaultDigestAlgo;

    @Autowired
    private SigningService signingService;

    @Autowired
    private PrivKeyService privKeyService;

    @InitBinder
    public void initBinder(WebDataBinder webDataBinder) {
        webDataBinder.registerCustomEditor(SignatureForm.class, new EnumPropertyEditor(SignatureForm.class));
        webDataBinder.registerCustomEditor(ASiCContainerType.class, new ASiCContainerTypePropertyEditor());
        webDataBinder.registerCustomEditor(SignaturePackaging.class, new EnumPropertyEditor(SignaturePackaging.class));
        webDataBinder.registerCustomEditor(SignatureLevel.class, new EnumPropertyEditor(SignatureLevel.class));
        webDataBinder.registerCustomEditor(DigestAlgorithm.class, new EnumPropertyEditor(DigestAlgorithm.class));
        webDataBinder.registerCustomEditor(EncryptionAlgorithm.class, new EnumPropertyEditor(EncryptionAlgorithm.class));
    }

    @InitBinder
    public void setAllowedFields(WebDataBinder webDataBinder) {
        webDataBinder.setAllowedFields(ALLOWED_FIELDS);
    }

    @RequestMapping(method = RequestMethod.GET)
    public String showSignatureParameters(Model model, HttpServletRequest request) {
        PrivKeySignatureDocumentForm signatureDocumentForm = new PrivKeySignatureDocumentForm();

        signatureDocumentForm.setDigestAlgorithm(DigestAlgorithm.forName(defaultDigestAlgo, DigestAlgorithm.SHA256));
        signatureDocumentForm.setCertificateFormat(Encoding.PEM);
        signatureDocumentForm.setPrivateKeyFormat(Encoding.PEM);

        model.addAttribute("privKeySignatureDocumentForm", signatureDocumentForm);

        return SIGNATURE_START;
    }

    @RequestMapping(method = RequestMethod.POST)
    public String sign(Model model, HttpServletRequest response,
                                   @ModelAttribute("privKeySignatureDocumentForm") @Valid PrivKeySignatureDocumentForm signatureDocumentForm, BindingResult result) {
        if (result.hasErrors()) {
            if (LOG.isDebugEnabled()) {
                List<ObjectError> allErrors = result.getAllErrors();
                for (ObjectError error : allErrors) {
                    LOG.debug(error.getDefaultMessage());
                }
            }
            return SIGNATURE_START;
        }

        try {
            String cert = new String(signatureDocumentForm.getCertificate().getBytes(), Charset.defaultCharset());

            cert = privKeyService.parseCertificate(cert);

            signatureDocumentForm.setBase64Certificate(cert);

            String privKey = new String(signatureDocumentForm.getPrivateKey().getBytes(), Charset.defaultCharset());

            privKey = privKeyService.parsePrivateKey(privKey);

            signatureDocumentForm.setSigningDate(new Date());

            if (signatureDocumentForm.isAddContentTimestamp()) {
                signatureDocumentForm.setContentTimestamp(WebAppUtils.fromTimestampToken(signingService.getContentTimestamp(signatureDocumentForm)));
            }

            ToBeSigned dataToSign = signingService.getDataToSign(signatureDocumentForm);

            if (dataToSign == null) {
                return null;
            }

            SignatureAlgorithm certificateSignatureAlgorithm = DSSUtils.loadCertificateFromBase64EncodedString(signatureDocumentForm.getBase64Certificate()).getSignatureAlgorithm();
            signatureDocumentForm.setEncryptionAlgorithm(certificateSignatureAlgorithm.getEncryptionAlgorithm());

            model.addAttribute("signatureDocumentForm", signatureDocumentForm);
            model.addAttribute("digestAlgorithm", signatureDocumentForm.getDigestAlgorithm());
            byte [] signature = privKeyService.sign(dataToSign.getBytes(), Base64.getDecoder().decode(privKey), signatureDocumentForm.getDigestAlgorithm().toString(), signatureDocumentForm.getEncryptionAlgorithm().getName());

            if(signature != null) {
                signatureDocumentForm.setBase64SignatureValue(new String(signature));

                DSSDocument document = signingService.signDocument(signatureDocumentForm);
                InMemoryDocument signedDocument = new InMemoryDocument(DSSUtils.toByteArray(document), document.getName(), document.getMimeType());

                model.addAttribute("signedDocument", signedDocument);
                return SIGNATURE_SIGNED;
            } else
                return SIGNATURE_START;


        } catch (IOException | NoSuchPaddingException | IllegalBlockSizeException | InvalidKeySpecException |
                 NoSuchAlgorithmException | InvalidKeyException | BadPaddingException | SignatureException  e) {
            throw new RuntimeException(e);
        }
    }

    @RequestMapping(value = "signedDocument/download", method = RequestMethod.GET)
    public String downloadSignedFile(@ModelAttribute("signedDocument") InMemoryDocument signedDocument, HttpServletResponse response) {
        try {
            MimeType mimeType = signedDocument.getMimeType();
            if (mimeType != null) {
                response.setContentType(mimeType.getMimeTypeString());
            }
            response.setHeader("Content-Transfer-Encoding", "binary");
            response.setHeader("Content-Disposition", "attachment; filename=\"" + signedDocument.getName() + "\"");
            Utils.copy(new ByteArrayInputStream(signedDocument.getBytes()), response.getOutputStream());

        } catch (Exception e) {
            LOG.error("An error occurred while pushing file in response : " + e.getMessage(), e);
        }
        return null;
    }

    @ModelAttribute("asicContainerTypes")
    public ASiCContainerType[] getASiCContainerTypes() {
        return ASiCContainerType.values();
    }

    @ModelAttribute("signatureForms")
    public SignatureForm[] getSignatureForms() {
        return new SignatureForm[] { SignatureForm.XAdES, SignatureForm.CAdES, SignatureForm.PAdES, SignatureForm.JAdES};
    }

    @ModelAttribute("signaturePackagings")
    public SignaturePackaging[] getSignaturePackagings() {
        return SignaturePackaging.values();
    }

    @ModelAttribute("digestAlgos")
    public DigestAlgorithm[] getDigestAlgorithms() {
        DigestAlgorithm[] algos = new DigestAlgorithm[] { DigestAlgorithm.SHA1, DigestAlgorithm.SHA256, DigestAlgorithm.SHA384,
                DigestAlgorithm.SHA512 };
        return algos;
    }

    @ModelAttribute("isMockUsed")
    public boolean isMockUsed() {
        return signingService.isMockTSPSourceUsed();
    }

}
