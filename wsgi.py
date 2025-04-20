#!/usr/bin/env python3
"""
WSGI entry point for the Line Art Coloring Book Generator
"""

import os
from server import app

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
