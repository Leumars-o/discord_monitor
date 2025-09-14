#!/bin/bash
# Linux/Mac setup script for self_bot env

echo "Setting up self_env environment..."
python -m venv self_env
source self_env/bin/activate
pip install -r requirements-self-env.txt
echo "✅ self_env setup complete!"
echo "To activate: source self_env/bin/activate"