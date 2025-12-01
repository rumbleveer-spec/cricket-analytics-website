#!/bin/bash
set -e

echo "🏏 Cricket Analytics - One-Click Deployment"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo -e "${YELLOW}📦 Updating system...${NC}"
apt update -qq

echo -e "${YELLOW}📥 Installing dependencies...${NC}"
apt install -y python3 python3-pip python3-venv nginx git -qq

# Clone or update repo
cd /var/www
if [ -d "cricket-analytics-website" ]; then
    echo -e "${YELLOW}📂 Updating repository...${NC}"
    cd cricket-analytics-website
    git pull
else
    echo -e "${YELLOW}📂 Cloning repository...${NC}"
    git clone https://github.com/rumbleveer-spec/cricket-analytics-website.git
    cd cricket-analytics-website
fi

# Setup Python environment
echo -e "${YELLOW}🐍 Setting up Python...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt gunicorn

# Create directories
mkdir -p data static/css static/js templates

# Initialize database
echo -e "${YELLOW}💾 Initializing database...${NC}"
python app.py &
sleep 3
pkill -f "python app.py" || true

# Create systemd service
echo -e "${YELLOW}⚙️ Creating service...${NC}"
cat > /etc/systemd/system/cricket-analytics.service << 'EOF'
[Unit]
Description=Cricket Analytics Gunicorn Service
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/cricket-analytics-website
Environment="PATH=/var/www/cricket-analytics-website/venv/bin"
ExecStart=/var/www/cricket-analytics-website/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cricket-analytics
systemctl restart cricket-analytics

# Configure Nginx
if [ ! -f /etc/nginx/sites-available/cricket-analytics ]; then
    echo -e "${YELLOW}🌐 Configuring Nginx...${NC}"
    cat > /etc/nginx/sites-available/cricket-analytics << 'EOF'
server {
    listen 80;
    server_name cricket.srv1138131.hstgr.cloud 72.61.224.193;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/cricket-analytics-website/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    ln -sf /etc/nginx/sites-available/cricket-analytics /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
fi

# Firewall
echo -e "${YELLOW}🔐 Configuring firewall...${NC}"
ufw --force enable
ufw allow 22
ufw allow 80
ufw allow 443

# Check status
sleep 2
echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 Your Cricket Analytics Website is LIVE!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Access at:"
echo "   → http://72.61.224.193:5001"
echo "   → http://cricket.srv1138131.hstgr.cloud (after DNS)"
echo ""
echo "📊 Service Status:"
systemctl is-active cricket-analytics >/dev/null 2>&1 && echo -e "   ✅ App: Running" || echo -e "   ❌ App: Failed"
systemctl is-active nginx >/dev/null 2>&1 && echo -e "   ✅ Nginx: Running" || echo -e "   ❌ Nginx: Failed"
echo ""
echo "🔧 Useful Commands:"
echo "   Restart: systemctl restart cricket-analytics"
echo "   Logs:    journalctl -u cricket-analytics -f"
echo "   Status:  systemctl status cricket-analytics"
echo ""
