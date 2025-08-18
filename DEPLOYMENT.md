# Deepfake Detection App - Deployment Guide

## 🚀 Recommended Platform: Railway

This application is optimized for deployment on **Railway** due to its ML-friendly infrastructure and GitLab integration.

## 📋 Prerequisites

1. **GitLab Account** with your repository
2. **Railway Account** (free tier available)
3. **Railway CLI** installed locally

## 🔧 Setup Instructions

### Step 1: Railway Setup

1. **Create Railway Account**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   ```

2. **Create New Project**
   ```bash
   # Initialize Railway project
   railway init
   
   # Link to existing project (if created via web)
   railway link
   ```

### Step 2: Environment Variables

Set these environment variables in Railway dashboard:

```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
PORT=10000
```

### Step 3: GitLab CI/CD Setup

1. **Add Railway Token to GitLab**
   - Go to GitLab → Settings → CI/CD → Variables
   - Add variable: `RAILWAY_TOKEN` (get from Railway dashboard)

2. **Configure GitLab Repository**
   ```bash
   # Push your code to GitLab
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

### Step 4: Deploy

1. **Manual Deployment**
   ```bash
   # Deploy directly from CLI
   railway up
   ```

2. **Automatic Deployment via GitLab**
   - Go to GitLab → CI/CD → Pipelines
   - Run the deployment pipeline manually
   - Or it will auto-deploy on main branch pushes

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitLab Repo   │───▶│  GitLab CI/CD   │───▶│   Railway App   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Test Stage    │    │  Production     │
                       │   (PyTorch,     │    │  Environment    │
                       │   MediaPipe)    │    │                 │
                       └─────────────────┘    └─────────────────┘
```

## 📁 File Structure

```
├── server.py              # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── .gitlab-ci.yml        # GitLab CI/CD pipeline
├── railway.json          # Railway configuration
├── Procfile             # Railway process file
├── runtime.txt          # Python version
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── Uploaded_Files/      # Temporary uploads
└── instance/            # SQLite database
```

## 🔍 Monitoring & Logs

### Railway Dashboard
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, network usage
- **Deployments**: Deployment history and rollbacks

### GitLab CI/CD
- **Pipeline Status**: Build and test results
- **Artifacts**: Test reports and build artifacts
- **Variables**: Environment configuration

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check Docker build locally
   docker build -t deepfake-app .
   docker run -p 10000:10000 deepfake-app
   ```

2. **Memory Issues**
   - Increase Railway instance size
   - Optimize model loading (lazy loading)

3. **Timeout Issues**
   - Increase healthcheck timeout in railway.json
   - Optimize video processing

### Performance Optimization

1. **Model Caching**
   ```python
   # Cache model in memory
   model = None
   
   def get_model():
       global model
       if model is None:
           model = load_model()
       return model
   ```

2. **File Cleanup**
   ```python
   # Clean up temporary files
   import atexit
   atexit.register(cleanup_temp_files)
   ```

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit secrets to Git
   - Use Railway's secure environment variables

2. **File Upload Security**
   - Validate file types and sizes
   - Clean up uploaded files

3. **Database Security**
   - Use production database (PostgreSQL on Railway)
   - Regular backups

## 📊 Scaling

### Railway Scaling Options

1. **Vertical Scaling**
   - Increase CPU/memory allocation
   - Enable auto-scaling

2. **Horizontal Scaling**
   - Multiple instances
   - Load balancing

### Cost Optimization

1. **Free Tier Limits**
   - 500 hours/month
   - 1GB RAM, 0.5 vCPU

2. **Paid Plans**
   - Pay-per-use pricing
   - Auto-scaling capabilities

## 🆘 Support

- **Railway Docs**: https://docs.railway.app/
- **GitLab CI/CD**: https://docs.gitlab.com/ee/ci/
- **Flask Deployment**: https://flask.palletsprojects.com/en/2.3.x/deploying/

## 📝 Deployment Checklist

- [ ] Railway account created
- [ ] Environment variables set
- [ ] GitLab repository configured
- [ ] CI/CD pipeline working
- [ ] Application deployed successfully
- [ ] Health checks passing
- [ ] Domain configured (optional)
- [ ] SSL certificate enabled (automatic on Railway) 