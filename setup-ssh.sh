#!/bin/bash

echo "🔑 SSH Authentication Setup"
echo "=========================="

echo ""
echo "📋 This will set up SSH authentication for GitHub"
echo ""

# Check if SSH key already exists
if [ -f ~/.ssh/id_ed25519 ]; then
    echo "✅ SSH key already exists"
    echo "Public key:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "📋 Add this key to GitHub:"
    echo "1. Go to: https://github.com/settings/keys"
    echo "2. Click 'New SSH key'"
    echo "3. Paste the key above"
    echo "4. Click 'Add SSH key'"
    echo ""
else
    echo "🔑 Generating new SSH key..."
    ssh-keygen -t ed25519 -C "gettechthings-del@github.com" -f ~/.ssh/id_ed25519 -N ""
    
    echo "✅ SSH key generated"
    echo "Public key:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "📋 Add this key to GitHub:"
    echo "1. Go to: https://github.com/settings/keys"
    echo "2. Click 'New SSH key'"
    echo "3. Paste the key above"
    echo "4. Click 'Add SSH key'"
    echo ""
fi

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

echo "🚀 Now let's update the remote URL to use SSH:"
git remote set-url origin git@github.com:gettechthings-del/dfd.git

echo "✅ Remote URL updated to SSH"
echo ""
echo "🚀 Now try pushing:"
echo "   git push origin main"
echo "" 