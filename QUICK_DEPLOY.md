# 🚀 Quick DigitalOcean Deployment

## 📋 Ready to Deploy Checklist

✅ **API Keys Configured:**
- Anthropic API: `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`
- News API: `8c11a527332e47f48b536fc233cd6a9d`

✅ **Application Running Locally:**
- Backend: http://localhost:8000 ✅
- Frontend: http://localhost:4000 ✅

✅ **Deployment Scripts Ready:**
- `deploy/digitalocean-setup.sh` - Server setup
- `deploy/deploy.sh` - Application deployment

## 🎯 3-Step Deployment

### Step 1: Create DigitalOcean Droplet
1. Go to https://cloud.digitalocean.com/droplets/new
2. Choose **Ubuntu 22.04 LTS**
3. Select **$6/month Basic plan** (minimum)
4. Add SSH key or use password
5. Create droplet

### Step 2: Setup Server
```bash
ssh root@YOUR_DROPLET_IP

# Run setup script
curl -sSL https://your-repo-url/deploy/digitalocean-setup.sh | bash
```

### Step 3: Deploy Application
```bash
# Clone your repository
git clone https://your-repo-url.git /var/www/comedy-social
cd /var/www/comedy-social

# Run deployment
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

## 🌐 After Deployment

Your app will be accessible at:
- **Main App**: `http://YOUR_DROPLET_IP`
- **API**: `http://YOUR_DROPLET_IP/api`
- **Health Check**: `http://YOUR_DROPLET_IP/health`

## 🔧 Quick Commands

```bash
# Check status
pm2 status

# View logs
pm2 logs

# Restart app
pm2 restart comedy-social-backend

# Monitor
pm2 monit
```

## 💰 Cost: ~$6/month

## 🆘 Need Help?
Refer to `DEPLOYMENT_GUIDE.md` for detailed instructions.

**Your Comedy Social Platform is ready to go live! 🎭**