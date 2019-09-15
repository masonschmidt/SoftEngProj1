# SoftEngProj1

Here are the instruction for starting a server for both java and python. If you want
you can start both servers on the same machine by following them back to back.

## Table of Contents

[VM Setup](#vmsetup)  
[Java Setup with Tomcat](#javasetup)  
[Python Setup with nginx and uwsgi](#pythonsetup)  
[Restarting a previously setup Server](#restarting)  
[Starting a Java server using App Engine](#appenginejava)  
[Starting a Python server using App Engine](#appenginepython)

<a name="vmsetup"/>

## VM Setup
What is needed:  
Access to Google Cloud Platform  
Computer Able to Connect to Virtual Machine  
Available Space for a Virtual Machine

Visit Google Cloud Platform  
Click 3 Lines at Top Left of the Page  
Hover your mouse over “Compute Engine” item and Click VM instances from pop-up
menu.

Click “CREATE INSTANCE” from VM instances Page  
Name your instance any name  
Specify the Machine Type as g1-small(1 vCPU, 1.7 GB memory)  
Change the Boot Disk Option to Ubuntu 18.04 LTS  
Select the Following Radio Button “Allow full access to all Cloud APIs”  
Select the Following Checkboxes “Allow HTTP and HTTPS traffic”  
Create

Open the Menu back up at top left and scroll down the menu and hover
“VPC NETWORK” and click External IP addresses.
At the External IP addresses page, select where your instance says Ephemeral
and change to static. Give it a cool name.

<a name ="javasetup"/>

## Java Setup with tomcat
The left of the page should display a submenu, click "Firewall rules".  
Click "CREATE FIREWALL RULE" and name the rule "allow-tomcat".  
Scroll down and select targets. From the drop down menu, click
"All instances in the network".  
Change the Source IP ranges to "0.0.0.0/0".  
Click the "Allow all" radio button in Protocols and ports.  
CREATE

Use the top left menu to navigate back over to VM instances through the Compute
engine.  
Click SSH under connect on your created instance and allow the window to pop up
and transfer keys to your instance.  

Commands:
~~~
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install default-jdk
sudo groupadd tomcat
sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat
cd /tmp
wget http://apache-mirror.8birdsvideo.com/tomcat/tomcat-9/v9.0.24/bin/apache-tomcat-9.0.24.tar.gz
sudo mkdir /opt/tomcat/
sudo tar xzvf apache-tomcat-9.0.24.tar.gz -C /opt/tomcat --strip-components=1
cd /opt/tomcat/
sudo chgrp -R tomcat /opt/tomcat
sudo chmod -R g+r conf
sudo chmod g+x conf
sudo chown -R tomcat webapps/ work/ temp/ logs/
sudo update-java-alternatives -l
sudo nano /etc/environment
~~~


add Following line to end of document and save:
~~~
JAVA_HOME="/usr/lib/jvm/java-1.11.0-openjdk-amd64"
~~~

Next input these commands on the console.

~~~
source /etc/environment
echo $JAVA_HOME
sudo nano /etc/systemd/system/tomcat.service
~~~

Add This to the file tomcat.service

~~~
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

Environment=JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
Environment=CATALINA_PID=/opt/tomcat/temp/tomcat.pid
Environment=CATALINA_HOME=/opt/tomcat
Environment=CATALINA_BASE=/opt/tomcat
Environment='CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC'
Environment='JAVA_OPTS=-Djava.awt.headless=true -Djava.security.egd=file:/dev/./urandom'

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

User=tomcat
Group=tomcat
UMask=0007
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
~~~

Save and go back to the console

~~~
sudo systemctl daemon-reload
sudo systemctl start tomcat
sudo systemctl status tomcat.service
~~~

### Check if Tomcat is running.
Ensure TOMCAT is running!!!!! Any issues can be found in /opt/tomcat/logs.  
To do this, enter the following lines:

~~~
sudo chown -R [Username]:[Username] /opt/tomcat
cat /opt/tomcat/logs/catalina.out
~~~

Check the log and ensure you enter the following line after checking:
~~~
sudo chown -R tomcat /opt/tomcat
~~~

### Creating Java File and running server

check if you did a good job by using the following command. The external address
is the ip of your VM, which you can find on the VM instances page in compute engine.
~~~
curl -g -6 "http://extrenaladdress:8080/"
~~~

Next create the jsp file.

~~~
sudo chown -R [Username]:[Username] /opt/tomcat/
cd /opt/tomcat/webapps/ROOT/
sudo nano Random.jsp
~~~

Enter the following lines in the file and save:

~~~
<%@ page language="java" contentType="text/html"%>
<%@ page import="java.text.*,java.lang.Math" %>
<html>
	<head>
		<title>Date JSP</title>
	</head>
<% int random_num= (int)(Math.random()*1000000+1); %>
<body>
	<h1><%= random_num %></h1>
</body>
</html>
~~~

Save and go back to the command line.

~~~
cd ../../
sudo chown -R tomcat /opt/tomcat
sudo systemctl stop tomcat
sudo systemctl daemon-reload
sudo systemctl start tomcat
~~~

Your server should be running! Go to you browser and type in
http://externaladdress:8080/Random.jsp to access the random number.

<a name="pythonsetup"/>

## Python setup with nginx and uwsgi


### Navigate to VM
If you haven't already.  
Use the top left menu to navigate back over to VM instances through the Compute
engine.  
Click SSH under connect on your created instance and allow the window to pop up
and transfer keys to your instance.

### Server setup.
Enter these commands, username:username requires the username for the VM.

~~~
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install nginx
sudo mkdir /var/www/demoapp
sudo chown -R ubuntu:ubuntu /var/www/demoapp/
cd /var/www/demoapp/
sudo apt-get install python-virtualenv
virtualenv venv
sudo chown -R username:username /var/www/demoapp/
virtualenv venv
. venv/bin/activate
pip install flask
sudo ufw allow 8081
nano hello.py
~~~

Enter the in the file.

~~~
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  import random
  return str(random.randint(1,1000001))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8081)
~~~

Next Run the script to make sure there are no problems.

~~~
python hello.py
~~~

Now to continue.

~~~
sudo apt-get install build-essential python python-dev
pip install uwsgi
sudo rm /etc/nginx/sites-enabled/default
nano demoapp_nginx.conf
~~~

Enter this in the file.

~~~
server {
    listen      80;
    server_name localhost;
    charset     utf-8;
    client_max_body_size 75M;

    location / { try_files $uri @yourapplication; }
    location @yourapplication {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/demoapp/demoapp_uwsgi.sock;
    }
}
~~~

Save and go back to the console.

~~~
sudo ln -s /var/www/demoapp/demoapp_nginx.conf
sudo ln -s /var/www/demoapp/demoapp_nginx.conf /etc/nginx/conf.d/
sudo /etc/init.d/nginx restart
nano demoapp_uwsgi.ini
~~~

Place this in the file.

~~~
[uwsgi]
#application's base folder
base = /var/www/demoapp

#python module to import
app = hello
module = %(app)

home = %(base)/venv
pythonpath = %(base)

#socket file's location
socket = /var/www/demoapp/%n.sock

#permissions for the socket file
chmod-socket    = 666

#the variable that holds a flask application inside the module imported at line #6
callable = app

#location of log files
logto = /var/log/uwsgi/%n.log
~~~

Save and go back to the console.

~~~
sudo mkdir -p /var/log/uwsgi
sudo chown -R ubuntu:ubuntu /var/log/uwsgi
sudo chown -R username:username /var/log/uwsgi
uwsgi --ini /var/www/demoapp/demoapp_uwsgi.ini
~~~

To test if it is up and running go a browser and go to the url  
http://externaladdress/

<a name="restarting"/>

## Restarting a python server.
~~~
cd /var/www/demoapp
sudo /etc/init.d/nginx start
source venv/bin/activate
uwsgi --ini /var/www/demoapp/demoapp_uwsgi.ini
~~~

## Restarting a Java server.
~~~
sudo systemctl start tomcat
~~~


## How to Run it on App Engine Java
Go to google cloud dashboard page

Click the Select from drop-down list at the top of the page.
click on new project on top right corner

give it a project name and click create

open cloud shell and activate cloud shell

in the shell do the following commands:
~~~
git clone https://github.com/GoogleCloudPlatform/appengine-try-java
~~~
~~~
cd cd appengine-try-java
nano /src/main/java/myapp/DemoServlet.java
~~~

Delete the code in DemoServlet.java and copy paste the following code and save
~~~
package myapp;
import java.io.IOException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.lang.Math;
public class DemoServlet extends HttpServlet {
  @Override
  public void doGet(HttpServletRequest req, HttpServletResponse resp)
      throws IOException {
    resp.setContentType("text/plain");
    int random = (int)(Math.random() * 1000000 + 1);
    resp.getWriter().println("{ \"name\": " + random + " }");
  }
}

~~~

~~~
navigate back to appengine-try-java

nano /src/main/webapp/index.html
~~~
Delete the code in index.html and copy paste the following code and save

~~~
<!doctype html>
<html>
  <head>
    <title>App Engine Demo</title>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
  </head>
  <body>
    <div id="result">Loading...</div>
    <script>
$(document).ready(function() {
  $.getJSON('/demo', function(data) {
    $('#result').html(data.name);
  });
});
    </script>
  </body>
</html>
~~~
navigate back to appengine-try-java

to test if its working run the following command
~~~
mvn appengine:run
~~~
click on the web preview to see it on a browser

To Deploy it
~~~
gcloud app create

gcloud config set project [project_name]
mvn appengine:deploy
~~~

Go to
[project_name].appspot.com.

<a name="appenginepython"/>

## How to Run it on App Engine Python
Go to google cloud dashboard page

Click the Select from drop-down list at the top of the page.
click on new project on top right corner

give it a project name and click create

open cloud shell and activate cloud shell

in the shell do the following commands:
~~~
git clone https://github.com/GoogleCloudPlatform/python-docs-samples
cd python-docs-samples/appengine/standard_python37/hello_world

nano main.py
~~~
Delete the code in main.py and copy paste the following code and save
~~~
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  import random
  return str(random.randint(1,1000001))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8081)
~~~

to test if its working run the following command
click on the web preview to see it on a browser

~~~
virtualenv --python python3~/envs/hello_world

source ~/envs/hello_world/bin/activate

pip install -r requirements.txt

python main.py
~~~

To Deploy it
~~~
gcloud app create //skip this if app is already created
gcloud app deploy app.yaml --project skilled-eon-251901
~~~

Go to

[project_name].appspot.com
