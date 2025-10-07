#!/bin/bash

# NeuroShield Malware Detection - Quick Start Script
# This script sets up and runs both applications

echo "🚀 NeuroShield Malware Detection - Quick Start"
echo "=============================================="

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port $port is already in use. Trying to kill existing process..."
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# Function to install dependencies
install_deps() {
    local app_dir=$1
    echo "📦 Installing dependencies for $app_dir..."
    cd "$app_dir"
    pip3 install -r requirements.txt
    cd - > /dev/null
}

# Function to start application
start_app() {
    local app_dir=$1
    local port=$2
    local app_name=$3
    
    echo "🚀 Starting $app_name on port $port..."
    cd "$app_dir"
    FLASK_PORT=$port python3 app.py &
    local pid=$!
    echo "✅ $app_name started with PID: $pid"
    cd - > /dev/null
    echo $pid
}

# Main execution
echo "🔧 Setting up applications..."

# Check and kill existing processes
check_port 5001
check_port 5002

# Install dependencies
install_deps "ML_based_detectionn"
install_deps "Virus_total_based"

# Start applications
ml_pid=$(start_app "ML_based_detectionn" 5001 "ML Detection")
vt_pid=$(start_app "Virus_total_based" 5002 "VirusTotal Detection")

# Wait for applications to start
echo "⏳ Waiting for applications to start..."
sleep 5

# Test applications
echo "🧪 Testing applications..."

# Test ML app
if curl -s http://127.0.0.1:5001/ > /dev/null; then
    echo "✅ ML Detection app is running at http://127.0.0.1:5001"
else
    echo "❌ ML Detection app failed to start"
fi

# Test VirusTotal app
if curl -s http://127.0.0.1:5002/ > /dev/null; then
    echo "✅ VirusTotal Detection app is running at http://127.0.0.1:5002"
else
    echo "❌ VirusTotal Detection app failed to start"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📱 Access your applications:"
echo "   ML Detection: http://127.0.0.1:5001"
echo "   VirusTotal Detection: http://127.0.0.1:5002"
echo ""
echo "🛑 To stop applications, run:"
echo "   kill $ml_pid $vt_pid"
echo ""
echo "📚 For detailed usage instructions, see SETUP_AND_USAGE.md"
echo "🧪 To run tests, execute: python3 test_applications.py"