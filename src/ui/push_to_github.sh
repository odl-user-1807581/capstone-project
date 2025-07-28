#!/bin/bash
# Git push script (no secrets in file)
git add .
git commit -m "Auto-commit: HTML code approved and deployed"
git push origin main
echo "Code pushed to GitHub successfully!"
