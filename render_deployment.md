# Render.com Deployment Instructions

## Overview
This document provides step-by-step instructions for deploying the Line Art Coloring Book Generator to Render.com for permanent hosting.

## Prerequisites
- A Render.com account (free tier is sufficient)
- A GitHub account (optional, for repository-based deployment)
- Stability AI API key

## Deployment Steps

### Option 1: Deploy from GitHub Repository

1. **Create a GitHub Repository**
   - Create a new repository on GitHub
   - Push all project files to the repository
   - Ensure the repository includes:
     - `index.html`, `styles.css`, `script.js` (frontend)
     - `server.py`, `wsgi.py` (backend)
     - `requirements.txt`, `runtime.txt`, `Procfile` (configuration)

2. **Create a Web Service on Render.com**
   - Log in to your Render.com account
   - Click "New" and select "Web Service"
   - Connect your GitHub account and select the repository
   - Configure the service:
     - Name: `line-art-generator` (or your preferred name)
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn wsgi:app`
   - Add environment variable:
     - Key: `STABILITY_API_KEY`
     - Value: Your Stability AI API key
   - Select the free instance type
   - Click "Create Web Service"

### Option 2: Manual Deployment

1. **Create a Web Service on Render.com**
   - Log in to your Render.com account
   - Click "New" and select "Web Service"
   - Choose "Deploy from file upload" option
   - Upload a ZIP file containing all project files
   - Configure the service as described in Option 1

## Verifying Deployment

1. Once deployment is complete, Render will provide a URL for your application
   (typically `https://line-art-generator.onrender.com` or similar)

2. Open the URL in your browser to verify the application is working correctly

3. Test the application by:
   - Generating a preview image
   - Creating a small batch of images
   - Downloading generated images

## Troubleshooting

If you encounter issues with the deployment:

1. **Check Render Logs**
   - Go to your Web Service dashboard
   - Click on "Logs" to view deployment and runtime logs
   - Look for error messages that might indicate the problem

2. **Common Issues**
   - **API Key**: Ensure the STABILITY_API_KEY environment variable is set correctly
   - **Dependencies**: Check if all required packages are listed in requirements.txt
   - **Port Configuration**: Ensure the application is listening on the port provided by Render

3. **Application Errors**
   - If the application deploys but doesn't function correctly, check browser console for JavaScript errors
   - Verify that API endpoints are accessible from the deployed URL

## Updating Your Application

To update your deployed application:

1. **For GitHub-based deployments**:
   - Push changes to your GitHub repository
   - Render will automatically detect changes and redeploy

2. **For manual deployments**:
   - Go to your Web Service dashboard
   - Click "Manual Deploy" and select "Clear build cache & deploy"

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Deployment Guide](https://render.com/docs/deploy-flask)
- [Environment Variables Guide](https://render.com/docs/environment-variables)
