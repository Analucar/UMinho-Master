package eu.europa.esig.dss.web.model;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

public class SignupForm {
    @NotNull
    @Pattern(regexp = "\\w+@[a-zA-Z_]+?.[a-zA-Z]{2,3}", message = "{error.email.wrongInput}")
    private String email;

    @NotNull
    @Pattern(regexp = "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#&()–[{}]:;',?/*~$^+=<>]).{12,128}", message = "{error.password.wrongInput}")
    private String password;

    public String getPassword() {
        return this.password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
