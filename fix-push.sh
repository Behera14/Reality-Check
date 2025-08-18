#!/bin/bash

echo "🔧 Fixing Git Push Issue"
echo "========================"

echo ""
echo "🧹 Clearing cached credentials..."
git config --global --unset credential.helper
git config --global credential.helper cache

echo "✅ Credentials cleared"
echo ""

echo "🔑 Setting up authentication..."
echo ""

echo "📋 You need to create a Personal Access Token:"
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Set Note: 'Render Deployment'"
echo "4. Set Expiration: 90 days"
echo "5. Select scopes:"
echo "   ✅ repo (Full control of private repositories)"
echo "   ✅ workflow (Update GitHub Action workflows)"
echo "6. Click 'Generate token'"
echo "7. Copy the token (you won't see it again!)"
echo ""

echo "🚀 After creating the token, run:"
echo "   git push origin main"
echo ""
echo "💡 When prompted:"
echo "   Username: gettechthings-del"
echo "   Password: [paste your Personal Access Token]"
echo ""

echo "✅ Current Git configuration:"
echo "   Name: $(git config user.name)"
echo "   Email: $(git config user.email)"
echo "   Remote: $(git remote get-url origin)"
echo ""

echo "🔍 If you still get errors, try:"
echo "   git push https://gettechthings-del:YOUR_TOKEN@github.com/gettechthings-del/dfd.git main"
echo "" 