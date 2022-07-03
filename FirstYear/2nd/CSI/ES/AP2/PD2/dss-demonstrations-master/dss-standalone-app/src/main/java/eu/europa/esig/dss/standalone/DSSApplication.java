package eu.europa.esig.dss.standalone;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import eu.europa.esig.dss.standalone.controller.SignatureController;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;

public class DSSApplication extends Application {

	private static final Logger LOG = LoggerFactory.getLogger(DSSApplication.class);

	private Stage stage;

	@Override
	public void start(Stage stage) {
		this.stage = stage;
		this.stage.setTitle("Digital Signature Service Application");
		this.stage.setResizable(true);
		this.stage.getIcons().add(new Image("/dss-logo.png"));

		initLayout();
	}

	private void initLayout() {
		try {
			FXMLLoader loader = new FXMLLoader();
			loader.setLocation(DSSApplication.class.getResource("/fxml/screen.fxml"));
			Pane pane = loader.load();
			
			Scene scene = new Scene(pane, 1050, 400);
			scene.getStylesheets().add("/styles/style.css");
			stage.setScene(scene);
			stage.show();

			SignatureController controller = loader.getController();
			controller.setStage(stage);
		} catch (Exception e) {
			LOG.error("Unable to init layout : " + e.getMessage(), e);
		}
	}

	public static void main(String[] args) {
		launch(DSSApplication.class, args);
	}

	public Stage getStage() {
		return stage;
	}

}
