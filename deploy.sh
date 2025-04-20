#!/bin/bash
# Deployment script for Line Art Coloring Book Generator

echo "Deploying Line Art Coloring Book Generator..."

# Create necessary directories if they don't exist
mkdir -p uploads outputs temp

# Check if .env file exists, create if not
if [ ! -f .env ]; then
    echo "Creating .env file template..."
    echo "STABILITY_API_KEY=your_stability_ai_api_key_here" > .env
    echo "⚠️ Please update the .env file with your actual Stability AI API key."
fi

# Start the server
echo "Starting the server..."
python3 server.py
