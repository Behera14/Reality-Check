#!/bin/bash

# Deepfake Detection App - Quick Deploy Script
# This script helps you deploy your app to Railway via GitLab

echo "🚀 Deepfake Detection App - Deployment Script"
echo "=============================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if user is logged into Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway:"
    railway login
fi

echo "✅ Prerequisites check passed!"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if we have a remote origin
if ! git remote get-url origin &> /dev/null; then
    echo "❌ No GitLab remote found. Please add your GitLab repository:"
    echo "   git remote add origin <your-gitlab-repo-url>"
    exit 1
fi

echo "📋 Deployment Steps:"
echo "===================="
echo ""
echo "1. 🚂 Push to GitLab:"
echo "   git push origin main"
echo ""
echo "2. 🔧 Set up Railway project:"
echo "   railway init"
echo "   railway link"
echo ""
echo "3. 🔐 Add environment variables in Railway dashboard:"
echo "   FLASK_ENV=production"
echo "   SECRET_KEY=your-super-secret-key-here"
echo "   PORT=10000"
echo ""
echo "4. 🎯 Deploy:"
echo "   railway up"
echo ""
echo "5. 🔗 Get your deployment URL:"
echo "   railway status"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "🎉 Happy deploying!" 