# 🏏 Cricket Analytics Website

Data-driven cricket tournament analysis platform featuring BBL, WBBL, and Super Smash statistics with interactive dashboards.

## 🌟 Features

- **Interactive Dashboards** - Real-time cricket statistics visualization
- **Match Analysis** - Comprehensive match-by-match breakdown
- **Player Statistics** - Detailed batting and bowling analytics
- **Team Strategies** - Tactical insights and performance metrics
- **Venue Analysis** - Ground-specific performance data
- **Responsive Design** - Mobile-friendly interface

## 🛠️ Tech Stack

- **Backend**: Flask (Python 3.10+)
- **Database**: SQLite3
- **Frontend**: Bootstrap 5 + Chart.js + DataTables
- **Server**: Nginx + Gunicorn

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Local Development

```bash
# Clone repository
git clone https://github.com/rumbleveer-spec/cricket-analytics-website.git
cd cricket-analytics-website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Application will be available at `http://localhost:5000`

## 🚀 Deployment on Hostinger VPS

### Server Details
- **IP**: 72.61.224.193
- **Hostname**: srv1138131.hstgr.cloud
- **Resources**: 2 CPU cores, 8GB RAM, 100GB disk

### Step 1: Connect to VPS

```bash
ssh root@72.61.224.193
```

### Step 2: Update System

```bash
apt update && apt upgrade -y
apt install python3 python3-pip python3-venv nginx git -y
```

### Step 3: Clone & Setup Application

```bash
cd /var/www
git clone https://github.com/rumbleveer-spec/cricket-analytics-website.git
cd cricket-analytics-website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt gunicorn

# Create necessary directories
mkdir -p data static/css static/js templates

# Initialize database
python app.py  # Press Ctrl+C after db creation
```

### Step 4: Configure Gunicorn

Create `/etc/systemd/system/cricket-analytics.service`:

```ini
[Unit]
Description=Cricket Analytics Gunicorn Service
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/cricket-analytics-website
Environment="PATH=/var/www/cricket-analytics-website/venv/bin"
ExecStart=/var/www/cricket-analytics-website/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
systemctl daemon-reload
systemctl enable cricket-analytics
systemctl start cricket-analytics
systemctl status cricket-analytics
```

### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/cricket-analytics`:

```nginx
server {
    listen 80;
    server_name 72.61.224.193 srv1138131.hstgr.cloud;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/cricket-analytics-website/static;
        expires 30d;
    }
}
```

Enable site and restart Nginx:

```bash
ln -s /etc/nginx/sites-available/cricket-analytics /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 6: Access Your Website

Visit: `http://72.61.224.193` or `http://srv1138131.hstgr.cloud`

## 📊 Populate Database

To add cricket data to the database, you'll need to create a data import script. The Google Sheet with all data is available at:
https://docs.google.com/spreadsheets/d/1Zs__sR5UDLnOs1uZ84EQB531MUFhVl1Y-oyXPp7bL8I/edit

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///data/cricket_data.db
FLASK_ENV=production
```

### Security Checklist

- [ ] Change SECRET_KEY in config.py
- [ ] Set up firewall (ufw)
- [ ] Configure SSL/HTTPS (Let's Encrypt)
- [ ] Regular backups of database
- [ ] Monitor logs

## 📈 Future Enhancements

- [ ] Live score integration
- [ ] User authentication system
- [ ] Advanced analytics dashboard
- [ ] API endpoints for mobile app
- [ ] Real-time match updates
- [ ] Player comparison tool
- [ ] Export reports (PDF/Excel)

## 🐛 Troubleshooting

**Application not starting:**
```bash
journalctl -u cricket-analytics -n 50
```

**Nginx errors:**
```bash
tail -f /var/log/nginx/error.log
```

**Database issues:**
```bash
rm data/cricket_data.db
python app.py  # Recreate database
```

## 📝 License

MIT License - Feel free to use and modify

## 👨‍💻 Developer

Created by Rube AI for comprehensive cricket analytics

## 📧 Support

For issues, please open a GitHub issue or contact support.

---

**Note**: This is a starter template. Add HTML templates, CSS, and populate the database with cricket data from the provided Google Sheet.
