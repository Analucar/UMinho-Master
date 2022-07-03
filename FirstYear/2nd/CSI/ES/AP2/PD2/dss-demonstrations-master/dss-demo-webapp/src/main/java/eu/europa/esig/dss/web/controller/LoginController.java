package eu.europa.esig.dss.web.controller;

import eu.europa.esig.dss.web.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
@Controller
public class LoginController {
    private final Logger LOG = LoggerFactory.getLogger(LoginController.class);
    @Autowired
    private UserService service;

    @RequestMapping(value = {"/login"})
    public String showLogin(Model model) {
        Authentication a = SecurityContextHolder.getContext().getAuthentication();
        if (a == null || a instanceof AnonymousAuthenticationToken) {
            return "login";
        }
        return "redirect:home";
    }
}

