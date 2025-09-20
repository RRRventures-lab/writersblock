#!/bin/bash

# DigitalOcean Droplet Setup Script for Comedy Social Platform
# Run this script on a fresh Ubuntu 22.04 droplet

set -e

echo "🚀 Setting up Comedy Social Platform on DigitalOcean..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Install Redis
sudo apt install redis-server -y
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Install PM2 for process management
sudo npm install -g pm2

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y

# Create app directory
sudo mkdir -p /var/www/comedy-social
sudo chown -R $USER:$USER /var/www/comedy-social

echo "✅ Basic setup complete!"
echo "📝 Next steps:"
echo "1. Clone your repository to /var/www/comedy-social"
echo "2. Run the deployment script"
echo "3. Configure Nginx"