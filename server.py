#!/usr/bin/env python3
"""
Line Art Coloring Book Generator - Backend Server
This server handles requests from the frontend and communicates with the Stable Diffusion API
to generate line art images for coloring books.
"""

import os
import json
import time
import uuid
import base64
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import zipfile
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
TEMP_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_BATCH_SIZE = 60

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Configure app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# API Configuration
# Get API key from environment variable
STABILITY_API_KEY = os.environ.get('STABILITY_API_KEY', '')
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

# Model configuration mapping
MODEL_CONFIG = {
    'sd_lineart_v1': {
        'api_url': 'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',
        'prompt_prefix': 'line art, coloring book style, black and white, clean lines, ',
        'negative_prompt': 'color, shading, grayscale, noise, texture, watermark, signature, blurry',
        'lora': 'sd_lineart_v1'
    },
    'illuminutty': {
        'api_url': 'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',
        'prompt_prefix': 'line art, coloring book style, black and white outlines, clean lines, illuminutty style, ',
        'negative_prompt': 'color, shading, grayscale, noise, texture, watermark, signature, blurry',
        'lora': 'illuminutty'
    },
    'sahastrakotiXL': {
        'api_url': 'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',
        'prompt_prefix': 'line art, coloring book style, black and white outlines, clean lines, sahastrakoti style, ',
        'negative_prompt': 'color, shading, grayscale, noise, texture, watermark, signature, blurry',
        'lora': 'sahastrakotiXL_v10'
    }
}

# Helper functions
def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(prefix='image', extension='png'):
    """Generate a unique filename with timestamp and UUID"""
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{timestamp}_{unique_id}.{extension}"

def add_margin(image, margin_size):
    """Add a white margin around the image"""
    if margin_size <= 0:
        return image
    
    width, height = image.size
    margin_pixels = int((width * margin_size) / 100)
    
    new_width = width + 2 * margin_pixels
    new_height = height + 2 * margin_pixels
    
    new_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))
    new_image.paste(image, (margin_pixels, margin_pixels))
    
    return new_image

def add_text(image, text, font_name, position):
    """Add text to the image at the specified position"""
    if not text:
        return image
    
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Try to load the font, fall back to default if not available
    try:
        if font_name == 'Arial':
            font = ImageFont.truetype('arial.ttf', size=int(height/20))
        elif font_name == 'Times New Roman':
            font = ImageFont.truetype('times.ttf', size=int(height/20))
        elif font_name == 'Courier New':
            font = ImageFont.truetype('cour.ttf', size=int(height/20))
        elif font_name == 'Georgia':
            font = ImageFont.truetype('georgia.ttf', size=int(height/20))
        else:
            font = ImageFont.load_default()
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text size and position
    try:
        text_width, text_height = draw.textsize(text, font=font)
    except AttributeError:
        # For newer Pillow versions
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    
    if position == 'top':
        text_position = ((width - text_width) // 2, height // 20)
    else:  # bottom
        text_position = ((width - text_width) // 2, height - height // 10)
    
    # Draw text with a white background for better visibility
    text_box = (
        text_position[0] - 5,
        text_position[1] - 5,
        text_position[0] + text_width + 5,
        text_position[1] + text_height + 5
    )
    draw.rectangle(text_box, fill=(255, 255, 255))
    draw.text(text_position, text, fill=(0, 0, 0), font=font)
    
    return image

def adjust_line_thickness(image, thickness):
    """Adjust the line thickness of the image"""
    # This is a simplified implementation
    # In a real application, you would use more sophisticated image processing
    
    # Convert to grayscale
    grayscale = image.convert('L')
    
    # Threshold to create binary image
    threshold = 200  # Adjust as needed
    binary = grayscale.point(lambda p: 0 if p < threshold else 255)
    
    # Apply dilation based on thickness
    from PIL import ImageFilter
    
    # Apply different levels of dilation based on thickness
    if thickness <= 1:
        # No change for thin lines
        processed = binary
    elif thickness == 2:
        # Slight dilation
        processed = binary.filter(ImageFilter.MinFilter(3))
    elif thickness == 3:
        # Medium dilation
        processed = binary.filter(ImageFilter.MinFilter(5))
    elif thickness == 4:
        # Heavy dilation
        processed = binary.filter(ImageFilter.MinFilter(7))
    else:
        # Maximum dilation
        processed = binary.filter(ImageFilter.MinFilter(9))
    
    # Convert back to RGB
    result = Image.new('RGB', image.size, (255, 255, 255))
    result.paste(Image.new('RGB', image.size, (0, 0, 0)), mask=processed)
    
    return result

def call_stability_api(params):
    """Call the Stability AI API to generate an image"""
    logger.info(f"Calling Stability API with params: {params}")
    
    # Get model configuration
    model_config = MODEL_CONFIG.get(params['modelSelection'], MODEL_CONFIG['sd_lineart_v1'])
    
    # Construct the prompt
    base_prompt = f"{model_config['prompt_prefix']}{params['styleDescriptor']}, {params['sceneType']}"
    
    # Prepare API request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}"
    }
    
    payload = {
        "text_prompts": [
            {
                "text": base_prompt,
                "weight": 1.0
            },
            {
                "text": model_config['negative_prompt'],
                "weight": -1.0
            }
        ],
        "cfg_scale": params['guidanceScale'],
        "height": params['resolution'],
        "width": params['resolution'],
        "samples": 1,
        "steps": params['generationSteps']
    }
    
    # Add seed if specified
    if params['seedValue'] != -1:
        payload["seed"] = params['seedValue']
    
    try:
        # Make API request
        response = requests.post(
            model_config['api_url'],
            headers=headers,
            json=payload
        )
        
        # Check for errors
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return None, f"API Error: {response.status_code} - {response.text}"
        
        # Parse response
        response_data = response.json()
        
        # Extract image data
        if 'artifacts' in response_data and len(response_data['artifacts']) > 0:
            image_data = response_data['artifacts'][0]['base64']
            seed = response_data['artifacts'][0]['seed']
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            return image, seed
        else:
            logger.error("No image data in API response")
            return None, "No image data in API response"
            
    except Exception as e:
        logger.error(f"Error calling Stability API: {str(e)}")
        return None, f"Error calling Stability API: {str(e)}"

def process_image(image, params):
    """Apply post-processing to the generated image"""
    if image is None:
        return None
    
    try:
        # Adjust line thickness
        if params['lineThickness'] != 2:  # 2 is default
            image = adjust_line_thickness(image, params['lineThickness'])
        
        # Add margin
        if params['marginSize'] > 0:
            image = add_margin(image, params['marginSize'])
        
        # Add text if enabled
        if params['enableText'] and params['textContent']:
            image = add_text(
                image,
                params['textContent'],
                params['fontSelection'],
                params['textPosition']
            )
        
        return image
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return None

def save_image(image, filename, format='PNG'):
    """Save the image to disk"""
    if image is None:
        return None
    
    try:
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        image.save(filepath, format=format)
        return filepath
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        return None

def create_zip_file(filepaths, zip_filename):
    """Create a ZIP file containing the specified files"""
    zip_filepath = os.path.join(TEMP_FOLDER, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for filepath in filepaths:
                filename = os.path.basename(filepath)
                zipf.write(filepath, filename)
        
        return zip_filepath
    except Exception as e:
        logger.error(f"Error creating ZIP file: {str(e)}")
        return None

# API Routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/generate-preview', methods=['POST'])
def generate_preview():
    """Generate a single preview image"""
    try:
        # Parse request data
        params = request.json
        logger.info(f"Received preview generation request: {params}")
        
        # Call API to generate image
        image, seed = call_stability_api(params)
        
        if image is None:
            return jsonify({'error': seed}), 500
        
        # Process image
        processed_image = process_image(image, params)
        
        if processed_image is None:
            return jsonify({'error': 'Failed to process image'}), 500
        
        # Save image
        filename = generate_unique_filename('preview')
        filepath = save_image(processed_image, filename)
        
        if filepath is None:
            return jsonify({'error': 'Failed to save image'}), 500
        
        # Return image URL and seed
        return jsonify({
            'url': f'/outputs/{filename}',
            'seed': seed
        })
    
    except Exception as e:
        logger.error(f"Error generating preview: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-batch', methods=['POST'])
def generate_batch():
    """Generate a batch of images"""
    try:
        # Parse request data
        params = request.json
        logger.info(f"Received batch generation request: {params}")
        
        # Validate batch size
        batch_size = params.get('batchSize', 1)
        if batch_size < 1 or batch_size > MAX_BATCH_SIZE:
            return jsonify({'error': f'Batch size must be between 1 and {MAX_BATCH_SIZE}'}), 400
        
        # Initialize response
        results = []
        filepaths = []
        
        # Generate images
        for i in range(batch_size):
            # Update seed if using sequential numbering
            if params['sequentialNumbering'] and params['seedValue'] != -1:
                current_params = params.copy()
                current_params['seedValue'] = params['seedValue'] + i
            else:
                current_params = params
            
            # Call API to generate image
            image, seed = call_stability_api(current_params)
            
            if image is None:
                # Log error but continue with batch
                logger.error(f"Failed to generate image {i+1}/{batch_size}: {seed}")
                continue
            
            # Process image
            processed_image = process_image(image, current_params)
            
            if processed_image is None:
                # Log error but continue with batch
                logger.error(f"Failed to process image {i+1}/{batch_size}")
                continue
            
            # Save image
            if params['sequentialNumbering']:
                filename = f"{params['batchName']}_{(i+1):03d}.png"
            else:
                filename = f"{params['batchName']}_{seed}.png"
            
            filepath = save_image(processed_image, filename)
            
            if filepath is None:
                # Log error but continue with batch
                logger.error(f"Failed to save image {i+1}/{batch_size}")
                continue
            
            # Add to results
            results.append({
                'url': f'/outputs/{filename}',
                'seed': seed
            })
            
            filepaths.append(filepath)
            
            # Send progress update
            progress = {
                'current': i + 1,
                'total': batch_size,
                'results': results
            }
            
            # In a real application, you would use WebSockets to send progress updates
            # For now, we'll just log the progress
            logger.info(f"Batch progress: {i+1}/{batch_size}")
        
        # Create ZIP file if requested
        if len(filepaths) > 0 and params.get('createZip', False):
            zip_filename = f"{params['batchName']}.zip"
            zip_filepath = create_zip_file(filepaths, zip_filename)
            
            if zip_filepath:
                results.append({
                    'zipUrl': f'/temp/{zip_filename}'
                })
        
        return jsonify({
            'results': results,
            'completed': len(results),
            'total': batch_size
        })
    
    except Exception as e:
        logger.error(f"Error generating batch: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-zip', methods=['POST'])
def download_zip():
    """Create and download a ZIP file of images"""
    try:
        # Parse request data
        data = request.json
        filenames = data.get('filenames', [])
        zip_name = data.get('zipName', 'images.zip')
        
        if not filenames:
            return jsonify({'error': 'No filenames provided'}), 400
        
        # Create list of file paths
        filepaths = [os.path.join(OUTPUT_FOLDER, filename) for filename in filenames]
        
        # Create ZIP file
        zip_filepath = create_zip_file(filepaths, zip_name)
        
        if zip_filepath is None:
            return jsonify({'error': 'Failed to create ZIP file'}), 500
        
        return jsonify({'zipUrl': f'/temp/{zip_name}'})
    
    except Exception as e:
        logger.error(f"Error creating ZIP file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/outputs/<filename>')
def serve_output(filename):
    """Serve generated images"""
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/temp/<filename>')
def serve_temp(filename):
    """Serve temporary files (like ZIP files)"""
    return send_from_directory(TEMP_FOLDER, filename)

@app.route('/api/status', methods=['GET'])
def api_status():
    """Check API status"""
    try:
        # Check if API key is configured
        if not STABILITY_API_KEY:
            return jsonify({
                'status': 'warning',
                'message': 'API key not configured'
            })
        
        return jsonify({
            'status': 'ready',
            'message': 'API is ready'
        })
    
    except Exception as e:
        logger.error(f"Error checking API status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# For production deployment
if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
