#!/usr/bin/env python3
"""
Production startup script for DeepFake Detection App
Handles GPU warnings and optimizations for deployment
"""

import os
import sys
import warnings
import logging

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set environment variables for CPU-only processing
os.environ.update({
    'KMP_DUPLICATE_LIB_OK': 'True',
    'MEDIAPIPE_DISABLE_GPU': '1',
    'TF_CPP_MIN_LOG_LEVEL': '3',
    'CUDA_VISIBLE_DEVICES': '',
    'TF_ENABLE_ONEDNN_OPTS': '0',
    'OMP_NUM_THREADS': '1',
    'MKL_NUM_THREADS': '1',
    'OPENBLAS_NUM_THREADS': '1',
    'NUMEXPR_NUM_THREADS': '1',
    'VECLIB_MAXIMUM_THREADS': '1'
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Suppress specific loggers
logging.getLogger('mediapipe').setLevel(logging.ERROR)
logging.getLogger('absl').setLevel(logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Import and run the main application
if __name__ == '__main__':
    try:
        from server import app
        
        port = int(os.environ.get('PORT', 10000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        print("🚀 Starting DeepFake Detection App...")
        print(f"📍 Port: {port}")
        print("🖥️  Mode: CPU-only (GPU disabled)")
        print("🌐 Production ready!")
        
        app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1) 