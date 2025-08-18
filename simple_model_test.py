#!/usr/bin/env python3

import torch
import torch.nn.functional as F
import numpy as np

def create_test_model():
    """Create a simple test model to demonstrate real vs hardcoded results"""
    class SimpleTestModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = torch.nn.Conv2d(3, 64, 3, padding=1)
            self.conv2 = torch.nn.Conv2d(64, 128, 3, padding=1)
            self.pool = torch.nn.AdaptiveAvgPool2d(1)
            self.fc = torch.nn.Linear(128, 2)
            
        def forward(self, x):
            # Handle both 4D and 5D inputs
            if len(x.shape) == 5:
                batch_size, seq_len, c, h, w = x.shape
                x = x.view(batch_size * seq_len, c, h, w)
            else:
                x = x.unsqueeze(1)  # Add sequence dimension
                batch_size, seq_len, c, h, w = x.shape
                x = x.view(batch_size * seq_len, c, h, w)
            
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = self.pool(x)
            x = x.view(batch_size, seq_len, -1)
            x = x.mean(dim=1)  # Average over sequence
            x = self.fc(x)
            return None, x  # Return dummy fmap and logits

    return SimpleTestModel()

def test_real_model_behavior():
    """Test with a real model to show actual behavior"""
    print("🔬 REAL MODEL BEHAVIOR TEST")
    print("=" * 50)
    
    # Create a real model with random weights
    model = create_test_model()
    model.eval()
    
    print("✅ Model created with random weights")
    
    # Test with different inputs
    print("\n📊 Test Results with Different Inputs:")
    print("-" * 40)
    
    results = []
    for i in range(8):
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
    fake_count = sum(1 for r in results if r['prediction'] == 0)
    real_count = sum(1 for r in results if r['prediction'] == 1)
    avg_confidence = np.mean([r['confidence'] for r in results])
    confidence_std = np.std([r['confidence'] for r in results])
    
    print(f"\n📈 Statistics:")
    print(f"FAKE predictions: {fake_count}/8 ({fake_count*12.5:.1f}%)")
    print(f"REAL predictions: {real_count}/8 ({real_count*12.5:.1f}%)")
    print(f"Average confidence: {avg_confidence:.2f}%")
    print(f"Confidence std dev: {confidence_std:.2f}%")
    
    # Test with extreme inputs
    print(f"\n📊 Extreme Input Tests:")
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

def test_hardcoded_behavior():
    """Test with hardcoded results for comparison"""
    print("\n🔬 HARDCODED MODEL BEHAVIOR (FOR COMPARISON)")
    print("=" * 50)
    
    def hardcoded_predict(input_data):
        # Always return the same result regardless of input
        return 0, 85.5  # FAKE, 85.5% confidence
    
    print("❌ This is what HARDCODED results look like:")
    print("-" * 40)
    
    for i in range(8):
        random_input = torch.randn(1, 20, 3, 112, 112)
        prediction, confidence = hardcoded_predict(random_input)
        class_name = 'FAKE' if prediction == 0 else 'REAL'
        print(f"Test {i+1:2d}: {class_name:4s} | Confidence: {confidence:6.2f}%")
    
    print(f"\n📈 Hardcoded Statistics:")
    print(f"FAKE predictions: 8/8 (100.0%)")
    print(f"REAL predictions: 0/8 (0.0%)")
    print(f"Average confidence: 85.50%")
    print(f"Confidence std dev: 0.00%")
    
    print(f"\n❌ HARDCODED CHARACTERISTICS:")
    print("- All predictions are identical")
    print("- All confidence scores are identical")
    print("- No variation regardless of input")
    print("- This indicates a fake/hardcoded model")

if __name__ == "__main__":
    print("🎯 MODEL AUTHENTICITY COMPARISON")
    print("=" * 60)
    print("This test compares REAL model behavior vs HARDCODED behavior")
    print("=" * 60)
    
    # Test real model behavior
    test_real_model_behavior()
    
    # Test hardcoded behavior for comparison
    test_hardcoded_behavior()
    
    print("\n" + "=" * 60)
    print("🏁 COMPARISON COMPLETED!")
    print("\n💡 KEY DIFFERENCES:")
    print("✅ REAL MODEL:")
    print("   - Different predictions for different inputs")
    print("   - Varying confidence scores")
    print("   - Responds to input changes")
    print("   - Shows natural variability")
    print("\n❌ HARDCODED MODEL:")
    print("   - Always same prediction")
    print("   - Always same confidence")
    print("   - No response to input changes")
    print("   - No variability")
    print("\n🔍 To test your actual model:")
    print("1. Run the same input multiple times - should get same result")
    print("2. Run different inputs - should get different results")
    print("3. If ALL results are identical = HARDCODED")
    print("4. If results vary with input = REAL MODEL") 