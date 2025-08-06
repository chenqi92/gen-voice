#!/usr/bin/env python3
"""
Kitten TTS Web Application Runner
Simple script to run the application with proper configuration
"""

import os
import sys
import logging
from app import app, load_tts_model

def setup_logging():
    """Setup logging configuration"""
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log') if os.environ.get('LOG_FILE') else logging.NullHandler()
        ]
    )

def main():
    """Main function to run the application"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Kitten TTS Web Application...")
    
    # Load the TTS model
    if not load_tts_model():
        logger.error("Failed to load TTS model. Exiting...")
        sys.exit(1)
    
    # Get configuration from environment
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
