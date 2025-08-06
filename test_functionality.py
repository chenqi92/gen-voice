#!/usr/bin/env python3
"""
Comprehensive functionality test for Kitten TTS Web Application
Tests all API endpoints and core functionality
"""

import requests
import json
import time
import sys
import logging
import base64
import threading
from subprocess import Popen, PIPE
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class KittenTTSFunctionalityTest:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.app_process = None
        
    def start_app(self):
        """Start the Flask application"""
        logger.info("Starting Kitten TTS Web Application...")
        
        # Use the virtual environment Python
        python_exe = ".venv/Scripts/python.exe" if os.name == 'nt' else ".venv/bin/python"
        
        self.app_process = Popen([python_exe, "app.py"], 
                                stdout=PIPE, stderr=PIPE, text=True)
        
        # Wait for app to start
        logger.info("Waiting for application to start...")
        time.sleep(5)
        
        # Check if app is running
        if self.app_process.poll() is not None:
            stdout, stderr = self.app_process.communicate()
            logger.error(f"App failed to start. STDOUT: {stdout}, STDERR: {stderr}")
            return False
        
        return True
    
    def stop_app(self):
        """Stop the Flask application"""
        if self.app_process:
            logger.info("Stopping application...")
            self.app_process.terminate()
            self.app_process.wait()
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        logger.info("Testing health endpoint...")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_keys = ['status', 'model_loaded', 'available_voices']
                
                if all(key in data for key in expected_keys):
                    logger.info(f"✓ Health check passed: {data}")
                    return True
                else:
                    logger.error(f"✗ Health check missing keys: {data}")
                    return False
            else:
                logger.error(f"✗ Health check failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Health check failed with exception: {e}")
            return False
    
    def test_voices_endpoint(self):
        """Test the voices API endpoint"""
        logger.info("Testing voices endpoint...")
        
        try:
            response = requests.get(f"{self.base_url}/api/voices", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'voices' in data and isinstance(data['voices'], list):
                    voices = data['voices']
                    if len(voices) > 0:
                        # Check voice structure
                        voice = voices[0]
                        expected_keys = ['id', 'name', 'gender', 'description']
                        
                        if all(key in voice for key in expected_keys):
                            logger.info(f"✓ Voices endpoint passed: {len(voices)} voices available")
                            return True, voices
                        else:
                            logger.error(f"✗ Voice missing keys: {voice}")
                            return False, []
                    else:
                        logger.error("✗ No voices available")
                        return False, []
                else:
                    logger.error(f"✗ Invalid voices response: {data}")
                    return False, []
            else:
                logger.error(f"✗ Voices endpoint failed with status {response.status_code}")
                return False, []
                
        except Exception as e:
            logger.error(f"✗ Voices endpoint failed with exception: {e}")
            return False, []
    
    def test_generate_endpoint(self, voice_id="expr-voice-2-f"):
        """Test the speech generation endpoint"""
        logger.info("Testing speech generation endpoint...")
        
        test_text = "Hello, this is a test message for Kitten TTS!"
        
        try:
            payload = {
                "text": test_text,
                "voice": voice_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and 'audio' in data:
                    audio_b64 = data['audio']
                    
                    # Validate base64 audio
                    try:
                        audio_bytes = base64.b64decode(audio_b64)
                        if len(audio_bytes) > 0:
                            logger.info(f"✓ Speech generation passed: {len(audio_bytes)} bytes generated")
                            return True
                        else:
                            logger.error("✗ Generated audio is empty")
                            return False
                    except Exception as e:
                        logger.error(f"✗ Invalid base64 audio: {e}")
                        return False
                else:
                    logger.error(f"✗ Generation failed: {data}")
                    return False
            else:
                logger.error(f"✗ Generation endpoint failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Generation endpoint failed with exception: {e}")
            return False
    
    def test_download_endpoint(self, voice_id="expr-voice-2-f"):
        """Test the audio download endpoint"""
        logger.info("Testing audio download endpoint...")
        
        test_text = "This is a download test for Kitten TTS."
        
        try:
            payload = {
                "text": test_text,
                "voice": voice_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/download",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                if response.headers.get('content-type') == 'audio/wav':
                    audio_data = response.content
                    if len(audio_data) > 0:
                        logger.info(f"✓ Audio download passed: {len(audio_data)} bytes downloaded")
                        return True
                    else:
                        logger.error("✗ Downloaded audio is empty")
                        return False
                else:
                    logger.error(f"✗ Wrong content type: {response.headers.get('content-type')}")
                    return False
            else:
                logger.error(f"✗ Download endpoint failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Download endpoint failed with exception: {e}")
            return False
    
    def test_static_files(self):
        """Test static file serving"""
        logger.info("Testing static file serving...")
        
        static_files = [
            "/static/css/style.css",
            "/static/js/app.js",
            "/static/js/i18n.js"
        ]
        
        all_passed = True
        
        for file_path in static_files:
            try:
                response = requests.get(f"{self.base_url}{file_path}", timeout=10)
                if response.status_code == 200:
                    logger.info(f"✓ Static file served: {file_path}")
                else:
                    logger.error(f"✗ Static file failed: {file_path} (status {response.status_code})")
                    all_passed = False
            except Exception as e:
                logger.error(f"✗ Static file error: {file_path} ({e})")
                all_passed = False
        
        return all_passed
    
    def test_main_page(self):
        """Test the main HTML page"""
        logger.info("Testing main page...")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Check for key elements
                required_elements = [
                    "Kitten TTS",
                    "voice-grid",
                    "text-input",
                    "generate-btn"
                ]
                
                missing_elements = []
                for element in required_elements:
                    if element not in html_content:
                        missing_elements.append(element)
                
                if not missing_elements:
                    logger.info("✓ Main page loaded successfully")
                    return True
                else:
                    logger.error(f"✗ Main page missing elements: {missing_elements}")
                    return False
            else:
                logger.error(f"✗ Main page failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Main page failed with exception: {e}")
            return False
    
    def run_all_tests(self):
        """Run all functionality tests"""
        logger.info("=" * 60)
        logger.info("Kitten TTS Web Application Functionality Test")
        logger.info("=" * 60)
        
        # Start the application
        if not self.start_app():
            logger.error("Failed to start application")
            return False
        
        try:
            # Wait a bit more for full startup
            time.sleep(3)
            
            tests = [
                ("Health Check", self.test_health_endpoint),
                ("Main Page", self.test_main_page),
                ("Static Files", self.test_static_files),
                ("Voices API", lambda: self.test_voices_endpoint()[0]),
                ("Speech Generation", self.test_generate_endpoint),
                ("Audio Download", self.test_download_endpoint),
            ]
            
            results = []
            
            for test_name, test_func in tests:
                logger.info(f"\n--- {test_name} ---")
                try:
                    result = test_func()
                    results.append((test_name, result))
                except Exception as e:
                    logger.error(f"Test '{test_name}' failed with exception: {e}")
                    results.append((test_name, False))
            
            # Summary
            logger.info("\n" + "=" * 60)
            logger.info("TEST SUMMARY")
            logger.info("=" * 60)
            
            passed = 0
            total = len(results)
            
            for test_name, result in results:
                status = "PASS" if result else "FAIL"
                logger.info(f"{test_name}: {status}")
                if result:
                    passed += 1
            
            logger.info(f"\nResults: {passed}/{total} tests passed")
            
            if passed == total:
                logger.info("\n🎉 All functionality tests passed!")
                logger.info("The Kitten TTS Web Application is working correctly!")
                return True
            else:
                logger.error(f"\n❌ {total - passed} tests failed.")
                return False
                
        finally:
            self.stop_app()

def main():
    """Main function"""
    tester = KittenTTSFunctionalityTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
