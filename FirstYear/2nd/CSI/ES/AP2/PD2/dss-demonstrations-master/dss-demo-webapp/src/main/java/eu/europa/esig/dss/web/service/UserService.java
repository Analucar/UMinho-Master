package eu.europa.esig.dss.web.service;
import eu.europa.esig.dss.web.repository.UserRepository;
import eu.europa.esig.dss.web.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.sql.SQLException;
import java.util.ArrayList;

@Component
public class UserService implements UserDetailsService {

    @Autowired
    private UserRepository repo;

    private final Logger LOG = LoggerFactory.getLogger(UserService.class);

    public void addUser(User u) throws NoSuchAlgorithmException, InvalidKeySpecException {

        BCryptPasswordEncoder pw = new BCryptPasswordEncoder();
        u.setPassword(pw.encode(u.getPassword()));
        repo.save(u);
    }

    public void updateUser(User u) throws SQLException {
        this.repo.save(u);
    }

    public User getUser(Long id) throws SQLException {
        return this.repo.findById(id).orElse(null);
    }

    public User getUser(String email) {
        return this.repo.findByEmail(email).orElse(null);
    }

    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {

        User user = this.getUser(email);

        if (user == null) {
            throw new UsernameNotFoundException("No user found with email: " + email);
        }

        ArrayList<GrantedAuthority> roles = new ArrayList<>();
        roles.add(new SimpleGrantedAuthority("USER"));

        return new org.springframework.security.core.userdetails.User(user.getEmail(), user.getPassword(), true, true, true, true, roles);
    }
}
