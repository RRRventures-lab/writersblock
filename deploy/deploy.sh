#!/bin/bash

# Deployment script for Comedy Social Platform
# Run this after digitalocean-setup.sh

set -e

APP_DIR="/var/www/comedy-social"
DOMAIN="your-domain.com"  # Change this to your domain

echo "🚀 Deploying Comedy Social Platform..."

# Navigate to app directory
cd $APP_DIR

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
npm install --production

# Create production environment file
echo "🔧 Creating production environment..."
cat > .env.production << EOF
NODE_ENV=production
PORT=8000
MONGODB_URI=mongodb://localhost:27017/comedy-social-prod
JWT_SECRET=$(openssl rand -base64 32)
JWT_EXPIRE=7d
REDIS_URL=redis://localhost:6379

# AI Service Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=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

# External APIs
NEWS_API_KEY=8c11a527332e47f48b536fc233cd6a9d
TWITTER_BEARER_TOKEN=your-twitter-bearer-token

# File Upload
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=50000000

# Rate Limiting
RATE_LIMIT_WINDOW=15
RATE_LIMIT_MAX=100
EOF

# Create uploads directory
mkdir -p uploads

# Build frontend
echo "🏗️ Building frontend..."
cd ../frontend
npm install
npm run build

# Create PM2 ecosystem file
echo "⚙️ Creating PM2 configuration..."
cd $APP_DIR
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'comedy-social-backend',
    script: './backend/server.js',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    },
    instances: 'max',
    exec_mode: 'cluster',
    max_memory_restart: '500M',
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
EOF

# Create logs directory
mkdir -p logs

# Start application with PM2
echo "🚀 Starting application..."
pm2 start ecosystem.config.js --env production
pm2 save
pm2 startup

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/comedy-social << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Frontend
    location / {
        root $APP_DIR/frontend/build;
        index index.html index.htm;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Health check
    location /health {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Socket.IO
    location /socket.io/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Static files (uploads)
    location /uploads {
        alias $APP_DIR/backend/uploads;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/comedy-social /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Setup firewall
echo "🔒 Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

echo "✅ Deployment complete!"
echo ""
echo "🎭 Comedy Social Platform is now running!"
echo "🌐 Frontend: http://$DOMAIN"
echo "🔧 Backend API: http://$DOMAIN/api"
echo "❤️ Health Check: http://$DOMAIN/health"
echo ""
echo "📊 Monitor with: pm2 monit"
echo "📋 View logs: pm2 logs"
echo "🔄 Restart: pm2 restart comedy-social-backend"
echo ""
echo "🔒 Next: Set up SSL with Let's Encrypt:"
echo "sudo apt install certbot python3-certbot-nginx"
echo "sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"