#!/usr/bin/env python3

import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import cv2
import os
import sys

# Add the current directory to the path so we can import from server.py
sys.path.append('.')

# Import the model class from server.py
from server import DFModel, get_model

def test_model_loading():
    """Test if the model can be loaded successfully"""
    try:
        print("Testing model loading...")
        model, transform = get_model()
        print("✅ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_single_image_prediction():
    """Test prediction on a single image"""
    try:
        print("Testing single image prediction...")
        model, transform = get_model()
        
        # Create a dummy image (random noise)
        dummy_image = torch.randn(1, 3, 224, 224)
        
        with torch.no_grad():
            fmap, logits = model(dummy_image)
            probabilities = F.softmax(logits, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)
            
        print(f"✅ Single image prediction successful!")
        print(f"   Prediction: {predicted_class.item()}")
        print(f"   Confidence: {confidence.item() * 100:.2f}%")
        return True
    except Exception as e:
        print(f"❌ Error in single image prediction: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_video_sequence_prediction():
    """Test prediction on a video sequence (5D tensor)"""
    try:
        print("Testing video sequence prediction...")
        model, transform = get_model()
        
        # Create a dummy video sequence (5D tensor: [batch, seq, channels, height, width])
        dummy_sequence = torch.randn(1, 20, 3, 112, 112)  # 1 batch, 20 frames, 3 channels, 112x112
        
        with torch.no_grad():
            fmap, logits = model(dummy_sequence)
            probabilities = F.softmax(logits, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)
            
        print(f"✅ Video sequence prediction successful!")
        print(f"   Prediction: {predicted_class.item()}")
        print(f"   Confidence: {confidence.item() * 100:.2f}%")
        return True
    except Exception as e:
        print(f"❌ Error in video sequence prediction: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing DeepFake Detection Model")
    print("=" * 50)
    
    # Test 1: Model loading
    if not test_model_loading():
        print("❌ Model loading failed. Exiting.")
        sys.exit(1)
    
    # Test 2: Single image prediction
    if not test_single_image_prediction():
        print("❌ Single image prediction failed.")
    
    # Test 3: Video sequence prediction
    if not test_video_sequence_prediction():
        print("❌ Video sequence prediction failed.")
    
    print("=" * 50)
    print("✅ All tests completed!") 