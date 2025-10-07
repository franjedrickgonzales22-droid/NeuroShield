#!/bin/bash
# Production startup script for VirusTotal-based Malware Detection

echo "🚀 Starting NeuroShield VirusTotal-based Detection..."
echo ""

cd /workspace/Virus_total_based

# Check if API key is configured
if grep -q "your-api-key-here-replace-this" .env 2>/dev/null; then
    echo "⚠️  Warning: VirusTotal API key not configured!"
    echo "   Edit .env and add your API key from https://www.virustotal.com/gui/my-apikey"
    echo ""
fi

# Start with Gunicorn (production WSGI server)
echo "Starting Gunicorn on 0.0.0.0:5001..."
echo "Access the application at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

~/.local/bin/gunicorn \
    --bind 0.0.0.0:5001 \
    --workers 4 \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    app_production:app