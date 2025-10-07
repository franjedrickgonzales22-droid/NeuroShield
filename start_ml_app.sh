#!/bin/bash
# Production startup script for ML-based Malware Detection

echo "🚀 Starting NeuroShield ML-based Malware Detection..."
echo ""

cd /workspace/ML_based_detectionn

# Check if model exists
if [ ! -f "ML_model/malwareclassifier-V2.pkl" ]; then
    echo "⚠️  Warning: ML model not found!"
    echo "   Run: python train_model.py --create-sample"
    echo ""
fi

# Start with Gunicorn (production WSGI server)
echo "Starting Gunicorn on 0.0.0.0:5000..."
echo "Access the application at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

~/.local/bin/gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    app_production:app