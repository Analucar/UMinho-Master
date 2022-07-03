package eu.europa.esig.dss.web.controller;

import eu.europa.esig.dss.web.model.SignupForm;
import eu.europa.esig.dss.web.model.User;
import eu.europa.esig.dss.web.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.sql.SQLException;
import java.util.List;


@Controller
public class SignupController {

    private final Logger LOG = LoggerFactory.getLogger(SignupController.class);
    @Autowired
    private UserService service;

    //@Autowired
    //AuthenticationManager authManager;

    @RequestMapping(value = { "/signup" }, method = RequestMethod.GET)
    public String showSignup(Model model, HttpServletRequest response) {

        model.addAttribute("signupForm", new SignupForm());

        return "signup";
    }

    @RequestMapping(value = { "/signup" }, method = RequestMethod.POST)
    public String saveSignup(Model model, HttpServletRequest response,
                             @ModelAttribute("signupForm") @Valid SignupForm userForm, BindingResult result) {

        if (result.hasErrors()) {
            if (LOG.isDebugEnabled()) {
                List<ObjectError> allErrors = result.getAllErrors();

                for (ObjectError error : allErrors) {
                    LOG.info(error.getDefaultMessage());
                }
            }
            return "signup";
        }

        try {

            if (this.service.getUser(userForm.getEmail()) == null) {
                User user = new User();
                user.setPassword(userForm.getPassword());
                user.setEmail(userForm.getEmail());
                this.service.addUser(user);
            }
            else
                return "signup";
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            return "signup";
        }

        return "login";

    }

}
