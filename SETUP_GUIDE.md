# NeuroShield Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- (For VirusTotal app) A VirusTotal API key - Get one free at https://www.virustotal.com/gui/join-us

## Installation

### 1. ML-Based Detection Application

#### Step 1: Install Dependencies

```bash
cd ML_based_detectionn
pip install -r requirements.txt
```

#### Step 2: Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your preferred settings (optional):
```env
FLASK_ENV=production
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
```

#### Step 3: Prepare ML Model

**IMPORTANT**: You need a trained machine learning model to use this application.

The model should:
- Accept 23 features from PE files
- Output binary classification (0 = Safe, 1 = Malware)
- Be saved using `joblib` in pickle format

Place your model at:
```
ML_based_detectionn/ML_model/malwareclassifier-V2.pkl
```

If you don't have a model yet:
- The application will start but show a warning
- File analysis will return an error until a model is provided
- You can train your own model using the provided feature extraction function

#### Step 4: Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

### 2. VirusTotal-Based Detection Application

#### Step 1: Install Dependencies

```bash
cd Virus_total_based
pip install -r requirements.txt
```

#### Step 2: Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file and add your VirusTotal API key:
```env
VIRUSTOTAL_API_KEY=your-actual-virustotal-api-key-here
FLASK_SECRET_KEY=your-random-secret-key-here
```

**Getting a VirusTotal API Key:**
1. Visit https://www.virustotal.com/gui/join-us
2. Create a free account
3. Navigate to your profile settings
4. Copy your API key from the API Key section

#### Step 3: Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Testing

### Run Complete Test Suite

From the workspace root:
```bash
python test_complete_app.py
```

This will verify:
- ✅ File structure is correct
- ✅ All dependencies are installed
- ✅ Both applications can start successfully
- ✅ Configuration is secure

### Verify Accuracy

```bash
python verify_accuracy.py
```

This will verify:
- ✅ Feature extraction produces consistent results
- ✅ All 23 features are extracted correctly
- ✅ No missing or invalid values
- ✅ Application configuration is secure

---

## Usage

### ML-Based Detection

1. Open `http://127.0.0.1:5000` in your browser
2. Upload a `.exe` or `.dll` file (max 10MB)
3. Click "Analyze"
4. View the results (Malware or Safe)

**Supported File Types:**
- Windows PE executables (`.exe`)
- Windows DLL files (`.dll`)

### VirusTotal Detection

1. Open `http://127.0.0.1:5000` in your browser
2. Choose one of the following options:
   - **Upload a file** (max 32MB)
   - **Enter a URL** to scan
   - **Enter a file hash** (MD5, SHA-1, or SHA-256)
   - **Submit XML data** for automated workflows
3. Click "Analyze"
4. View detailed scan results from multiple antivirus engines

---

## Features Extracted for ML Detection

The application extracts 23 features from PE files:

1. MajorLinkerVersion
2. MinorOperatingSystemVersion
3. MajorSubsystemVersion
4. SizeOfStackReserve
5. TimeDateStamp
6. MajorOperatingSystemVersion
7. Characteristics
8. ImageBase
9. Subsystem
10. MinorImageVersion
11. MinorSubsystemVersion
12. SizeOfInitializedData
13. DllCharacteristics
14. DirectoryEntryExport
15. ImageDirectoryEntryExport
16. CheckSum
17. DirectoryEntryImportSize
18. SectionMaxChar
19. MajorImageVersion
20. AddressOfEntryPoint
21. SectionMinEntropy
22. SizeOfHeaders
23. SectionMinVirtualsize

---

## Troubleshooting

### ML App: "Model not loaded" error

**Problem:** The ML model file is missing.

**Solution:**
1. Train a machine learning model using your dataset
2. Save it using `joblib.dump(model, 'malwareclassifier-V2.pkl')`
3. Place it in `ML_based_detectionn/ML_model/`

### VirusTotal App: "VIRUSTOTAL_API_KEY environment variable is not set"

**Problem:** API key is not configured.

**Solution:**
1. Get a free API key from https://www.virustotal.com
2. Add it to your `.env` file
3. Restart the application

### "Port 5000 already in use"

**Problem:** Another application is using port 5000.

**Solution:**
1. Change the port in your `.env` file:
   ```env
   FLASK_PORT=5001
   ```
2. Or stop the other application using port 5000

### Import Errors

**Problem:** Missing dependencies.

**Solution:**
```bash
pip install -r requirements.txt
```

---

## Security Considerations

### Both Applications:
- ✅ Debug mode disabled in production
- ✅ File size limits enforced
- ✅ Input validation on all user inputs
- ✅ Secure file handling with cleanup
- ✅ Secret key configuration for sessions

### VirusTotal App:
- ✅ XML parsing uses defusedxml to prevent XXE attacks
- ✅ URL validation to prevent SSRF attacks
- ✅ Temporary file cleanup after processing
- ✅ Request timeouts to prevent hanging connections

---

## Running in Production

### Important Security Steps:

1. **Generate a strong secret key:**
   ```python
   import os
   print(os.urandom(24).hex())
   ```
   Add this to your `.env` file

2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 127.0.0.1:5000 app:app
   ```

3. **Use environment variables** instead of `.env` files in production

4. **Set up HTTPS** using a reverse proxy (nginx/Apache)

5. **Implement rate limiting** to prevent abuse

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test output: `python test_complete_app.py`
3. Check application logs for detailed error messages

---

## License

All Rights Reserved by B & L.

Developed as part of an INSA project.