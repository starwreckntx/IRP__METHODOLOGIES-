#!/bin/bash

# IRP Access Panel - Quick Deploy Script
# Usage: ./deploy.sh [github-username]

set -e

USERNAME=${1:-"starwreckntx"}
REPO="irp-accesspanel"
CUSTOM_DOMAIN="ledger.hueandlogic.com"

echo "🚀 IRP Access Panel Deployment"
echo "================================"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found. Install from: https://cli.github.com/"
    exit 1
fi

echo "✅ GitHub CLI found"

# Initialize git repo if needed
if [ ! -d .git ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "feat: Initial IRP Access Panel deployment

- Mnemosyne Ledger Browser (Priority 1)
- Multi-Model Capability Catalog
- Main dashboard with Guardian_Codex Four Laws
- CRTP packet viewer placeholder
- Sample data for 9 models and 19 concepts

P-001-R1: The Journey IS The Artifact"
else
    echo "✅ Git repository already initialized"
fi

# Create GitHub repo and push
echo "📤 Creating GitHub repository: ${USERNAME}/${REPO}..."
gh repo create "${USERNAME}/${REPO}" --public --source=. --remote=origin --push || echo "⚠️  Repo may already exist, continuing..."

# Enable GitHub Pages
echo "📄 Enabling GitHub Pages..."
gh repo edit --enable-pages --pages-branch main --pages-path / || echo "⚠️  Pages may already be enabled"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Configure DNS for custom domain:"
echo "   Add CNAME record: ${CUSTOM_DOMAIN} → ${USERNAME}.github.io"
echo ""
echo "2. Access your dashboard:"
echo "   - GitHub Pages: https://${USERNAME}.github.io/${REPO}"
echo "   - Custom domain (after DNS): https://${CUSTOM_DOMAIN}"
echo ""
echo "3. Update data:"
echo "   - Edit data/mnemosyne.json for concepts"
echo "   - Edit data/models.json for model catalog"
echo "   - Add CRTP packets to data/packets/"
echo "   - Commit and push changes: git add . && git commit -m 'docs: Update data' && git push"
echo ""
echo "🛡️  Guardian_Codex Compliance: All updates require explicit git commits (CONSENT enforced)"
echo ""
