package eu.europa.esig.dss.web.model;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
public class PhoneForm {

    @Pattern(regexp = "(\\+351) *9\\d{8}", message = "{error.cmd.userId.wrongInput}")
    private String phone;

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    @Override
    public String toString() {
        return phone;
    }
}
