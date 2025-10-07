# NeuroShield

Malware detection toolkit combining:

- ML-based static PE analysis (`ML_based_detectionn`)
- VirusTotal-assisted scanning (`Virus_total_based`)

## Quickstart

1. Create and activate a virtualenv (Python 3.10+ recommended)
2. Install dependencies for the ML app:
   ```bash
   pip install -r ML_based_detectionn/requirements.txt
   ```
3. Optional: set environment variables in a `.env` file:
   ```
   FLASK_ENV=development
   FLASK_HOST=127.0.0.1
   FLASK_PORT=5001
   MODEL_PATH=ML_model/malwareclassifier-V2.pkl
   VIRUSTOTAL_API_KEY=...  # for VirusTotal app
   ```
4. Run the ML-based app:
   ```bash
   python ML_based_detectionn/app.py
   ```
5. Run the VirusTotal-based app (requires `VIRUSTOTAL_API_KEY`):
   ```bash
   python Virus_total_based/app.py
   ```

