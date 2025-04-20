#!/bin/bash
# Script to prepare files for Render.com deployment

echo "Preparing files for Render.com deployment..."

# Create a deployment directory
DEPLOY_DIR="line_art_generator_deploy"
mkdir -p $DEPLOY_DIR

# Copy all necessary files to the deployment directory
echo "Copying files to deployment directory..."
cp index.html $DEPLOY_DIR/
cp styles.css $DEPLOY_DIR/
cp script.js $DEPLOY_DIR/
cp server.py $DEPLOY_DIR/
cp wsgi.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/
cp runtime.txt $DEPLOY_DIR/
cp Procfile $DEPLOY_DIR/

# Create necessary directories in the deployment folder
mkdir -p $DEPLOY_DIR/uploads
mkdir -p $DEPLOY_DIR/outputs
mkdir -p $DEPLOY_DIR/temp

# Create a README file
cat > $DEPLOY_DIR/README.md << 'EOF'
# Line Art Coloring Book Generator

A web application that generates line art coloring book images with a focus on office interiors in Apple + Severance diorama style.

## Features

- Clean line art generation for coloring books
- Batch processing of up to 60 images
- Customization options for line thickness, text, resolution, and margins
- Multiple model options for different line art styles

## Deployment

This application is configured for deployment on Render.com.

### Requirements

- Stability AI API key

### Environment Variables

- `STABILITY_API_KEY`: Your Stability AI API key

## Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python wsgi.py`
3. Access at http://localhost:5000
EOF

# Create a .gitignore file
cat > $DEPLOY_DIR/.gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# Environment variables
.env

# Logs
*.log

# Generated files
uploads/*
outputs/*
temp/*
!uploads/.gitkeep
!outputs/.gitkeep
!temp/.gitkeep
EOF

# Create empty .gitkeep files to preserve directory structure
touch $DEPLOY_DIR/uploads/.gitkeep
touch $DEPLOY_DIR/outputs/.gitkeep
touch $DEPLOY_DIR/temp/.gitkeep

# Create a ZIP file for manual upload to Render
echo "Creating ZIP file for deployment..."
zip -r line_art_generator_deploy.zip $DEPLOY_DIR

echo "Deployment package created: line_art_generator_deploy.zip"
echo "You can now deploy this package to Render.com following the instructions in render_deployment.md"
