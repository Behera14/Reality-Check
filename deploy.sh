#!/bin/bash

# 🚀 DeepFake Detection App - Deployment Script
# This script helps deploy your app to Render

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "server.py" ]; then
    echo "❌ Error: server.py not found. Please run this script from the project root."
    exit 1
fi

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found. Please ensure it exists."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please ensure it exists."
    exit 1
fi

echo "✅ Project structure looks good!"

# Git operations
echo "📝 Checking git status..."
git status

echo "📤 Pushing to GitLab..."
git add .
git commit -m "Deploy: $(date)"
git push gitlab main

echo "✅ Code pushed to GitLab successfully!"

echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://dashboard.render.com"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitLab repository"
echo "4. Use these settings:"
echo "   - Name: deepfake-detection-app"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python server.py"
echo "5. Deploy!"
echo ""
echo "🌐 Your app will be available at: https://deepfake-detection-app.onrender.com"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md" 