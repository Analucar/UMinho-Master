package eu.europa.esig.dss.web.model;

import eu.europa.esig.dss.web.validation.Base64;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

public class SignatureDigestForm extends AbstractSignatureForm {

	@NotNull(message = "{error.document.name.mandatory}")
	private String documentName;

	@Base64
	@NotEmpty(message = "{error.to.sign.digest.mandatory}")
	private String digestToSign;
	
	public String getDocumentName() {
		return documentName;
	}

	public void setDocumentName(String documentName) {
		this.documentName = documentName;
	}

	public String getDigestToSign() {
		return digestToSign;
	}

	public void setDigestToSign(String digestToSign) {
		this.digestToSign = digestToSign;
	}
	
}
