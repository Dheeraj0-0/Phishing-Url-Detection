#!/bin/bash
echo "🐍 Starting custom startup.sh"
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt --target="./.python_packages/lib/site-packages"

echo "🚀 Launching Gunicorn server..."
PYTHONPATH="./.python_packages/lib/site-packages" gunicorn app:app --bind=0.0.0.0:8000
