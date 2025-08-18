#!/usr/bin/env python3

import torch
import torch.nn.functional as F
import numpy as np
import sys
import os

# Add current directory to path
sys.path.append('.')

from server import DFModel, get_model, predict

def test_model_variability():
    """Test if the model produces different outputs for different inputs"""
    print("🧪 Testing Model Variability")
    print("=" * 50)
    
    try:
        # Get the model
        model, transform = get_model()
        print("✅ Model loaded successfully")
        
        # Test 1: Different random inputs should give different outputs
        print("\n📊 Test 1: Random Input Variability")
        results = []
        
        for i in range(5):
            # Create different random inputs
            random_input = torch.randn(1, 20, 3, 112, 112)  # Different random data each time
            
            with torch.no_grad():
                fmap, logits = model(random_input)
                probabilities = F.softmax(logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
                
                result = {
                    'prediction': int(predicted_class.item()),
                    'confidence': float(confidence.item() * 100),
                    'logits': logits.detach().cpu().numpy().flatten()
                }
                results.append(result)
                
                print(f"   Test {i+1}: Prediction={result['prediction']}, Confidence={result['confidence']:.2f}%")
        
        # Check if results vary
        predictions = [r['prediction'] for r in results]
        confidences = [r['confidence'] for r in results]
        
        if len(set(predictions)) > 1:
            print("✅ Predictions vary - Model is working!")
        else:
            print("⚠️  All predictions are the same - might be hardcoded")
            
        if max(confidences) - min(confidences) > 1.0:
            print("✅ Confidences vary - Model is working!")
        else:
            print("⚠️  Confidences are very similar - might be hardcoded")
        
        # Test 2: Test with the predict function
        print("\n📊 Test 2: Using predict() function")
        for i in range(3):
            random_input = torch.randn(1, 20, 3, 112, 112)
            result = predict(model, random_input)
            print(f"   Test {i+1}: {result}")
        
        # Test 3: Test with extreme inputs
        print("\n📊 Test 3: Extreme Inputs")
        
        # All zeros
        zeros_input = torch.zeros(1, 20, 3, 112, 112)
        with torch.no_grad():
            fmap, logits = model(zeros_input)
            probabilities = F.softmax(logits, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)
            print(f"   All zeros: Prediction={predicted_class.item()}, Confidence={confidence.item()*100:.2f}%")
        
        # All ones
        ones_input = torch.ones(1, 20, 3, 112, 112)
        with torch.no_grad():
            fmap, logits = model(ones_input)
            probabilities = F.softmax(logits, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)
            print(f"   All ones: Prediction={predicted_class.item()}, Confidence={confidence.item()*100:.2f}%")
        
        # High values
        high_input = torch.ones(1, 20, 3, 112, 112) * 10
        with torch.no_grad():
            fmap, logits = model(high_input)
            probabilities = F.softmax(logits, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)
            print(f"   High values: Prediction={predicted_class.item()}, Confidence={confidence.item()*100:.2f}%")
        
        # Test 4: Check model parameters
        print("\n📊 Test 4: Model Parameters")
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        print(f"   Total parameters: {total_params:,}")
        print(f"   Trainable parameters: {trainable_params:,}")
        
        # Check if parameters are non-zero (not hardcoded)
        non_zero_params = sum((p != 0).sum().item() for p in model.parameters())
        print(f"   Non-zero parameters: {non_zero_params:,}")
        
        if non_zero_params > 0:
            print("✅ Model has non-zero parameters - likely trained")
        else:
            print("❌ All parameters are zero - likely hardcoded")
        
        # Test 5: Check model gradients
        print("\n📊 Test 5: Model Gradients")
        random_input = torch.randn(1, 20, 3, 112, 112, requires_grad=True)
        fmap, logits = model(random_input)
        loss = logits.sum()
        loss.backward()
        
        grad_norm = torch.norm(random_input.grad).item()
        print(f"   Gradient norm: {grad_norm:.6f}")
        
        if grad_norm > 1e-6:
            print("✅ Model produces gradients - likely functional")
        else:
            print("⚠️  Very small gradients - might be hardcoded")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_hardcoded_detection():
    """Test to detect if results are hardcoded"""
    print("\n🔍 Hardcoded Detection Test")
    print("=" * 30)
    
    try:
        model, transform = get_model()
        
        # Test with completely different inputs
        test_inputs = [
            torch.randn(1, 20, 3, 112, 112),  # Random
            torch.randn(1, 20, 3, 112, 112) * 100,  # High variance
            torch.randn(1, 20, 3, 112, 112) * 0.01,  # Low variance
            torch.zeros(1, 20, 3, 112, 112),  # Zeros
            torch.ones(1, 20, 3, 112, 112),   # Ones
        ]
        
        results = []
        for i, test_input in enumerate(test_inputs):
            with torch.no_grad():
                fmap, logits = model(test_input)
                probabilities = F.softmax(logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
                
                result = {
                    'input_type': f'Test {i+1}',
                    'prediction': int(predicted_class.item()),
                    'confidence': float(confidence.item() * 100),
                    'logits': logits.detach().cpu().numpy().flatten()
                }
                results.append(result)
        
        # Analyze results
        predictions = [r['prediction'] for r in results]
        confidences = [r['confidence'] for r in results]
        
        print(f"Predictions: {predictions}")
        print(f"Confidences: {[f'{c:.2f}%' for c in confidences]}")
        
        # Check for hardcoded patterns
        if len(set(predictions)) == 1:
            print("❌ SUSPICIOUS: All predictions are identical - likely hardcoded!")
        else:
            print("✅ Predictions vary - good sign")
            
        if max(confidences) - min(confidences) < 0.1:
            print("❌ SUSPICIOUS: All confidences are nearly identical - likely hardcoded!")
        else:
            print("✅ Confidences vary - good sign")
        
        # Check logits for patterns
        logits_arrays = [r['logits'] for r in results]
        logits_variance = [np.var(logits) for logits in logits_arrays]
        print(f"Logits variance: {[f'{v:.6f}' for v in logits_variance]}")
        
        if all(v < 1e-6 for v in logits_variance):
            print("❌ SUSPICIOUS: Very low logits variance - likely hardcoded!")
        else:
            print("✅ Logits vary - good sign")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in hardcoded detection: {e}")
        return False

if __name__ == "__main__":
    print("🔬 DeepFake Model Authenticity Test")
    print("=" * 60)
    
    # Run tests
    test_model_variability()
    test_hardcoded_detection()
    
    print("\n" + "=" * 60)
    print("🏁 Test completed!")
    print("\n💡 Interpretation:")
    print("- If predictions and confidences vary significantly, the model is likely working")
    print("- If all results are identical, the model might be hardcoded")
    print("- Check the console output above for detailed analysis") 