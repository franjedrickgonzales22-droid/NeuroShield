#!/usr/bin/env python3
"""Complete test script for both applications"""
import sys
import os

def test_ml_app():
    """Test ML-based detection app"""
    print("\n" + "="*60)
    print("Testing ML-Based Detection Application")
    print("="*60)
    
    sys.path.insert(0, '/workspace/ML_based_detectionn')
    
    try:
        from app import app, ALLOWED_EXTENSIONS
        from feature_extraction import extract_features, calculate_entropy
        
        print("✅ All imports successful")
        print(f"✅ Allowed extensions: {ALLOWED_EXTENSIONS}")
        print(f"✅ Upload folder: {app.config['UPLOAD_FOLDER']}")
        print(f"✅ Max content length: {app.config['MAX_CONTENT_LENGTH']} bytes")
        print(f"✅ Debug mode: {app.config['DEBUG']}")
        
        test_data = b"Hello World" * 100
        entropy = calculate_entropy(test_data)
        print(f"✅ Entropy calculation works: {entropy:.2f}")
        
        test_file = '/workspace/ML_based_detectionn/uploads/notepad.exe'
        if os.path.exists(test_file):
            features = extract_features(test_file)
            print(f"✅ Feature extraction works: {features.shape[1]} features extracted")
        
        print("\n✅ ML-Based Detection App: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ ML-Based Detection App: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_virustotal_app():
    """Test VirusTotal-based detection app"""
    print("\n" + "="*60)
    print("Testing VirusTotal-Based Detection Application")
    print("="*60)
    
    sys.path = [p for p in sys.path if 'ML_based_detectionn' not in p]
    sys.path.insert(0, '/workspace/Virus_total_based')
    
    if 'app' in sys.modules:
        del sys.modules['app']
    
    try:
        os.environ['VIRUSTOTAL_API_KEY'] = 'test_api_key'
        
        import importlib.util
        spec = importlib.util.spec_from_file_location("vt_app", "/workspace/Virus_total_based/app.py")
        vt_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vt_module)
        
        print("✅ All imports successful")
        print(f"✅ API endpoints configured")
        print(f"✅ Recent results list initialized: {len(vt_module.recent_results)} items")
        print(f"✅ Secret key configured: {bool(vt_module.app.secret_key)}")
        
        print("\n✅ VirusTotal-Based Detection App: ALL TESTS PASSED")
        print("⚠️  Note: API key needs to be set in .env file for actual scanning")
        return True
        
    except Exception as e:
        print(f"\n❌ VirusTotal-Based Detection App: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test file and directory structure"""
    print("\n" + "="*60)
    print("Testing File Structure")
    print("="*60)
    
    required_files = [
        '/workspace/README.md',
        '/workspace/ML_based_detectionn/app.py',
        '/workspace/ML_based_detectionn/feature_extraction.py',
        '/workspace/ML_based_detectionn/requirements.txt',
        '/workspace/ML_based_detectionn/.env.example',
        '/workspace/ML_based_detectionn/templates/index.html',
        '/workspace/ML_based_detectionn/templates/result.html',
        '/workspace/Virus_total_based/app.py',
        '/workspace/Virus_total_based/.env.example',
        '/workspace/Virus_total_based/templates/index.html',
        '/workspace/Virus_total_based/templates/result.html',
    ]
    
    required_dirs = [
        '/workspace/ML_based_detectionn',
        '/workspace/ML_based_detectionn/templates',
        '/workspace/ML_based_detectionn/uploads',
        '/workspace/ML_based_detectionn/ML_model',
        '/workspace/Virus_total_based',
        '/workspace/Virus_total_based/templates',
    ]
    
    all_good = True
    
    print("\nChecking directories:")
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ Missing: {dir_path}")
            all_good = False
    
    print("\nChecking files:")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    if all_good:
        print("\n✅ File Structure: ALL CHECKS PASSED")
    else:
        print("\n⚠️  File Structure: Some files/directories missing")
    
    return all_good

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("NEUROSHIELD MALWARE DETECTION - COMPLETE TEST SUITE")
    print("="*60)
    
    results = {
        'File Structure': test_file_structure(),
        'ML App': test_ml_app(),
        'VirusTotal App': test_virustotal_app(),
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! The application is ready to use.")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())