#!/usr/bin/env python3

import torch
import torch.nn.functional as F
import numpy as np
import sys
import os

# Add current directory to path
sys.path.append('.')

def test_your_actual_model():
    """Test your actual model from server.py"""
    print("🔬 TESTING YOUR ACTUAL MODEL")
    print("=" * 50)
    
    try:
        # Import your actual model
        from server import get_model, predict
        
        print("Loading your actual model...")
        model, transform = get_model()
        print("✅ Your model loaded successfully!")
        
        # Test with different inputs
        print("\n📊 Your Model Results with Different Inputs:")
        print("-" * 50)
        
        results = []
        for i in range(10):
            # Create different random inputs
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
        predictions = [r['prediction'] for r in results]
        confidences = [r['confidence'] for r in results]
        
        fake_count = sum(1 for r in results if r['prediction'] == 0)
        real_count = sum(1 for r in results if r['prediction'] == 1)
        avg_confidence = np.mean(confidences)
        confidence_std = np.std(confidences)
        unique_predictions = len(set(predictions))
        confidence_range = max(confidences) - min(confidences)
        
        print(f"\n📈 Your Model Statistics:")
        print(f"FAKE predictions: {fake_count}/10 ({fake_count*10}%)")
        print(f"REAL predictions: {real_count}/10 ({real_count*10}%)")
        print(f"Average confidence: {avg_confidence:.2f}%")
        print(f"Confidence std dev: {confidence_std:.2f}%")
        print(f"Unique predictions: {unique_predictions}/10")
        print(f"Confidence range: {confidence_range:.2f}%")
        
        # Determine if model is real or hardcoded
        print(f"\n🔍 ANALYSIS:")
        if unique_predictions > 1:
            print("✅ PREDICTIONS VARY - Your model is REAL!")
        else:
            print("❌ ALL PREDICTIONS IDENTICAL - Your model might be HARDCODED!")
            
        if confidence_range > 1.0:
            print("✅ CONFIDENCE VARIES - Your model is REAL!")
        else:
            print("❌ CONFIDENCE TOO SIMILAR - Your model might be HARDCODED!")
            
        if confidence_std > 0.5:
            print("✅ GOOD VARIABILITY - Your model is REAL!")
        else:
            print("⚠️  LOW VARIABILITY - Your model might be HARDCODED!")
        
        # Test with extreme inputs
        print(f"\n📊 Extreme Input Tests:")
        print("-" * 40)
        
        extreme_cases = [
            ("All Zeros", torch.zeros(1, 20, 3, 112, 112)),
            ("All Ones", torch.ones(1, 20, 3, 112, 112)),
            ("High Values", torch.ones(1, 20, 3, 112, 112) * 10),
            ("Negative Values", torch.ones(1, 20, 3, 112, 112) * -5),
        ]
        
        extreme_results = []
        for case_name, test_input in extreme_cases:
            with torch.no_grad():
                fmap, logits = model(test_input)
                probabilities = F.softmax(logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
                
                class_name = 'FAKE' if predicted_class.item() == 0 else 'REAL'
                extreme_results.append({
                    'case': case_name,
                    'prediction': predicted_class.item(),
                    'confidence': confidence.item() * 100,
                    'class': class_name
                })
                
                print(f"{case_name:15s}: {class_name:4s} | Confidence: {confidence.item()*100:6.2f}%")
        
        # Check extreme case variability
        extreme_predictions = [r['prediction'] for r in extreme_results]
        extreme_confidences = [r['confidence'] for r in extreme_results]
        
        if len(set(extreme_predictions)) > 1:
            print("✅ Extreme inputs produce different results - REAL MODEL!")
        else:
            print("❌ Extreme inputs produce same results - SUSPICIOUS!")
            
        if max(extreme_confidences) - min(extreme_confidences) > 5.0:
            print("✅ Extreme inputs produce varying confidence - REAL MODEL!")
        else:
            print("❌ Extreme inputs produce similar confidence - SUSPICIOUS!")
        
        # Final verdict
        print(f"\n🏁 FINAL VERDICT:")
        print("=" * 30)
        
        real_indicators = 0
        if unique_predictions > 1: real_indicators += 1
        if confidence_range > 1.0: real_indicators += 1
        if confidence_std > 0.5: real_indicators += 1
        if len(set(extreme_predictions)) > 1: real_indicators += 1
        if max(extreme_confidences) - min(extreme_confidences) > 5.0: real_indicators += 1
        
        if real_indicators >= 4:
            print("✅ YOUR MODEL IS REAL! (Authentic DeepFake Detection Model)")
            print("   - Shows proper variability")
            print("   - Responds to input changes")
            print("   - Has natural confidence distribution")
        elif real_indicators >= 2:
            print("⚠️  YOUR MODEL MIGHT BE REAL (Some concerns)")
            print("   - Shows some variability")
            print("   - But may have issues")
        else:
            print("❌ YOUR MODEL IS LIKELY HARDCODED!")
            print("   - No variability in predictions")
            print("   - No response to input changes")
            print("   - Suspiciously consistent results")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing your model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 YOUR MODEL AUTHENTICITY TEST")
    print("=" * 60)
    print("This test checks if YOUR actual model is real or hardcoded")
    print("=" * 60)
    
    test_your_actual_model()
    
    print("\n" + "=" * 60)
    print("🏁 TEST COMPLETED!")
    print("\n💡 What this means:")
    print("- If your model shows variability = REAL MODEL")
    print("- If your model always gives same result = HARDCODED")
    print("- Check the analysis above for the final verdict") 