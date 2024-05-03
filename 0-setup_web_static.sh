#!/usr/bin/env bash
# This script sets up the web servers for the deployment of web_static.

# Install Nginx if it is not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Create the required directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Testing Moussafir.tech Domain
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ directory to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content
if ! grep -q "hbnb_static" /etc/nginx/sites-available/default; then
    sudo sed -i '/server_name _;/a \\tlocation /hbnb_static/ { alias /data/web_static/current/; autoindex off; }' /etc/nginx/sites-available/default
fi

# Restart Nginx to apply the configuration changes
sudo service nginx restart

# Exit successfully
exit 0
