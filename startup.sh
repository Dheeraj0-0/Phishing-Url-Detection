#!/bin/bash
echo "📦 Installing packages..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --target="./.python_packages/lib/site-packages"

echo "🚀 Starting app..."
PYTHONPATH="./.python_packages/lib/site-packages" gunicorn app:app --bind=0.0.0.0:8000
