#!/bin/bash
# Script to test the authentication system for the Line Art Generator

echo "Testing authentication system for Line Art Generator..."

# Create a test directory
TEST_DIR="auth_test"
mkdir -p $TEST_DIR

# Create a simple test script
cat > $TEST_DIR/test_auth.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for Line Art Generator authentication
"""

import requests
import base64
import sys

def test_with_credentials(url, username, password):
    """Test access with provided credentials"""
    print(f"\nTesting with credentials: {username}:{password}")
    
    # Create auth header
    auth_string = f"{username}:{password}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_b64}'
    }
    
    # Test access
    try:
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Authentication successful - Access granted")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed - Access denied")
            return False
        else:
            print(f"❓ Unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"❗ Error: {str(e)}")
        return False

def test_without_credentials(url):
    """Test access without credentials"""
    print("\nTesting without credentials")
    
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Authentication working - Access correctly denied")
            return True
        elif response.status_code == 200:
            print("❌ Authentication failed - Access incorrectly granted")
            return False
        else:
            print(f"❓ Unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"❗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_auth.py <url> [username] [password]")
        sys.exit(1)
    
    url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else "admin"
    password = sys.argv[3] if len(sys.argv) > 3 else "lineart2025"
    
    print(f"Testing authentication for: {url}")
    
    # Test without credentials
    test_without_credentials(url)
    
    # Test with correct credentials
    test_with_credentials(url, username, password)
    
    # Test with incorrect credentials
    test_with_credentials(url, "wrong_user", "wrong_pass")
EOF

# Make the test script executable
chmod +x $TEST_DIR/test_auth.py

# Create a local test server script
cat > $TEST_DIR/run_test_server.py << 'EOF'
#!/usr/bin/env python3
"""
Test server for Line Art Generator authentication
"""

import os
import sys
import subprocess
import time
import signal
import requests

def start_server(server_file):
    """Start the Flask server"""
    print(f"Starting server with {server_file}...")
    process = subprocess.Popen(
        [sys.executable, server_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(2)
    return process

def stop_server(process):
    """Stop the Flask server"""
    print("Stopping server...")
    process.send_signal(signal.SIGTERM)
    process.wait()

def run_tests(server_url):
    """Run the authentication tests"""
    print(f"Running authentication tests against {server_url}...")
    subprocess.run([sys.executable, "test_auth.py", server_url])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_test_server.py <server_file>")
        sys.exit(1)
    
    server_file = sys.argv[1]
    server_url = "http://localhost:5000"
    
    if not os.path.exists(server_file):
        print(f"Error: Server file {server_file} not found")
        sys.exit(1)
    
    # Start server
    server_process = start_server(server_file)
    
    try:
        # Run tests
        run_tests(server_url)
    finally:
        # Stop server
        stop_server(server_process)
EOF

# Make the test server script executable
chmod +x $TEST_DIR/run_test_server.py

echo "Authentication test scripts created in $TEST_DIR directory"
echo ""
echo "To test the authentication system locally:"
echo "1. cd $TEST_DIR"
echo "2. python run_test_server.py ../server_with_auth.py"
echo ""
echo "To test against a deployed server:"
echo "1. cd $TEST_DIR"
echo "2. python test_auth.py https://your-deployed-app-url.onrender.com [username] [password]"
echo ""
echo "The default credentials are:"
echo "Username: admin"
echo "Password: lineart2025"
