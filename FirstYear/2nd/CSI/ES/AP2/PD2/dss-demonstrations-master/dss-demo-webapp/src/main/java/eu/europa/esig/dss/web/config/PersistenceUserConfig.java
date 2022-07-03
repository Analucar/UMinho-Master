package eu.europa.esig.dss.web.config;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.env.Environment;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;

import javax.sql.DataSource;
import java.util.HashMap;


@Configuration
@EnableJpaRepositories(
        basePackages = "eu.europa.esig.dss.web.repository",
        entityManagerFactoryRef = "userEntityManager",
        transactionManagerRef = "userTransactionManager"
)

public class PersistenceUserConfig {
    @Autowired
    private Environment env;

    @Value("${datasource.users.driver}")
    private String dataSourceDriverUsers;

    @Value("${datasource.users.username}")
    private String usernameUsers;

    @Value("${datasource.users.password}")
    private String passwordUsers;

    @Value("${datasource.users.url}")
    private String dataSourceUrlUsers;

    @Bean
    public LocalContainerEntityManagerFactoryBean userEntityManager() {
        LocalContainerEntityManagerFactoryBean entityMan
                = new LocalContainerEntityManagerFactoryBean();

        entityMan.setDataSource(dataSourceDB());
        entityMan.setPackagesToScan("eu.europa.esig.dss.web.model");

        HibernateJpaVendorAdapter vendorAdapter
                = new HibernateJpaVendorAdapter();
        entityMan.setJpaVendorAdapter(vendorAdapter);

        HashMap<String, Object> properties = new HashMap<>();
        properties.put("hibernate.hbm2ddl.auto", "update");
        properties.put("hibernate.dialect", "org.hibernate.dialect.PostgreSQLDialect");

        entityMan.setJpaPropertyMap(properties);

        return entityMan;
    }

    @Bean(name = "dataSourceDB")
    public DataSource dataSourceDB(){
        DriverManagerDataSource ds = new DriverManagerDataSource();
        ds.setDriverClassName(dataSourceDriverUsers);
        ds.setUrl(dataSourceUrlUsers);
        ds.setUsername(usernameUsers);
        ds.setPassword(passwordUsers);

        return ds;
    }

    @Bean
    public PlatformTransactionManager userTransactionManager() {
        JpaTransactionManager transactionManager = new JpaTransactionManager();
        transactionManager.setEntityManagerFactory(userEntityManager().getObject());

        return transactionManager;
    }
}
