#!/bin/bash

# The Empathy Engine - Premium Setup Script
# This script sets up the best possible voice quality

echo "🎭 Setting up The Premium Empathy Engine..."
echo "================================================"

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  It's recommended to use a virtual environment."
    echo "Create one with: python3 -m venv empathy_env"
    echo "Activate with: source empathy_env/bin/activate"
    echo ""
    read -p "Continue with system installation? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Installing system dependencies..."

# Install system audio dependencies
sudo apt update
sudo apt install -y espeak espeak-data libespeak1 libespeak-dev ffmpeg python3-dev

echo "🐍 Installing Python packages..."

# Install Python packages
if [[ "$VIRTUAL_ENV" != "" ]]; then
    # We're in a virtual environment
    pip install -r requirements_premium.txt
else
    # System installation with --break-system-packages
    pip install --break-system-packages -r requirements_premium.txt
fi

echo "🎤 Testing voice engines..."

# Test the premium engine
python3 empathy_engine_premium.py "Hello! This is a test of the premium voice engine." --engine edge

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage examples:"
echo "  # Best quality (requires internet):"
echo "  python3 empathy_engine_premium.py \"Your text here\" --engine edge"
echo ""
echo "  # Good quality offline after first use:"
echo "  python3 empathy_engine_premium.py \"Your text here\" --engine gtts"
echo ""
echo "  # Basic quality (fully offline):"
echo "  python3 empathy_engine_premium.py \"Your text here\" --engine espeak"
echo ""
echo "  # Run demo:"
echo "  python3 empathy_engine_premium.py --demo --engine edge"
