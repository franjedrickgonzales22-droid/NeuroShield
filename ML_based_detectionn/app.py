import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import joblib

# Load environment variables
load_dotenv()

# Initialize Flask app with secure configuration
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
)

# Secure configuration - never enable debug in production
app.config.update(
    ENV=os.getenv('FLASK_ENV', 'production'),
    DEBUG=False,  # Explicitly disable debug mode
    SECRET_KEY=os.getenv('SECRET_KEY', os.urandom(24)),
    UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', 'uploads'),
    MAX_CONTENT_LENGTH=10 * 1024 * 1024  # 10MB max file size
)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {"exe", "dll"}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create upload folder safely
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the ML model with error handling
model = None
try:
    model_path = os.getenv('MODEL_PATH', os.path.join('ML_model', 'malwareclassifier-V2.pkl'))
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        logging.info("Model loaded successfully")
    else:
        logging.warning(f"Model file not found at '{model_path}'. Running without ML predictions.")
except Exception as e:
    logging.error(f"Failed to load model: {str(e)}")
    # Continue without model so that the app can still serve the UI

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Provide safe defaults for template variables
    return render_template('index.html', recent_results=[])

@app.route('/analyze', methods=['POST'])
def analyze():
    # Ensure a file was uploaded
    if 'file' not in request.files:
        return render_template('index.html', error="No file uploaded."), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return render_template('index.html', error="Unsupported file type."), 400

    if model is None:
        return render_template('index.html', error="Model is not available on the server."), 503

    # Construct the full file path safely
    safe_name = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

    # Save the file
    file.save(file_path)

    # Use the model for prediction
    try:
        # Lazy import to avoid heavy deps unless needed
        try:
            from .feature_extraction import extract_features as _extract_features  # type: ignore
        except Exception:
            try:
                from feature_extraction import extract_features as _extract_features  # type: ignore
            except Exception:
                return render_template('index.html', error="Feature extraction module not available."), 500

        features = _extract_features(file_path)
        prediction = model.predict(features)
        result = {
            "type": "file",
            "prediction": "Malware" if int(prediction[0]) == 1 else "Safe",
            "file_name": safe_name
        }
        return render_template('result.html', result=result)
    except Exception as e:
        logging.exception("Error during feature extraction or prediction")
        return render_template('index.html', error=f"Analysis failed: {str(e)}"), 500

if __name__ == '__main__':
    # Get environment settings with secure defaults
    env = os.getenv('FLASK_ENV', 'production')
    debug = env == 'development'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    # Default to 5001 to avoid clashing with the VirusTotal app
    port = int(os.getenv('FLASK_PORT', 5001))

    app.run(
        host=host,
        port=port,
        debug=debug
    )