#!/bin/bash
#./dss-demo-bundle/target/dss-demo-bundle-5.10.1/apache-tomcat-8.5.78/bin/shutdown.sh
mvn clean install #-Dmaven.test.skip=true
unzip dss-demo-bundle/target/dss-demo-bundle-5.10.1.zip -d dss-demo-bundle/target/
chmod +x dss-demo-bundle/target/dss-demo-bundle-5.10.1/apache-tomcat-8.5.78/bin/startup.sh
chmod +x dss-demo-bundle/target/dss-demo-bundle-5.10.1/apache-tomcat-8.5.78/bin/shutdown.sh
chmod +x dss-demo-bundle/target/dss-demo-bundle-5.10.1/apache-tomcat-8.5.78/bin/catalina.sh
./dss-demo-bundle/target/dss-demo-bundle-5.10.1/apache-tomcat-8.5.78/bin/startup.sh
