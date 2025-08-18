# Deployment Troubleshooting Guide

## 🚨 Common Build Issues

### 1. OpenGL/Mesa Package Errors
**Error**: `Package 'libgl1-mesa-glx' has no installation candidate`

**Solution**: Use the minimal Dockerfile
```yaml
# In render.yaml, change:
dockerfilePath: ./Dockerfile.minimal
```

### 2. Memory Issues During Build
**Error**: Build fails due to memory constraints

**Solutions**:
- Use `requirements-minimal.txt` instead of `requirements.txt`
- Reduce thread counts in environment variables
- Use the minimal Dockerfile

### 3. PyTorch Installation Issues
**Error**: PyTorch fails to install

**Solution**: Use CPU-only PyTorch
```bash
# In requirements-minimal.txt, use:
torch==2.1.2+cpu
torchvision==0.16.2+cpu
```

## 🔧 Alternative Deployment Methods

### Method 1: Render with Minimal Setup
1. Use `Dockerfile.minimal`
2. Use `requirements-minimal.txt`
3. Update `render.yaml`:
```yaml
dockerfilePath: ./Dockerfile.minimal
```

### Method 2: Google Cloud Run (Recommended)
```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy deepfake-detector \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

### Method 3: Fly.io (Free Tier)
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Create fly.toml
fly launch --no-deploy

# Edit fly.toml to add:
[env]
  MEDIAPIPE_DISABLE_GPU = "1"
  KMP_DUPLICATE_LIB_OK = "True"

# Deploy
fly deploy
```

## 📋 Pre-Deployment Checklist

- [ ] All required files present
- [ ] Git repository initialized and pushed
- [ ] Environment variables configured
- [ ] Dependencies compatible
- [ ] Dockerfile tested locally

## 🐛 Debug Commands

### Test Docker Build Locally
```bash
docker build -f Dockerfile.minimal -t deepfake-detector .
docker run -p 10000:10000 deepfake-detector
```

### Check Requirements Compatibility
```bash
pip install -r requirements-minimal.txt
python -c "import torch; print('PyTorch OK')"
python -c "import mediapipe; print('MediaPipe OK')"
```

### Test Flask App Locally
```bash
python server.py
# Visit http://localhost:10000
```

## 📊 Platform Comparison

| Platform | Free Tier | ML Support | Ease of Use | Build Time |
|----------|-----------|------------|-------------|------------|
| Render | ✅ | ✅ | ⭐⭐⭐⭐⭐ | 5-10 min |
| Google Cloud Run | ✅ | ✅ | ⭐⭐⭐⭐ | 3-5 min |
| Fly.io | ✅ | ✅ | ⭐⭐⭐ | 2-4 min |
| Heroku | ❌ | ✅ | ⭐⭐⭐⭐⭐ | 2-3 min |

## 🆘 Emergency Solutions

### If All Else Fails:

1. **Use Google Colab + Gradio**:
   ```python
   !pip install gradio
   import gradio as gr
   
   def detect_fake(video):
       # Your detection logic
       return result
   
   gr.Interface(fn=detect_fake, inputs="video", outputs="text").launch()
   ```

2. **Use Streamlit Cloud**:
   ```bash
   pip install streamlit
   streamlit run app.py
   ```

3. **Use Hugging Face Spaces**:
   - Upload your model to HF Hub
   - Create a Gradio app
   - Deploy on HF Spaces

## 📞 Support

If you're still having issues:
1. Check the platform's documentation
2. Look at the build logs carefully
3. Try a different platform from the list above
4. Consider using a simpler deployment method 