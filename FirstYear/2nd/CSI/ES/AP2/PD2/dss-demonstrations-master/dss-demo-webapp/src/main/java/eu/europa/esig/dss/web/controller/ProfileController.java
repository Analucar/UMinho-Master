package eu.europa.esig.dss.web.controller;

import eu.europa.esig.dss.web.model.PhoneForm;
import eu.europa.esig.dss.web.model.User;
import eu.europa.esig.dss.web.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import java.sql.SQLException;
import java.util.List;

@Controller
public class ProfileController {
    private final Logger LOG = LoggerFactory.getLogger(ProfileController.class);
    @Autowired
    private UserService service;

    @RequestMapping(value = { "/profile" }, method = RequestMethod.GET)
    public String showProfile(Model model, HttpServletRequest response) throws SQLException {

        PhoneForm phoneForm = new PhoneForm();

        model.addAttribute("phoneForm", phoneForm);

        return "profile";
    }

    @RequestMapping(value = { "/profile" }, method = RequestMethod.POST)
    public String saveProfile(Model model, HttpServletRequest response,
                              @ModelAttribute("phoneForm") @Valid PhoneForm phoneForm, BindingResult result) throws SQLException {

        if (result.hasErrors()) {
            if (LOG.isDebugEnabled()) {
                List<ObjectError> allErrors = result.getAllErrors();
                for (ObjectError error : allErrors) {
                    LOG.info(error.getDefaultMessage());
                }
            }
            return "profile";
        }

        UserDetails u = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = service.getUser(u.getUsername());

        String userPhone = user.getPhone();
        String formPhone = phoneForm.getPhone();

        if(userPhone == null || !userPhone.equals(formPhone)){

            LOG.info("Update de user");
            user.setPhone(formPhone);
            this.service.updateUser(user);
        }

        return "home";
    }
}
