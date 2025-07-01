#!/bin/bash

# Auto Deploy and Push Script
# Usage: ./deploy.sh "commit message"

set -e

echo "🚀 Starting auto deploy process..."

# Set default commit message
COMMIT_MSG="${1:-Auto deployment $(date '+%Y-%m-%d %H:%M:%S')}"

echo "📝 Commit message: $COMMIT_MSG"

# Add all changes
echo "📁 Adding changes to git..."
git add -A

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️ No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "$COMMIT_MSG"
fi

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
if command -v vercel &> /dev/null; then
    vercel --prod --yes
elif [ -f "./node_modules/.bin/vercel" ]; then
    ./node_modules/.bin/vercel --prod --yes
else
    echo "❌ Vercel CLI not found. Installing..."
    npm install vercel
    ./node_modules/.bin/vercel --prod --yes
fi

# Set alias for short URL
echo "🔗 Setting up short URL alias..."
if command -v vercel &> /dev/null; then
    vercel alias set kigyou-lab.vercel.app
elif [ -f "./node_modules/.bin/vercel" ]; then
    ./node_modules/.bin/vercel alias set kigyou-lab.vercel.app
fi

# Push to GitHub (if changes were committed)
if ! git diff --staged --quiet || [ "$(git log --oneline -1)" != "$(git log --oneline -1 origin/main 2>/dev/null || echo '')" ]; then
    echo "📤 Pushing to GitHub..."
    git push origin main
    echo "✅ Successfully pushed to GitHub"
else
    echo "ℹ️ No new commits to push"
fi

echo "🎉 Deploy process completed!"
echo "🌐 Live URL: https://kigyou-lab.vercel.app"
echo "📊 Dashboard: https://vercel.com/mokayamos-projects/kigyou-lab-final-main"