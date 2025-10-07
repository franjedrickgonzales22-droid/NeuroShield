# NeuroShield Malware Detection System

## Overview

NeuroShield is a comprehensive malware detection system that provides two different approaches to malware analysis:

1. **ML-based Detection** - Uses machine learning models to analyze PE files
2. **VirusTotal-based Detection** - Integrates with VirusTotal API for cloud-based analysis

## Features

### ML-based Detection
- ✅ PE file analysis using 23 extracted features
- ✅ Random Forest classifier for malware detection
- ✅ Confidence scoring for predictions
- ✅ Support for .exe, .dll, and .bin files
- ✅ Automatic model creation if none exists
- ✅ Comprehensive error handling

### VirusTotal-based Detection
- ✅ File hash analysis
- ✅ URL analysis
- ✅ File upload and scanning
- ✅ XML data parsing
- ✅ Real-time scan results
- ✅ Graceful handling of missing API keys

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # Navigate to the project directory
   cd /workspace
   ```

2. **Install ML-based detection dependencies**
   ```bash
   cd ML_based_detectionn
   pip3 install -r requirements.txt
   ```

3. **Install VirusTotal-based detection dependencies**
   ```bash
   cd ../Virus_total_based
   pip3 install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   # For VirusTotal API (optional)
   export VIRUSTOTAL_API_KEY="your_api_key_here"
   
   # For Flask configuration (optional)
   export FLASK_ENV="development"
   export FLASK_PORT="5000"
   ```

## Usage

### Running the Applications

#### ML-based Detection (Port 5001)
```bash
cd ML_based_detectionn
python3 app.py
```
Access at: http://127.0.0.1:5001

#### VirusTotal-based Detection (Port 5002)
```bash
cd Virus_total_based
python3 app.py
```
Access at: http://127.0.0.1:5002

### Using the Web Interface

1. **ML-based Detection**
   - Upload a PE file (.exe, .dll, .bin)
   - View analysis results with confidence scores
   - Results show "Malware" or "Safe" classification

2. **VirusTotal-based Detection**
   - Upload a file for scanning
   - Enter a file hash for lookup
   - Enter a URL for analysis
   - View detailed scan results from multiple engines

### API Usage

#### ML-based Detection API
```bash
# Upload file for analysis
curl -X POST -F "file=@sample.exe" http://127.0.0.1:5001/analyze
```

#### VirusTotal-based Detection API
```bash
# Analyze file hash
curl -X POST -d "file_hash=abc123" http://127.0.0.1:5002/analyze

# Analyze URL
curl -X POST -d "url=https://example.com" http://127.0.0.1:5002/analyze
```

## Testing

### Automated Testing
Run the comprehensive test suite:
```bash
cd /workspace
python3 test_applications.py
```

### Manual Testing
1. Start both applications
2. Test file uploads with different file types
3. Test error handling with invalid inputs
4. Verify UI responsiveness and dark mode toggle

## Configuration

### ML-based Detection Configuration
- **Model Path**: `ML_model/malwareclassifier-V2.pkl`
- **Upload Folder**: `uploads/`
- **Max File Size**: 10MB
- **Allowed Extensions**: .exe, .dll, .bin

### VirusTotal-based Detection Configuration
- **API Key**: Set via `VIRUSTOTAL_API_KEY` environment variable
- **Max File Size**: 32MB
- **Timeout**: 30 seconds for API calls

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port using environment variables
   - Kill existing processes using the port

2. **Model not found**
   - The system will automatically create a dummy model
   - For production, replace with a trained model

3. **VirusTotal API errors**
   - Ensure API key is set correctly
   - Check API quota and rate limits
   - Verify internet connectivity

4. **File upload errors**
   - Check file size limits
   - Verify file format is supported
   - Ensure proper permissions

### Error Handling

Both applications include comprehensive error handling:
- Invalid file types are rejected with clear messages
- Missing API keys are handled gracefully
- Network timeouts are managed appropriately
- File processing errors are logged and reported

## Security Features

- ✅ Input validation and sanitization
- ✅ File size limits
- ✅ Secure file handling with temporary directories
- ✅ XML parsing with defusedxml library
- ✅ Environment variable configuration
- ✅ Proper error logging

## Performance

- **ML Detection**: Fast analysis using pre-trained models
- **VirusTotal Detection**: Depends on API response times
- **File Processing**: Optimized for PE file analysis
- **Memory Usage**: Efficient with automatic cleanup

## Development

### Adding New Features
1. Follow the existing code structure
2. Add comprehensive error handling
3. Update tests accordingly
4. Document new functionality

### Code Quality
- All code includes proper error handling
- Logging is implemented throughout
- Input validation is comprehensive
- Security best practices are followed

## License

This project is for educational and research purposes. Please ensure compliance with VirusTotal's terms of service when using their API.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the error logs
3. Run the test suite to identify problems
4. Ensure all dependencies are properly installed

---

**Note**: This system is designed for educational and research purposes. Always use additional security measures in production environments.