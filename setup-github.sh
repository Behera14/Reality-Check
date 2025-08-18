#!/bin/bash

echo "🔐 GitHub Authentication Setup"
echo "=============================="

echo ""
echo "📋 Steps to create Personal Access Token:"
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

read -p "Have you created the token? (y/n): " token_created

if [ "$token_created" = "y" ]; then
    echo ""
    echo "🔑 Now let's configure Git to use the token:"
    echo ""
    
    # Configure Git credentials
    git config --global credential.helper store
    
    echo "✅ Git credential helper configured"
    echo ""
    echo "🚀 Now try pushing again:"
    echo "   git push origin main"
    echo ""
    echo "💡 When prompted:"
    echo "   Username: gettechthings-del"
    echo "   Password: [paste your Personal Access Token]"
    echo ""
else
    echo ""
    echo "❌ Please create the token first, then run this script again."
    echo ""
fi 