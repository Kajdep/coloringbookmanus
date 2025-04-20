#!/bin/bash
# Test script for Line Art Coloring Book Generator

echo "Testing Line Art Coloring Book Generator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if required Python packages are installed
echo "Checking required Python packages..."
python3 -m pip install flask flask-cors pillow python-dotenv requests

# Create test directories if they don't exist
mkdir -p uploads outputs temp

# Create a test .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating sample .env file (you'll need to update with your actual API key)..."
    echo "STABILITY_API_KEY=your_stability_ai_api_key_here" > .env
    echo "⚠️ Please update the .env file with your actual Stability AI API key."
fi

# Check if server.py exists
if [ ! -f server.py ]; then
    echo "Error: server.py not found."
    exit 1
fi

# Check if index.html exists
if [ ! -f index.html ]; then
    echo "Error: index.html not found."
    exit 1
fi

# Check if styles.css exists
if [ ! -f styles.css ]; then
    echo "Error: styles.css not found."
    exit 1
fi

# Check if script.js exists
if [ ! -f script.js ]; then
    echo "Error: script.js not found."
    exit 1
fi

echo "All required files found."

# Test server startup
echo "Testing server startup..."
python3 -c "import server; print('Server module loaded successfully')"
if [ $? -ne 0 ]; then
    echo "Error: Failed to load server module."
    exit 1
fi

echo "✅ Basic tests passed."
echo ""
echo "To start the application, run:"
echo "python3 server.py"
echo ""
echo "Then open your browser to http://localhost:5000"
echo ""
echo "Note: For full functionality, you need a valid Stability AI API key in the .env file."
