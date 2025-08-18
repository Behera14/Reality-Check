#!/bin/bash

echo "🚀 DeepFake Detection App - Deployment Script"
echo "=============================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote repository found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/yourrepo.git"
    exit 1
fi

echo "✅ Git repository configured"

# Check if all required files exist
required_files=("server.py" "requirements.txt" "Dockerfile" "render.yaml" "wsgi.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

echo "✅ All required files present"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy to Render - $(date)"
git push origin main

echo ""
echo "🎉 Code pushed to GitHub!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect your repository"
echo "5. Configure:"
echo "   - Name: deepfake-detector"
echo "   - Environment: Docker"
echo "   - Branch: main"
echo "6. Click 'Create Web Service'"
echo ""
echo "⏱️  Build time: 5-10 minutes"
echo "🌐 Your app will be available at: https://your-app-name.onrender.com" 