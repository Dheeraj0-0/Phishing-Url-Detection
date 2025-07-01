#!/bin/bash
echo "📦 Installing packages..."
pip install --upgrade pip
pip install -r requirements.txt --target="./.python_packages/lib/site-packages"

echo "🚀 Launching Gunicorn on port 8000..."
PYTHONPATH="./.python_packages/lib/site-packages" gunicorn app:app --bind=0.0.0.0:8000
