import os
import tensorflow as tf
import sys

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

MODEL_PATH = 'models/df_92_v2.h5'
OUTPUT_FILE = 'model_info.txt'

def describe_model():
    print(f"Loading model from {MODEL_PATH}...")
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        
        print(f"Model loaded successfully.")
        print(f"Saving summary to {OUTPUT_FILE}...")
        
        # redirect stdout to file
        with open(OUTPUT_FILE, 'w') as f:
            # Write header
            f.write(f"Model File: {MODEL_PATH}\n")
            f.write("="*65 + "\n")
            
            # Write summary
            model.summary(print_fn=lambda x: f.write(x + '\n'))
            
            f.write("\n\n")
            f.write("="*65 + "\n")
            f.write("Detailed Layer Information:\n")
            f.write("="*65 + "\n")
            
            for i, layer in enumerate(model.layers):
                f.write(f"Layer {i}: {layer.name} ({layer.__class__.__name__})\n")
                f.write(f"  Input Shape: {layer.input_shape}\n")
                f.write(f"  Output Shape: {layer.output_shape}\n")
                if hasattr(layer, 'activation'):
                    f.write(f"  Activation: {layer.activation.__name__}\n")
                f.write("-" * 30 + "\n")

        print(f"Done! Check {OUTPUT_FILE} for details.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    describe_model()
