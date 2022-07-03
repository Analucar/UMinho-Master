package eu.europa.esig.dss.web.config;

import javax.annotation.PostConstruct;
import javax.sql.DataSource;

import eu.europa.esig.dss.web.WebAppUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

@Configuration
@EnableTransactionManagement
public class PersistenceConfig {

	private final Logger LOG = LoggerFactory.getLogger(PersistenceConfig.class);
	@Value("${datasource.username}")
	private String username;

	@Value("${datasource.password}")
	private String password;

	@Value("${datasource.url}")
	private String dataSourceUrl;
	@Value("${datasource.driver.class}")
	private String dataSourceDriverClassName;

	@Bean(name = "dataSource")
	@Primary
	public DataSource dataSource() {
		HikariDataSource ds = new HikariDataSource();
		ds.setPoolName("DSS-Hikari-Pool");
		ds.setJdbcUrl(dataSourceUrl);
		ds.setDriverClassName(dataSourceDriverClassName);
		ds.setUsername(username);
		ds.setPassword(password);
		ds.setAutoCommit(false);
		return ds;
	}

}
