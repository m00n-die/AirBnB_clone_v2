#!/usr/bin/env bash
# Sets up webservers for deployment of static
 if ! dpkg -l nginx | grep -E 'îi.*nginx' > /dev/null 2>&1; then
    sudo apt update
    sudo apt install -y nginx
    sudo ufw allow 'Nginx Full'
fi
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/

SERVER_CONFIG="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
	alias /data/web_static/current;
	index index.html index.htm;
    }
    location /redirect_me {
	return 301 http://cuberule.com/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"
sudo bash -c "echo -e '$SERVER_CONFIG' > /etc/nginx/sites-available/default"

sudo service nginx restart
