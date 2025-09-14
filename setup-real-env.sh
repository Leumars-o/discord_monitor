#!/bin/bash
# Linux/Mac setup script for Real Discord bot env

echo "Setting up real_env environment..."
python -m venv real_env
source real_env/bin/activate
pip install -r requirements-real-env.txt
echo "✅ real_env setup complete!"
echo "To activate: source real_env/bin/activate"