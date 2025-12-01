#!/bin/bash
set -e

echo "🏏 Cricket Analytics - Automated Deployment"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}📦 Updating system...${NC}"
apt update -qq

echo -e "${YELLOW}📥 Installing dependencies...${NC}"
apt install -y python3 python3-pip python3-venv nginx git -qq

echo -e "${YELLOW}📂 Setting up application...${NC}"
cd /var/www
if [ -d "cricket-analytics-website" ]; then
    cd cricket-analytics-website
    git pull
else
    git clone https://github.com/rumbleveer-spec/cricket-analytics-website.git
    cd cricket-analytics-website
fi

echo -e "${YELLOW}🐍 Creating Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt gunicorn

mkdir -p data static/css static/js templates

echo -e "${YELLOW}⚙️ Creating systemd service...${NC}"
cat > /etc/systemd/system/cricket-analytics.service << 'EOF'
[Unit]
Description=Cricket Analytics Service
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/cricket-analytics-website
Environment="PATH=/var/www/cricket-analytics-website/venv/bin"
ExecStart=/var/www/cricket-analytics-website/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5001 app:app

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cricket-analytics
systemctl restart cricket-analytics

echo -e "${YELLOW}🌐 Configuring Nginx...${NC}"
if [ ! -f /etc/nginx/sites-available/cricket ]; then
    cat > /etc/nginx/sites-available/cricket << 'EOF'
server {
    listen 80;
    server_name cricket.srv1138131.hstgr.cloud 72.61.224.193;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/cricket-analytics-website/static;
    }
}
EOF
    ln -sf /etc/nginx/sites-available/cricket /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
fi

echo -e "${YELLOW}🔐 Configuring firewall...${NC}"
ufw --force enable 2>/dev/null
ufw allow 22 2>/dev/null
ufw allow 80 2>/dev/null
ufw allow 443 2>/dev/null

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo "🌐 Access: http://72.61.224.193:5001"
echo "📊 Status: systemctl status cricket-analytics"
echo "📝 Logs: journalctl -u cricket-analytics -f"
