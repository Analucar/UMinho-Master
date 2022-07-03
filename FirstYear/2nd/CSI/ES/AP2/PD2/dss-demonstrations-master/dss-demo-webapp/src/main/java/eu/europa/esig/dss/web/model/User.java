package eu.europa.esig.dss.web.model;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

@Entity
@Table(name = "USERS")
public class User {
    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private long id;
    @NotNull
    private String email;

    @NotNull
    private String password;

    private String phone;
    public User() {
        this.email = null;
        this.password = null;
        this.phone = null;
    }

    public User(String em, String pw, String ph) {
        this.email = em;
        this.password = pw;
        this.phone = ph;
    }

    public User(Long id, String em, String pw, String ph) {
        this.id = id;
        this.email = em;
        this.password = pw;
        this.phone = ph;
    }
    public String getPassword() {
        return this.password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getPhone() {
        return this.phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public long getId(){ return this.id; }

    public void setId(long id) { this.id = id; }

    @Override
    public String toString() {
        return "USER - " + email + " | " + password + " | " + id;
    }
}
