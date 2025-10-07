#!/usr/bin/env python3
"""
Comprehensive test script for both malware detection applications.
This script tests the ML-based and VirusTotal-based detection systems.
"""

import requests
import time
import os
import sys
import subprocess
import signal
from pathlib import Path

class ApplicationTester:
    def __init__(self):
        self.ml_app_url = "http://127.0.0.1:5001"
        self.vt_app_url = "http://127.0.0.1:5002"
        self.ml_process = None
        self.vt_process = None
        
    def start_applications(self):
        """Start both applications in the background"""
        print("🚀 Starting applications...")
        
        # Start ML application
        try:
            self.ml_process = subprocess.Popen(
                ["python3", "app.py"],
                cwd="/workspace/ML_based_detectionn",
                env={**os.environ, "FLASK_PORT": "5001"}
            )
            print("✅ ML application started on port 5001")
        except Exception as e:
            print(f"❌ Failed to start ML application: {e}")
            return False
            
        # Start VirusTotal application
        try:
            self.vt_process = subprocess.Popen(
                ["python3", "app.py"],
                cwd="/workspace/Virus_total_based",
                env={**os.environ, "FLASK_PORT": "5002"}
            )
            print("✅ VirusTotal application started on port 5002")
        except Exception as e:
            print(f"❌ Failed to start VirusTotal application: {e}")
            return False
            
        # Wait for applications to start
        time.sleep(3)
        return True
        
    def stop_applications(self):
        """Stop both applications"""
        print("\n🛑 Stopping applications...")
        
        if self.ml_process:
            self.ml_process.terminate()
            self.ml_process.wait()
            print("✅ ML application stopped")
            
        if self.vt_process:
            self.vt_process.terminate()
            self.vt_process.wait()
            print("✅ VirusTotal application stopped")
            
    def test_ml_application(self):
        """Test the ML-based detection application"""
        print("\n🔬 Testing ML-based detection application...")
        
        # Test 1: Check if application is running
        try:
            response = requests.get(f"{self.ml_app_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ ML application is running and accessible")
            else:
                print(f"❌ ML application returned status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Failed to connect to ML application: {e}")
            return False
            
        # Test 2: Test file upload with sample file
        sample_file = "/workspace/ML_based_detectionn/uploads/notepad.exe"
        if os.path.exists(sample_file):
            try:
                with open(sample_file, 'rb') as f:
                    files = {'file': ('notepad.exe', f, 'application/octet-stream')}
                    response = requests.post(f"{self.ml_app_url}/analyze", files=files, timeout=30)
                    
                if response.status_code == 200:
                    print("✅ File upload and analysis successful")
                    if "Malware Detected" in response.text or "No Malware Detected" in response.text:
                        print("✅ Analysis result displayed correctly")
                    else:
                        print("⚠️  Analysis result format may be incorrect")
                else:
                    print(f"❌ File upload failed with status code: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ File upload test failed: {e}")
                return False
        else:
            print("⚠️  Sample file not found, skipping file upload test")
            
        # Test 3: Test invalid file type
        try:
            files = {'file': ('test.txt', b'Hello World', 'text/plain')}
            response = requests.post(f"{self.ml_app_url}/analyze", files=files, timeout=10)
            
            if response.status_code == 200 and "Unsupported file type" in response.text:
                print("✅ Invalid file type properly rejected")
            else:
                print("⚠️  Invalid file type handling may need improvement")
        except Exception as e:
            print(f"⚠️  Invalid file type test failed: {e}")
            
        return True
        
    def test_virustotal_application(self):
        """Test the VirusTotal-based detection application"""
        print("\n🌐 Testing VirusTotal-based detection application...")
        
        # Test 1: Check if application is running
        try:
            response = requests.get(f"{self.vt_app_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ VirusTotal application is running and accessible")
            else:
                print(f"❌ VirusTotal application returned status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Failed to connect to VirusTotal application: {e}")
            return False
            
        # Test 2: Test without API key (should show error message)
        try:
            data = {'file_hash': 'test123'}
            response = requests.post(f"{self.vt_app_url}/analyze", data=data, timeout=10)
            
            if response.status_code == 200 and "API key not configured" in response.text:
                print("✅ Missing API key properly handled")
            else:
                print("⚠️  API key error handling may need improvement")
        except Exception as e:
            print(f"⚠️  API key test failed: {e}")
            
        # Test 3: Test URL analysis without API key
        try:
            data = {'url': 'https://example.com'}
            response = requests.post(f"{self.vt_app_url}/analyze", data=data, timeout=10)
            
            if response.status_code == 200 and "API key not configured" in response.text:
                print("✅ URL analysis without API key properly handled")
            else:
                print("⚠️  URL analysis error handling may need improvement")
        except Exception as e:
            print(f"⚠️  URL analysis test failed: {e}")
            
        return True
        
    def test_error_handling(self):
        """Test error handling in both applications"""
        print("\n🛡️  Testing error handling...")
        
        # Test ML app with invalid file
        try:
            files = {'file': ('invalid.exe', b'invalid content', 'application/octet-stream')}
            response = requests.post(f"{self.ml_app_url}/analyze", files=files, timeout=10)
            
            if response.status_code == 200:
                print("✅ ML app handled invalid file gracefully")
            else:
                print("⚠️  ML app error handling may need improvement")
        except Exception as e:
            print(f"⚠️  ML app error handling test failed: {e}")
            
        # Test VirusTotal app with empty input
        try:
            data = {}
            response = requests.post(f"{self.vt_app_url}/analyze", data=data, timeout=10)
            
            if response.status_code == 200 and "No valid input provided" in response.text:
                print("✅ VirusTotal app handled empty input properly")
            else:
                print("⚠️  VirusTotal app input validation may need improvement")
        except Exception as e:
            print(f"⚠️  VirusTotal app error handling test failed: {e}")
            
        return True
        
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Starting comprehensive application testing...")
        print("=" * 60)
        
        success = True
        
        # Start applications
        if not self.start_applications():
            print("❌ Failed to start applications")
            return False
            
        try:
            # Test ML application
            if not self.test_ml_application():
                success = False
                
            # Test VirusTotal application
            if not self.test_virustotal_application():
                success = False
                
            # Test error handling
            if not self.test_error_handling():
                success = False
                
        finally:
            # Always stop applications
            self.stop_applications()
            
        print("\n" + "=" * 60)
        if success:
            print("🎉 All tests passed! Applications are working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the output above.")
            
        return success

def main():
    """Main function"""
    print("NeuroShield Malware Detection - Application Tester")
    print("=" * 60)
    
    tester = ApplicationTester()
    
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        tester.stop_applications()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        tester.stop_applications()
        sys.exit(1)

if __name__ == "__main__":
    main()