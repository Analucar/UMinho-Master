package eu.europa.esig.dss.web.service;

import com.google.common.primitives.Bytes;
import eu.europa.esig.dss.enumerations.DigestAlgorithm;
import eu.europa.esig.dss.enumerations.EncryptionAlgorithm;
import org.springframework.stereotype.Component;
import wsdlservice.ObjectFactory;
import wsdlservice.SignRequest;
import wsdlservice.SignStatus;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.security.*;
import java.security.cert.Certificate;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.*;

@Component
public class PrivKeyService {

    public String parseCertificate(String cert) {
        cert = cert.replace("-----BEGIN CERTIFICATE-----", "")
                   .replaceAll(System.lineSeparator(), "")
                   .replace("-----END CERTIFICATE-----", "");

        return cert;
    }
    public String parsePrivateKey(String privKey) {
        String privateKeyPEM = privKey.replace("-----BEGIN PRIVATE KEY-----", "")
                                      .replaceAll(System.lineSeparator(), "")
                                      .replace("-----END PRIVATE KEY-----", "");
        return privateKeyPEM;
    }

    public byte[] sign(byte[] doc, byte [] privateKey, String digestAlgo, String EncAlgo) throws InvalidKeySpecException, NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException, BadPaddingException, SignatureException {
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(privateKey);
        KeyFactory kf = KeyFactory.getInstance("RSA");
        PrivateKey privKey = kf.generatePrivate(keySpec);
        Signature sgn = Signature.getInstance(digestAlgo + "with" + EncAlgo);
        sgn.initSign(privKey);
        sgn.update(doc);
        return Base64.getEncoder().encode(sgn.sign());
    }
}
