import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, render_template
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

# Load the ML model with error handling
try:
    model = joblib.load('ML_model/malwareclassifier-V2.pkl')
    logging.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Failed to load model: {str(e)}")
    raise RuntimeError("Application failed to initialize - model not loaded")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Check if a file is uploaded
    if 'file' in request.files:
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return render_template('index.html', error="Unsupported file type.")
        
        # Construct the full file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Save the file
        file.save(file_path)

        # Use the model for prediction if the file is `.exe` or `.dll`
        if allowed_file(file.filename):
            features = extract_features(file_path)  # Your feature extraction function
            prediction = model.predict(features)     # Predict using your model
            result = {
                "type": "file",
                "prediction": "Malware" if prediction[0] == 1 else "Safe",
                "file_name": file.filename
            }

        return render_template('result.html', result=result)

    return render_template('index.html', error="No file uploaded.")

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ...existing code...

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