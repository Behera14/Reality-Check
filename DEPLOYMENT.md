# DeepFake Detection App - Deployment Guide

## 🚀 Recommended Platform: Render (Free)

### Why Render?
- ✅ Free tier available
- ✅ Docker support
- ✅ Persistent storage
- ✅ Good for ML applications
- ✅ Easy deployment

### Deployment Steps:

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub account

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   - **Name**: `deepfake-detector`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (if app is in root)

4. **Environment Variables** (Optional - already in render.yaml)
   - `PORT`: `10000`
   - `MEDIAPIPE_DISABLE_GPU`: `1`
   - `FLASK_ENV`: `production`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes)

## 🔧 Alternative Platforms

### Google Cloud Run (Free Tier)
```bash
# Install Google Cloud CLI
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy deepfake-detector \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Fly.io (Free Tier)
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### Heroku (Paid - $7/month)
```bash
# Install Heroku CLI
heroku create deepfake-detector
git push heroku main
```

## 📁 File Structure for Deployment
```
├── server.py              # Main Flask app
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── render.yaml           # Render configuration
├── wsgi.py              # WSGI entry point
├── templates/            # HTML templates
├── static/              # Static files
└── .dockerignore        # Docker ignore file
```

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check `requirements.txt` for version conflicts
   - Ensure all dependencies are compatible

2. **App Crashes on Startup**
   - Check logs in Render dashboard
   - Verify environment variables

3. **Memory Issues**
   - Reduce thread counts in render.yaml
   - Optimize ML model loading

4. **File Upload Issues**
   - Ensure directories exist and have proper permissions
   - Check file size limits

### Performance Optimization:

1. **For Render Free Tier:**
   - Reduced thread counts to 2 (already configured)
   - Single worker in Gunicorn
   - Optimized Docker image

2. **For Production:**
   - Upgrade to paid plan for more resources
   - Add Redis for session management
   - Use CDN for static files

## 🌐 Access Your App

After deployment, your app will be available at:
- Render: `https://your-app-name.onrender.com`
- Google Cloud Run: `https://your-app-name-xxxxx-uc.a.run.app`
- Fly.io: `https://your-app-name.fly.dev`
- Heroku: `https://your-app-name.herokuapp.com`

## 📊 Monitoring

- **Render**: Built-in logs and metrics
- **Google Cloud**: Cloud Monitoring
- **Fly.io**: Built-in monitoring
- **Heroku**: Heroku Metrics

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable HTTPS (automatic on most platforms)
- Regular dependency updates 