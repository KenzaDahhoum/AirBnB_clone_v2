#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install Nginx if it is not already installed
apt-get update
apt-get -y install nginx

# Create required directories
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo '<html>
  <head>
  </head>
  <body>
    Moussafir Domain
  </body>
</html>' > /data/web_static/releases/test/index.html

# Create a symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership
chown -hR ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content of /data/web_static/current/
if ! grep -q "hbnb_static" /etc/nginx/sites-available/default; then
    sed -i '/server_name _;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}' /etc/nginx/sites-available/default
fi

# Restart Nginx to apply changes
service nginx restart
