# NeuroShield Branding Update

**Date:** October 7, 2025  
**Status:** ✅ Complete

---

## 📝 Summary

All website names and references have been updated to use the **NeuroShield** branding consistently across both applications.

---

## ✅ Changes Made

### 1. ML-Based Detection Application

**File:** `ML_based_detectionn/templates/index.html`
- Page Title: `NeuroShield - AI-Powered Malware Detection`
- Main Header: `NeuroShield - AI Malware Detection`
- Section Header: `NeuroShield`
- Navigation: Updated links (removed hardcoded IPs)

**File:** `ML_based_detectionn/templates/result.html`
- Page Title: `NeuroShield - Analysis Result`
- Footer: `© 2025 NeuroShield. All Rights Reserved by F.J.G.`

---

### 2. VirusTotal-Based Detection Application

**File:** `Virus_total_based/templates/index.html`
- Main Header: `NeuroShield - Threat Intelligence Platform`
- Section Header: `NeuroShield`
- Navigation: Updated links

**File:** `Virus_total_based/templates/result.html`
- Footer: `© 2025 NeuroShield. All Rights Reserved by F.J.G.`
- Chart Titles: 
  - `NeuroShield Detection Results (Bar Chart)`
  - `NeuroShield Detection Results (Pie Chart)`

**File:** `Virus_total_based/templates/details.html`
- Footer: `© 2025 NeuroShield. All Rights Reserved by F.J.G.`

---

## 🌐 Domain References

The applications are now branded as **NeuroShield** and can be configured to use:

### Development (Local)
- ML Detection: `http://localhost:5000`
- VirusTotal Detection: `http://localhost:5001`

### Production (Example Domains)

**Option 1: Subdomain Structure**
- ML Detection: `https://ml.neuroshield.com`
- VirusTotal Detection: `https://vt.neuroshield.com`
- Main Site: `https://neuroshield.com`

**Option 2: Path-Based Structure**
- ML Detection: `https://neuroshield.com/ml`
- VirusTotal Detection: `https://neuroshield.com/vt`
- Main Site: `https://neuroshield.com`

**Option 3: Separate Domains**
- ML Detection: `https://neuroshield.ai`
- VirusTotal Detection: `https://neuroshield.io`

---

## 🎨 Branding Consistency

### Brand Name
- **Primary:** NeuroShield
- **Tagline ML:** AI-Powered Malware Detection
- **Tagline VT:** Threat Intelligence Platform

### Copyright
- **Format:** `© 2025 NeuroShield. All Rights Reserved by F.J.G.`

### Navigation Links
Both applications now use:
- Home
- ML Detection / Dynamic Analysis
- Awareness
- About

---

## 📋 Nginx Configuration Example

For production deployment with neuroshield domain:

```nginx
# ML Application
server {
    listen 80;
    server_name ml.neuroshield.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# VirusTotal Application  
server {
    listen 80;
    server_name vt.neuroshield.com;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Main landing page (optional)
server {
    listen 80;
    server_name neuroshield.com www.neuroshield.com;
    
    location / {
        # Serve main landing page or redirect
        return 301 https://neuroshield.com$request_uri;
    }
}
```

---

## 🔒 SSL/TLS Configuration

For HTTPS with Let's Encrypt:

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificates for all subdomains
sudo certbot --nginx -d neuroshield.com -d www.neuroshield.com
sudo certbot --nginx -d ml.neuroshield.com
sudo certbot --nginx -d vt.neuroshield.com

# Auto-renewal test
sudo certbot renew --dry-run
```

---

## 🎯 DNS Configuration

For custom domain, configure DNS records:

```
Type    Name    Value                   TTL
A       @       <your-server-ip>        3600
A       ml      <your-server-ip>        3600
A       vt      <your-server-ip>        3600
CNAME   www     neuroshield.com         3600
```

---

## ✅ Verification

All branding has been updated and tested:

- ✅ Page titles use "NeuroShield"
- ✅ Headers and navigation updated
- ✅ Footers show correct copyright
- ✅ Chart titles branded correctly
- ✅ No hardcoded IP addresses in navigation
- ✅ Consistent naming across all templates
- ✅ Professional appearance

---

## 📱 Next Steps

### Optional Branding Enhancements

1. **Add Favicon**
   - Create `static/favicon.ico`
   - Add to HTML: `<link rel="icon" href="/static/favicon.ico">`

2. **Add Logo**
   - Create NeuroShield logo
   - Add to header in templates
   - Use in navigation bar

3. **Custom Domain**
   - Register neuroshield.com domain
   - Configure DNS records
   - Set up SSL certificates
   - Update Nginx configuration

4. **Social Media**
   - Create social media accounts with @neuroshield
   - Add social links to footer
   - Create og:image meta tags

5. **Brand Guidelines**
   - Define color scheme
   - Choose official fonts
   - Create logo variations
   - Document brand voice

---

## 🎨 Current Brand Colors

Based on existing templates:

- **Primary:** `#2534ff` (Blue)
- **Accent:** `#ff5733` (Red/Orange)
- **Success:** `#33e7ff` (Cyan)
- **Dark Mode Background:** `#001637` (Dark Blue)
- **Dark Mode Header:** `#02102b` (Very Dark Blue)

---

**Updated By:** Automated Branding Update  
**Date:** October 7, 2025  
**Status:** ✅ All templates updated with NeuroShield branding