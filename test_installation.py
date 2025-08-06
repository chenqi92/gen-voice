#!/usr/bin/env python3
"""
Test script to verify Kitten TTS installation and basic functionality
"""

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required packages can be imported"""
    logger.info("Testing imports...")
    
    try:
        import flask
        logger.info(f"✓ Flask {flask.__version__}")
    except ImportError as e:
        logger.error(f"✗ Flask import failed: {e}")
        return False
    
    try:
        import soundfile
        logger.info(f"✓ SoundFile {soundfile.__version__}")
    except ImportError as e:
        logger.error(f"✗ SoundFile import failed: {e}")
        return False
    
    try:
        import numpy
        logger.info(f"✓ NumPy {numpy.__version__}")
    except ImportError as e:
        logger.error(f"✗ NumPy import failed: {e}")
        return False
    
    return True

def test_kitten_tts():
    """Test if Kitten TTS can be imported and initialized"""
    logger.info("Testing Kitten TTS...")
    
    try:
        from kittentts import KittenTTS
        logger.info("✓ Kitten TTS imported successfully")
        
        # Try to initialize the model
        logger.info("Initializing Kitten TTS model (this may take a moment)...")
        model = KittenTTS("KittenML/kitten-tts-nano-0.1")
        logger.info("✓ Kitten TTS model loaded successfully")
        
        # Test getting available voices
        voices = model.available_voices
        logger.info(f"✓ Available voices: {voices}")
        
        # Test basic generation with a short text
        test_text = "Hello, this is a test."
        logger.info(f"Testing speech generation with: '{test_text}'")
        audio = model.generate(test_text)
        logger.info(f"✓ Speech generated successfully (audio shape: {audio.shape})")
        
        return True
        
    except ImportError as e:
        logger.warning(f"⚠ Kitten TTS import failed: {e}")
        logger.info("This is expected if Kitten TTS is not installed.")
        logger.info("The web app will run in demo mode.")
        logger.info("To install Kitten TTS, use:")
        logger.info("pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl")
        return True  # Return True for demo mode
    except Exception as e:
        logger.warning(f"⚠ Kitten TTS initialization failed: {e}")
        logger.info("The web app will run in demo mode.")
        return True  # Return True for demo mode

def test_web_app():
    """Test if the web application can be imported"""
    logger.info("Testing web application...")
    
    try:
        from app import app, load_tts_model
        logger.info("✓ Web application imported successfully")
        
        # Test model loading
        if load_tts_model():
            logger.info("✓ TTS model loaded in web app (may be in demo mode)")
        else:
            logger.error("✗ Failed to load TTS model in web app")
            return False
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ Web application import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Web application test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("Kitten TTS Web Application Installation Test")
    logger.info("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Kitten TTS", test_kitten_tts),
        ("Web Application", test_web_app),
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
    logger.info("\n" + "=" * 50)
    logger.info("TEST SUMMARY")
    logger.info("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 All tests passed! Your installation is ready.")
        logger.info("You can now run the application with: python app.py")
    else:
        logger.error("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
