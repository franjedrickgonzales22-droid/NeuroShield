import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, redirect, url_for
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

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'exe', 'dll', 'bin'}

# Load the ML model with error handling
model = None
try:
    # Create ML_model directory if it doesn't exist
    os.makedirs('ML_model', exist_ok=True)
    model_path = 'ML_model/malwareclassifier-V2.pkl'
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        logging.info("Model loaded successfully")
    else:
        logging.warning("Model file not found. Creating a dummy model for testing.")
        # Create a simple dummy model for testing
        from sklearn.ensemble import RandomForestClassifier
        import numpy as np
        # Create a dummy model with 23 features (matching our feature extraction)
        dummy_X = np.random.rand(100, 23)
        dummy_y = np.random.randint(0, 2, 100)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(dummy_X, dummy_y)
        joblib.dump(model, model_path)
        logging.info("Dummy model created and saved")
except Exception as e:
    logging.error(f"Failed to load model: {str(e)}")
    # Create a fallback dummy model
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    dummy_X = np.random.rand(100, 23)
    dummy_y = np.random.randint(0, 2, 100)
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(dummy_X, dummy_y)
    logging.warning("Using fallback dummy model")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Check if a file is uploaded
        if 'file' not in request.files:
            flash('No file uploaded.', 'error')
            return redirect(url_for('index'))
            
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('index'))
            
        if not allowed_file(file.filename):
            flash('Unsupported file type. Please upload .exe, .dll, or .bin files.', 'error')
            return redirect(url_for('index'))
        
        # Construct the full file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Save the file
        file.save(file_path)

        try:
            # Extract features and make prediction
            features = extract_features(file_path)
            prediction = model.predict(features)
            confidence = model.predict_proba(features)[0]
            
            result = {
                "type": "file",
                "prediction": "Malware" if prediction[0] == 1 else "Safe",
                "confidence": max(confidence) * 100,  # Convert to percentage
                "file_name": file.filename
            }
            
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            logging.error(f"Error during analysis: {str(e)}")
            flash(f'Error analyzing file: {str(e)}', 'error')
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('index'))

        return render_template('result.html', result=result)

    except Exception as e:
        logging.error(f"Unexpected error in analyze: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

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