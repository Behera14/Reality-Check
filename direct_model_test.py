#!/usr/bin/env python3

import torch
import torch.nn.functional as F
import numpy as np
import sys
import os

# Add current directory to path
sys.path.append('.')

from server import DFModel, get_model, predict

def test_actual_model_results():
    """Test the actual model with real inputs and show results"""
    print("🔬 ACTUAL MODEL RESULTS TEST")
    print("=" * 50)
    
    try:
        # Load the actual model
        print("Loading model...")
        model, transform = get_model()
        print("✅ Model loaded successfully!")
        
        # Test 1: Multiple random inputs to see real variability
        print("\n📊 Test 1: Model Predictions with Different Inputs")
        print("-" * 40)
        
        results = []
        for i in range(10):
            # Create random input (simulating different videos)
            random_input = torch.randn(1, 20, 3, 112, 112)
            
            with torch.no_grad():
                fmap, logits = model(random_input)
                probabilities = F.softmax(logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
                
                result = {
                    'test': i + 1,
                    'prediction': int(predicted_class.item()),
                    'confidence': float(confidence.item() * 100),
                    'class': 'FAKE' if predicted_class.item() == 0 else 'REAL'
                }
                results.append(result)
                
                print(f"Test {i+1:2d}: {result['class']:4s} | Confidence: {result['confidence']:6.2f}%")
        
        # Calculate statistics
        fake_count = sum(1 for r in results if r['prediction'] == 0)
        real_count = sum(1 for r in results if r['prediction'] == 1)
        avg_confidence = np.mean([r['confidence'] for r in results])
        
        print(f"\n📈 Statistics:")
        print(f"FAKE predictions: {fake_count}/10 ({fake_count*10}%)")
        print(f"REAL predictions: {real_count}/10 ({real_count*10}%)")
        print(f"Average confidence: {avg_confidence:.2f}%")
        
        # Test 2: Extreme cases
        print("\n📊 Test 2: Extreme Input Cases")
        print("-" * 40)
        
        extreme_cases = [
            ("All Zeros", torch.zeros(1, 20, 3, 112, 112)),
            ("All Ones", torch.ones(1, 20, 3, 112, 112)),
            ("High Values", torch.ones(1, 20, 3, 112, 112) * 10),
            ("Negative Values", torch.ones(1, 20, 3, 112, 112) * -5),
        ]
        
        for case_name, test_input in extreme_cases:
            with torch.no_grad():
                fmap, logits = model(test_input)
                probabilities = F.softmax(logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
                
                class_name = 'FAKE' if predicted_class.item() == 0 else 'REAL'
                print(f"{case_name:15s}: {class_name:4s} | Confidence: {confidence.item()*100:6.2f}%")
        
        # Test 3: Model parameters analysis
        print("\n📊 Test 3: Model Parameters Analysis")
        print("-" * 40)
        
        total_params = sum(p.numel() for p in model.parameters())
        non_zero_params = sum((p != 0).sum().item() for p in model.parameters())
        param_variance = []
        
        for name, param in model.named_parameters():
            if param.numel() > 0:
                variance = torch.var(param).item()
                param_variance.append(variance)
        
        avg_variance = np.mean(param_variance)
        
        print(f"Total parameters: {total_params:,}")
        print(f"Non-zero parameters: {non_zero_params:,}")
        print(f"Average parameter variance: {avg_variance:.6f}")
        
        if avg_variance > 1e-6:
            print("✅ Model parameters show variation - likely trained")
        else:
            print("⚠️  Low parameter variance - might be untrained")
        
        # Test 4: Real prediction function test
        print("\n📊 Test 4: Using predict() Function")
        print("-" * 40)
        
        for i in range(5):
            random_input = torch.randn(1, 20, 3, 112, 112)
            result = predict(model, random_input)
            class_name = 'FAKE' if result[0] == 0 else 'REAL'
            print(f"Test {i+1}: {class_name:4s} | Confidence: {result[1]:6.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_accuracy_simulation():
    """Simulate model accuracy with known patterns"""
    print("\n📊 Test 5: Model Accuracy Simulation")
    print("-" * 40)
    
    try:
        model, transform = get_model()
        
        # Create test cases that should be clearly different
        test_cases = [
            ("Random Noise 1", torch.randn(1, 20, 3, 112, 112)),
            ("Random Noise 2", torch.randn(1, 20, 3, 112, 112)),
            ("Random Noise 3", torch.randn(1, 20, 3, 112, 112)),
            ("Structured Pattern", torch.randn(1, 20, 3, 112, 112) * 0.5 + 0.5),
            ("High Contrast", torch.randn(1, 20, 3, 112, 112) * 2.0),
        ]
        
        predictions = []
        confidences = []
        
        for case_name, test_input in test_cases:
            with torch.no_grad():
                fmap, logits = model(test_input)
                probabilities = F.softmax(logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
                
                predictions.append(predicted_class.item())
                confidences.append(confidence.item() * 100)
                
                class_name = 'FAKE' if predicted_class.item() == 0 else 'REAL'
                print(f"{case_name:20s}: {class_name:4s} | Confidence: {confidence.item()*100:6.2f}%")
        
        # Calculate consistency
        unique_predictions = len(set(predictions))
        confidence_range = max(confidences) - min(confidences)
        
        print(f"\nConsistency Analysis:")
        print(f"Unique predictions: {unique_predictions}/5")
        print(f"Confidence range: {confidence_range:.2f}%")
        
        if unique_predictions > 1:
            print("✅ Model shows variability - likely real")
        else:
            print("⚠️  All predictions identical - suspicious")
            
        if confidence_range > 5.0:
            print("✅ Confidence varies significantly - likely real")
        else:
            print("⚠️  Confidence very similar - suspicious")
        
    except Exception as e:
        print(f"❌ Error in accuracy test: {e}")

if __name__ == "__main__":
    print("🎯 DIRECT MODEL ACCURACY & RESULTS TEST")
    print("=" * 60)
    print("This test shows the ACTUAL model performance without any hardcoded values")
    print("=" * 60)
    
    # Run the tests
    test_actual_model_results()
    test_model_accuracy_simulation()
    
    print("\n" + "=" * 60)
    print("🏁 TEST COMPLETED!")
    print("\n💡 What to look for:")
    print("- Different predictions for different inputs = REAL MODEL")
    print("- Varying confidence scores = REAL MODEL") 
    print("- Non-zero parameter variance = TRAINED MODEL")
    print("- All identical results = SUSPICIOUS/HARDCODED") 