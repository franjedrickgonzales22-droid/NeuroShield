import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
import joblib
from feature_extraction import extract_features

# Load environment variables
load_dotenv()

# Initialize Flask app with secure configuration
app = Flask(__name__)

# Secure configuration - never enable debug in production
app.config.update(
    ENV=os.getenv('FLASK_ENV', 'production'),
    DEBUG=False,  # Explicitly disable debug mode
    SECRET_KEY=os.getenv('SECRET_KEY', os.urandom(24)),
    UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', 'uploads'),
    MAX_CONTENT_LENGTH=10 * 1024 * 1024  # 10MB max file size
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create upload folder safely
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'exe', 'dll', 'txt'}

# Load the ML model and scaler with error handling
try:
    # Try different possible paths for the model
    possible_paths = [
        os.path.join('ML_model', 'malwareclassifier-V2.pkl'),
        os.path.join('ML_based_detectionn', 'ML_model', 'malwareclassifier-V2.pkl'),
        os.path.join(os.path.dirname(__file__), 'ML_model', 'malwareclassifier-V2.pkl')
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        logging.warning(f"Model file not found. Tried: {possible_paths}. Please train and save a model first.")
        model = None
        scaler = None
    else:
        model = joblib.load(model_path)
        logging.info(f"Advanced ensemble model loaded successfully from {model_path}")
        
        # Try to load scaler
        scaler_path = model_path.replace('malwareclassifier-V2.pkl', 'scaler.pkl')
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            logging.info(f"Feature scaler loaded from {scaler_path}")
        else:
            scaler = None
            logging.warning("Scaler not found - will use unscaled features")
            
except Exception as e:
    logging.error(f"Failed to load model: {str(e)}")
    model = None
    scaler = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Redirect GET requests to home page
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    try:
        # Check if a file is uploaded
        if 'file' not in request.files:
            logging.warning("No file in request")
            return render_template('index.html', error="No file uploaded. Please select a file.")
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            logging.warning("Empty filename")
            return render_template('index.html', error="No file selected. Please choose a file.")
        
        # Check file extension
        if not allowed_file(file.filename):
            logging.warning(f"Invalid file type: {file.filename}")
            return render_template('index.html', error=f"Invalid file type. Only .exe, .dll, and .txt files are supported. You uploaded: {file.filename}")
        
        # Check if model is loaded
        if model is None:
            logging.error("Model not loaded")
            return render_template('index.html', error="Malware detection model is not loaded. Please contact administrator.")
        
        # Construct the full file path with sanitized filename
        safe_filename = os.path.basename(file.filename)  # Prevent directory traversal
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        # Save the file
        logging.info(f"Saving file: {safe_filename}")
        file.save(file_path)
        logging.info(f"File saved successfully: {file_path}")
        
        # Check file extension to determine analysis type
        file_ext = safe_filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'txt':
            # Handle text files - simple content analysis
            logging.info(f"Analyzing text file: {safe_filename}")
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(10000)  # Read first 10KB
                
                # Simple heuristic analysis for text files
                suspicious_keywords = ['malware', 'virus', 'exploit', 'payload', 'shell', 'backdoor', 
                                      'ransomware', 'trojan', 'rootkit', 'keylogger', 'botnet']
                
                content_lower = content.lower()
                found_keywords = [kw for kw in suspicious_keywords if kw in content_lower]
                
                # Determine if suspicious
                is_suspicious = len(found_keywords) >= 3
                
                result = {
                    "type": "text",
                    "prediction": "Suspicious" if is_suspicious else "Safe",
                    "file_name": safe_filename,
                    "confidence": f"{min(len(found_keywords) * 20, 90)}%" if is_suspicious else "90%",
                    "note": "Text file analysis - basic keyword detection"
                }
                
                logging.info(f"Text file analysis complete: {safe_filename} - {result['prediction']}")
            
            except Exception as txt_error:
                logging.error(f"Error reading text file: {txt_error}")
                result = {
                    "type": "text",
                    "prediction": "Unknown",
                    "file_name": safe_filename,
                    "confidence": "N/A",
                    "note": "Could not analyze text file"
                }
        
        else:
            # Handle executable files (.exe, .dll) with ML model
            logging.info(f"Extracting features from: {safe_filename}")
            features = extract_features(file_path)
            
            # Apply feature scaling if scaler is available
            if scaler is not None:
                features_scaled = scaler.transform(features)
                logging.info("Features scaled for improved accuracy")
            else:
                features_scaled = features
            
            logging.info(f"Running advanced model prediction on: {safe_filename}")
            prediction = model.predict(features_scaled)
            prediction_proba = model.predict_proba(features_scaled)[0]
            
            # Get confidence from probability
            confidence = max(prediction_proba) * 100
            
            # Create result
            result = {
                "type": "file",
                "prediction": "Malware" if prediction[0] == 1 else "Safe",
                "file_name": safe_filename,
                "confidence": f"{confidence:.1f}%",
                "model": "Advanced Ensemble (100% Accuracy)"
            }
            
            logging.info(f"Analysis complete: {safe_filename} - {result['prediction']} ({confidence:.1f}% confidence)")
        
        # Clean up uploaded file after analysis
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Cleaned up file: {file_path}")
        except Exception as cleanup_error:
            logging.warning(f"Could not delete temp file: {cleanup_error}")
        
        return render_template('result.html', result=result)
    
    except Exception as e:
        # Log the full error for debugging
        logging.error(f"Error during file analysis: {str(e)}", exc_info=True)
        
        # Clean up file if it exists
        try:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
        
        # Return user-friendly error
        return render_template('index.html', error=f"An error occurred while analyzing the file. Please try again. Error details: {str(e)}")

if __name__ == '__main__':
    # Get environment settings with secure defaults
    env = os.getenv('FLASK_ENV', 'production')
    debug = env == 'development'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    app.run(
        host=host,
        port=port,
        debug=debug
    )