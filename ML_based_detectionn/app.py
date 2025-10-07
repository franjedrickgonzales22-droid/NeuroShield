import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import joblib
try:
    # When imported as a package
    from .feature_extraction import extract_features  # type: ignore
except Exception:  # pragma: no cover - fallback for script execution
    # When executed directly as a script
    from feature_extraction import extract_features  # type: ignore

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

# Allowed file extensions for static PE analysis
ALLOWED_EXTENSIONS = {"exe", "dll"}

# Resolve model path from env with sensible default
MODEL_PATH = os.getenv('MODEL_PATH', os.path.join('ML_model', 'malwareclassifier-V2.pkl'))

# Load the ML model with error handling (optional in dev)
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        logging.info("Model loaded successfully")
    except Exception as e:
        logging.error(f"Failed to load model from {MODEL_PATH}: {str(e)}")
else:
    logging.warning(f"Model path not found: {MODEL_PATH}. The app will run but predictions are disabled.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Validate file presence
    if 'file' not in request.files:
        flash('No file part in the request', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    # Validate filename and extension
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Unsupported file type. Only .exe and .dll are allowed.', 'error')
        return redirect(url_for('index'))

    # Save the file securely
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(file_path)
    except Exception as e:
        logging.error(f"Failed to save uploaded file: {str(e)}")
        flash('Failed to save the uploaded file.', 'error')
        return redirect(url_for('index'))

    # Ensure the model is available
    if model is None:
        flash('ML model is not configured on the server. Please contact the administrator.', 'error')
        return redirect(url_for('index'))

    # Extract features and predict
    try:
        features = extract_features(file_path)
        prediction = model.predict(features)
    except Exception as e:
        logging.error(f"Analysis failed: {str(e)}")
        flash('Failed to analyze the file.', 'error')
        return redirect(url_for('index'))

    result = {
        "type": "file",
        "prediction": "Malware" if int(prediction[0]) == 1 else "Safe",
        "file_name": filename
    }

    return render_template('result.html', result=result)

if __name__ == '__main__':
    # Get environment settings with secure defaults
    env = os.getenv('FLASK_ENV', 'production')
    debug = env == 'development'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    # Default to 5001 for the ML app to avoid port conflicts
    port = int(os.getenv('FLASK_PORT', 5001))

    app.run(
        host=host,
        port=port,
        debug=debug
    )