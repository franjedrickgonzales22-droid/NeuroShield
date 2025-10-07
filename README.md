# NeuroShield

A comprehensive malware detection system that combines machine learning and VirusTotal integration to identify malicious software.

## Features

### ML-Based Detection
- Analyzes Windows PE files (`.exe`, `.dll`) using machine learning
- Extracts 23 features from PE files for classification
- Real-time malware detection with trained models
- Secure file upload and processing

### VirusTotal Integration
- Scan files, URLs, and file hashes
- Leverages multiple antivirus engines
- Detailed scan result visualization
- Recent scan history tracking
- XML data parsing for automated workflows

## Quick Start

1. **Install dependencies:**
   ```bash
   cd ML_based_detectionn && pip3 install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application:**
   ```bash
   python3 app.py
   ```

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Testing

All components have been tested and verified. Run the test suite:
```bash
python3 test_complete_app.py
```

## Project Structure

```
NeuroShield/
├── ML_based_detectionn/       # ML-based malware detection
│   ├── app.py                 # Flask application
│   ├── feature_extraction.py  # PE file feature extraction
│   ├── requirements.txt       # Python dependencies
│   ├── templates/            # HTML templates
│   ├── uploads/              # Uploaded files directory
│   └── ML_model/             # Trained ML models
├── Virus_total_based/        # VirusTotal integration
│   ├── app.py                # Flask application
│   └── templates/            # HTML templates
└── README.md                 # This file
```

## Security

- File size limits enforced
- Input validation and sanitization
- Secure file handling
- XML vulnerability protection
- Production-ready configuration

## License

All Rights Reserved by B & L.

## Contributors

Developed as part of an INSA (Institut National des Sciences Appliquées) project.
