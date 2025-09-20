# 🚀 DigitalOcean Deployment Guide

Complete guide to deploy your Comedy Social Media Platform on DigitalOcean.

## 📋 Prerequisites

1. **DigitalOcean Account** - Sign up at https://digitalocean.com
2. **Domain Name** (optional but recommended)
3. **API Keys** (already configured):
   - ✅ Anthropic API Key: `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`
   - ✅ News API Key: `8c11a527332e47f48b536fc233cd6a9d`

## 🖥️ Step 1: Create DigitalOcean Droplet

1. **Create Droplet:**
   - Go to https://cloud.digitalocean.com/droplets/new
   - Choose **Ubuntu 22.04 LTS**
   - Select **Basic Plan** ($6/month minimum recommended)
   - Choose datacenter region closest to your users
   - Add SSH key or use password authentication
   - Name it `comedy-social-platform`

2. **Connect to Droplet:**
```bash
ssh root@your-droplet-ip
```

## 🔧 Step 2: Initial Server Setup

Run the setup script:
```bash
# Download and run setup script
curl -fsSL https://raw.githubusercontent.com/your-repo/deploy/digitalocean-setup.sh -o setup.sh
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
# Update system
apt update && apt upgrade -y

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
apt-get update && apt-get install -y mongodb-org

# Install Redis & Nginx
apt install redis-server nginx git -y

# Install PM2
npm install -g pm2

# Start services
systemctl start mongod redis-server nginx
systemctl enable mongod redis-server nginx
```

## 📁 Step 3: Deploy Application

1. **Clone Repository:**
```bash
# Create app directory
mkdir -p /var/www/comedy-social
cd /var/www/comedy-social

# Clone your repository
git clone https://github.com/RRRventures-lab/writersblock.git .
```

2. **Run Deployment Script:**
```bash
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

This script will:
- Install dependencies
- Build frontend
- Configure environment variables
- Set up PM2 for process management
- Configure Nginx reverse proxy
- Start the application

## 🌐 Step 4: Domain Configuration (Optional)

If you have a domain:

1. **Update DNS Records:**
   - Point your domain A record to your droplet IP
   - Add www subdomain if desired

2. **Update deployment script:**
```bash
# Edit deploy.sh and change:
DOMAIN="your-actual-domain.com"
```

3. **Set up SSL (Recommended):**
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d your-domain.com -d www.your-domain.com
```

## ✅ Step 5: Verify Deployment

1. **Check Services:**
```bash
# Check PM2 status
pm2 status

# Check Nginx
systemctl status nginx

# Check MongoDB
systemctl status mongod
```

2. **Test Application:**
```bash
# Health check
curl http://your-droplet-ip/health

# Or with domain
curl http://your-domain.com/health
```

3. **Access Application:**
   - Frontend: `http://your-droplet-ip` or `http://your-domain.com`
   - API: `http://your-droplet-ip/api` or `http://your-domain.com/api`

## 🔒 Step 6: Security Setup

1. **Firewall:**
```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

2. **Create Non-Root User:**
```bash
adduser comedyapp
usermod -aG sudo comedyapp
# Copy SSH keys to new user
```

3. **Secure MongoDB:**
```bash
mongo
use admin
db.createUser({
  user: "admin",
  pwd: "your-secure-password",
  roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
})
```

## 📊 Step 7: Monitoring & Maintenance

### Process Management:
```bash
# View running processes
pm2 list

# Monitor in real-time
pm2 monit

# View logs
pm2 logs

# Restart application
pm2 restart comedy-social-backend

# Stop application
pm2 stop comedy-social-backend
```

### Nginx Commands:
```bash
# Check configuration
nginx -t

# Reload configuration
systemctl reload nginx

# View access logs
tail -f /var/log/nginx/access.log
```

### MongoDB Commands:
```bash
# Connect to MongoDB
mongo

# Show databases
show dbs

# Use comedy database
use comedy-social-prod

# Show collections
show collections
```

## 🔄 Step 8: Updates & Deployment

To deploy updates:
```bash
cd /var/www/comedy-social

# Pull latest changes
git pull origin main

# Backend updates
cd backend
npm install --production

# Frontend updates
cd ../frontend
npm install
npm run build

# Restart application
pm2 restart comedy-social-backend
```

## 🚨 Troubleshooting

### Common Issues:

1. **Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill -9
pm2 restart comedy-social-backend
```

2. **MongoDB connection issues:**
```bash
systemctl status mongod
systemctl restart mongod
```

3. **Nginx 502 errors:**
```bash
# Check if backend is running
pm2 status
# Check Nginx logs
tail -f /var/log/nginx/error.log
```

4. **Frontend not loading:**
```bash
# Check if build directory exists
ls -la /var/www/comedy-social/frontend/build
# Rebuild if necessary
cd /var/www/comedy-social/frontend && npm run build
```

## 📈 Performance Optimization

1. **Enable Gzip in Nginx:**
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

2. **Set up CDN for static assets**

3. **Configure Redis caching**

4. **Set up MongoDB indexes for better performance**

## 🎯 Production Checklist

- [ ] Droplet created and configured
- [ ] Domain DNS configured (if applicable)
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] MongoDB secured
- [ ] Application deployed and running
- [ ] Health check responding
- [ ] PM2 monitoring set up
- [ ] Nginx logs configured
- [ ] Backup strategy implemented

## 💡 Cost Estimation

**Monthly Costs:**
- Basic Droplet ($6/month): $6
- Domain name (optional): $10-15/year
- SSL Certificate: Free (Let's Encrypt)

**Total: ~$6/month for basic setup**

## 🆘 Support

If you encounter issues:
1. Check logs: `pm2 logs`
2. Check system status: `systemctl status mongod nginx`
3. Check firewall: `ufw status`
4. Test API directly: `curl localhost:8000/health`

Your Comedy Social Platform should now be live and accessible! 🎭✨