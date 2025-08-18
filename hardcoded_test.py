#!/usr/bin/env python3

import torch
import torch.nn.functional as F
import numpy as np
import random

def hardcoded_predict(model, img, path='./'):
    """Hardcoded version that always returns the same result"""
    # Always return FAKE with 85.5% confidence
    return [0, 85.5]  # 0 = FAKE, 85.5% confidence

def hardcoded_model_forward(x):
    """Hardcoded model forward pass that always returns the same logits"""
    # Always return the same logits regardless of input
    batch_size = x.shape[0]
    # Create logits that will always give FAKE prediction with ~85.5% confidence
    logits = torch.tensor([[2.0, 1.0]] * batch_size)  # Higher value for class 0 (FAKE)
    fmap = torch.randn(batch_size, 2048, 7, 7)  # Dummy feature map
    return fmap, logits

def test_hardcoded_vs_real():
    """Compare hardcoded vs real model behavior"""
    print("🔬 Hardcoded vs Real Model Comparison")
    print("=" * 50)
    
    # Test hardcoded version
    print("\n📊 Hardcoded Model Test:")
    for i in range(5):
        # Create different random inputs
        random_input = torch.randn(1, 20, 3, 112, 112)
        result = hardcoded_predict(None, random_input)
        print(f"   Test {i+1}: {result}")
    
    # Test with extreme inputs
    print("\n📊 Hardcoded Model - Extreme Inputs:")
    test_inputs = [
        torch.zeros(1, 20, 3, 112, 112),  # All zeros
        torch.ones(1, 20, 3, 112, 112),   # All ones
        torch.randn(1, 20, 3, 112, 112) * 100,  # High values
    ]
    
    for i, test_input in enumerate(test_inputs):
        result = hardcoded_predict(None, test_input)
        print(f"   Input {i+1}: {result}")
    
    print("\n💡 Hardcoded Model Characteristics:")
    print("- Always returns the same prediction regardless of input")
    print("- Always returns the same confidence score")
    print("- No variation in results")
    print("- This is what you would see if the model was hardcoded")

def test_real_model_behavior():
    """Test the real model to see if it behaves differently"""
    print("\n📊 Real Model Test (if available):")
    try:
        import sys
        sys.path.append('.')
        from server import get_model, predict
        
        model, transform = get_model()
        
        # Test with different inputs
        for i in range(3):
            random_input = torch.randn(1, 20, 3, 112, 112)
            result = predict(model, random_input)
            print(f"   Test {i+1}: {result}")
        
        # Test with extreme inputs
        print("\n📊 Real Model - Extreme Inputs:")
        test_inputs = [
            torch.zeros(1, 20, 3, 112, 112),  # All zeros
            torch.ones(1, 20, 3, 112, 112),   # All ones
            torch.randn(1, 20, 3, 112, 112) * 100,  # High values
        ]
        
        for i, test_input in enumerate(test_inputs):
            result = predict(model, test_input)
            print(f"   Input {i+1}: {result}")
            
    except Exception as e:
        print(f"   Error testing real model: {e}")

if __name__ == "__main__":
    test_hardcoded_vs_real()
    test_real_model_behavior()
    
    print("\n" + "=" * 50)
    print("🔍 How to Detect Hardcoded Models:")
    print("1. Run the same input multiple times - should get same result")
    print("2. Run different inputs - should get different results")
    print("3. If ALL results are identical regardless of input = HARDCODED")
    print("4. If results vary with input = REAL MODEL")
    print("5. Check model parameters - should be non-zero and varied") 