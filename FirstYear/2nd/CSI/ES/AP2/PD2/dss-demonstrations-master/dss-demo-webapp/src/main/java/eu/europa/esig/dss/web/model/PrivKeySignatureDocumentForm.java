package eu.europa.esig.dss.web.model;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.constraints.NotNull;

public class PrivKeySignatureDocumentForm extends SignatureDocumentForm{

    @NotNull
    private MultipartFile privateKey;
    @NotNull
    private MultipartFile certificate;

    private Encoding certificateFormat;

    private Encoding privateKeyFormat;

    public MultipartFile getPrivateKey() { return this.privateKey; }

    public void setPrivateKey(MultipartFile pKey) {
        this.privateKey = pKey;
    }

    public MultipartFile getCertificate() {
        return this.certificate;
    }

    public void setCertificate(MultipartFile cert) {
        this.certificate = cert;
    }

    public Encoding getCertificateFormat(){ return this.certificateFormat; }

    public void setCertificateFormat(Encoding certificateFormat){ this.certificateFormat = certificateFormat; }

    public Encoding getPrivateKeyFormat(){ return this.privateKeyFormat; }

    public void setPrivateKeyFormat(Encoding privateKeyFormat){ this.privateKeyFormat = privateKeyFormat; }

}
