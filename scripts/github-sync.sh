#!/bin/bash
REPO_URL="https://github.com/starwreckntx/sovereign-ai-hub.git"
BRANCH="main"

if [ ! -d ".git" ]; then git init && git remote add origin $REPO_URL; fi

sync() {
    git fetch origin 2>/dev/null
    git merge origin/$BRANCH --no-edit 2>/dev/null || true
    git add -A
    git commit -m "Auto-sync: $(date +"%Y-%m-%d %H:%M:%S")" 2>/dev/null || echo "No changes"
    git push origin $BRANCH 2>/dev/null || echo "Push failed"
}

watch() { while true; do sync; sleep 60; done; }

case "$1" in sync) sync ;; watch) watch ;; *) echo "Usage: $0 {sync|watch}" ;; esac
