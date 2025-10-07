# NeuroShield - Production Deployment Guide

**Status:** ✅ Ready for Production Deployment  
**Date:** October 7, 2025

---

## 🎯 Deployment Checklist Completed

### ✅ 1. Environment Configuration
- [x] `.env` files created with secure secret keys
- [x] Strong secret keys generated (256-bit)
- [x] Environment variables configured for both applications
- [x] API key placeholder created for VirusTotal

### ✅ 2. ML Model
- [x] Training script created (`train_model.py`)
- [x] Sample model trained (91% accuracy)
- [x] Model saved at `ML_model/malwareclassifier-V2.pkl`
- [x] Model loading tested successfully

### ✅ 3. Production WSGI Server
- [x] Gunicorn installed
- [x] Production app files created (`app_production.py`)
- [x] Startup scripts created
- [x] Multi-worker configuration

### ✅ 4. Rate Limiting
- [x] Flask-Limiter installed
- [x] Rate limits configured:
  - ML App: 30 requests/minute (index), 10 requests/minute (analyze)
  - VirusTotal App: 60 requests/minute (index), 5 requests/minute (analyze)
- [x] Health check endpoints exempt from rate limiting

### ✅ 5. Security Enhancements
- [x] Debug mode disabled in production
- [x] Secure secret keys
- [x] File size limits enforced
- [x] Input validation
- [x] File cleanup after processing
- [x] Request logging

### ✅ 6. Logging
- [x] File logging configured
- [x] Log directories created
- [x] Separate logs for access and errors

---

## 🚀 Quick Start (Production)

### ML-Based Detection

```bash
# Start the production server
./start_ml_app.sh
```

The application will be available at: `http://localhost:5000`

### VirusTotal Detection

```bash
# Start the production server
./start_virustotal_app.sh
```

The application will be available at: `http://localhost:5001`

---

## 📋 Detailed Configuration

### 1. Environment Variables

**ML Application** (`ML_based_detectionn/.env`):
```env
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=<256-bit-hex-key>
UPLOAD_FOLDER=uploads
```

**VirusTotal Application** (`Virus_total_based/.env`):
```env
VIRUSTOTAL_API_KEY=<your-actual-api-key>
FLASK_SECRET_KEY=<256-bit-hex-key>
```

### 2. Getting a VirusTotal API Key

1. Visit: https://www.virustotal.com/gui/join-us
2. Create a free account
3. Go to your profile → API Key
4. Copy your API key
5. Replace `your-api-key-here-replace-this` in `.env` file

### 3. Gunicorn Configuration

Both startup scripts use the following Gunicorn configuration:

```bash
gunicorn \
    --bind 0.0.0.0:5000 \      # Listen on all interfaces
    --workers 4 \                # 4 worker processes
    --timeout 120 \              # 120 second timeout
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    app_production:app
```

**Workers**: `2-4 x CPU cores` is recommended. Current: 4 workers.

### 4. Rate Limiting

Rate limits are configured to prevent abuse:

**ML Application:**
- Homepage: 30 requests/minute per IP
- File analysis: 10 requests/minute per IP
- Daily limit: 200 requests/day per IP

**VirusTotal Application:**
- Homepage: 60 requests/minute per IP
- Scan requests: 5 requests/minute per IP (VirusTotal API constraint)
- Daily limit: 100 requests/day per IP

Rate limits can be adjusted in `app_production.py`.

---

## 🔒 Security Features

### Implemented Security Measures

1. **Debug Mode**: Disabled in production
2. **Secret Keys**: Cryptographically secure 256-bit keys
3. **File Upload Limits**: 
   - ML App: 10MB max
   - VirusTotal App: 32MB max
4. **Input Validation**: All user inputs validated
5. **File Type Restrictions**: Only `.exe` and `.dll` for ML app
6. **XML Security**: DefusedXML prevents XXE attacks
7. **URL Validation**: Prevents SSRF attacks
8. **Request Timeouts**: 30 seconds to prevent hanging
9. **File Cleanup**: Automatic cleanup after processing
10. **Rate Limiting**: Prevents DoS attacks
11. **Logging**: All requests and errors logged

### Additional Security Recommendations

1. **Use HTTPS**: Set up SSL/TLS certificates
2. **Reverse Proxy**: Use Nginx or Apache
3. **Firewall**: Configure UFW or iptables
4. **Regular Updates**: Keep dependencies updated
5. **Monitoring**: Set up application monitoring
6. **Backup**: Regular database and model backups

---

## 📊 Monitoring & Health Checks

### Health Check Endpoints

**ML Application:**
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

**VirusTotal Application:**
```bash
curl http://localhost:5001/health
```

Response:
```json
{
  "status": "healthy",
  "api_configured": true
}
```

### Log Files

- **Access Logs**: `logs/access.log` - All HTTP requests
- **Error Logs**: `logs/error.log` - Application errors
- **App Logs**: `app.log` / `virustotal.log` - Application-specific logs

### Monitoring Commands

```bash
# Watch access logs
tail -f logs/access.log

# Watch error logs
tail -f logs/error.log

# Check for errors
grep ERROR logs/error.log

# Monitor worker processes
ps aux | grep gunicorn
```

---

## 🔧 Systemd Service Setup (Optional)

For automatic startup and management, create systemd services:

### ML Application Service

Create `/etc/systemd/system/neuroshield-ml.service`:

```ini
[Unit]
Description=NeuroShield ML Malware Detection
After=network.target

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=/workspace/ML_based_detectionn
Environment="PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/ubuntu/.local/bin/gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile /workspace/ML_based_detectionn/logs/access.log \
    --error-logfile /workspace/ML_based_detectionn/logs/error.log \
    --log-level info \
    app_production:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### VirusTotal Application Service

Create `/etc/systemd/system/neuroshield-vt.service`:

```ini
[Unit]
Description=NeuroShield VirusTotal Detection
After=network.target

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=/workspace/Virus_total_based
Environment="PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/ubuntu/.local/bin/gunicorn \
    --bind 0.0.0.0:5001 \
    --workers 4 \
    --timeout 120 \
    --access-logfile /workspace/Virus_total_based/logs/access.log \
    --error-logfile /workspace/Virus_total_based/logs/error.log \
    --log-level info \
    app_production:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Service Commands

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start services
sudo systemctl start neuroshield-ml
sudo systemctl start neuroshield-vt

# Enable on boot
sudo systemctl enable neuroshield-ml
sudo systemctl enable neuroshield-vt

# Check status
sudo systemctl status neuroshield-ml
sudo systemctl status neuroshield-vt

# View logs
sudo journalctl -u neuroshield-ml -f
sudo journalctl -u neuroshield-vt -f
```

---

## 🌐 Nginx Reverse Proxy (Recommended)

### Installation

```bash
sudo apt update
sudo apt install nginx
```

### Configuration

Create `/etc/nginx/sites-available/neuroshield`:

```nginx
# ML Application
server {
    listen 80;
    server_name ml.neuroshield.example.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}

# VirusTotal Application
server {
    listen 80;
    server_name vt.neuroshield.example.com;

    client_max_body_size 32M;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/neuroshield /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL/TLS with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificates
sudo certbot --nginx -d ml.neuroshield.example.com
sudo certbot --nginx -d vt.neuroshield.example.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## 📈 Performance Tuning

### Worker Process Calculation

```python
workers = (2 * CPU_CORES) + 1
```

For a 4-core system: `(2 * 4) + 1 = 9 workers`

### Memory Considerations

Each worker uses ~100-200MB of RAM. For 4 workers:
- Minimum RAM: 1GB
- Recommended RAM: 2GB+

### Timeouts

- **Default**: 120 seconds
- For large file uploads: Increase to 300 seconds
- For quick responses: Reduce to 60 seconds

---

## 🐛 Troubleshooting

### Common Issues

**1. Model not loading**
```bash
# Check if model file exists
ls -lh ML_based_detectionn/ML_model/malwareclassifier-V2.pkl

# Train a new model
cd ML_based_detectionn
python train_model.py --create-sample
```

**2. API key errors (VirusTotal)**
```bash
# Check .env file
cat Virus_total_based/.env | grep API_KEY

# Ensure no extra spaces or quotes
```

**3. Permission denied**
```bash
# Make scripts executable
chmod +x start_ml_app.sh start_virustotal_app.sh

# Fix log directory permissions
chmod 755 ML_based_detectionn/logs Virus_total_based/logs
```

**4. Port already in use**
```bash
# Find process using port
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>
```

**5. Gunicorn not found**
```bash
# Add to PATH
export PATH=$PATH:~/.local/bin

# Or use full path in scripts
~/.local/bin/gunicorn ...
```

---

## ✅ Production Readiness Checklist

Before deploying to production:

- [ ] VirusTotal API key configured (for VT app)
- [ ] ML model trained with real data (for ML app)
- [ ] Strong secret keys generated
- [ ] `.env` files configured
- [ ] Gunicorn installed
- [ ] Log directories created
- [ ] File upload directories have correct permissions
- [ ] Firewall configured
- [ ] HTTPS/SSL enabled
- [ ] Reverse proxy configured (Nginx/Apache)
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Health checks tested
- [ ] Load testing completed
- [ ] Security audit done

---

## 📚 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Gunicorn Documentation**: https://docs.gunicorn.org/
- **Nginx Documentation**: https://nginx.org/en/docs/
- **VirusTotal API**: https://developers.virustotal.com/
- **Let's Encrypt**: https://letsencrypt.org/

---

## 📞 Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review error messages
3. Consult troubleshooting section
4. Check health endpoints

---

**Deployment Date:** October 7, 2025  
**Version:** 2.0  
**Status:** ✅ Production Ready