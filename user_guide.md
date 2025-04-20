# Line Art Coloring Book Image Generator - User Guide

## Overview

This application allows you to create line art coloring book images in a 1:1 aspect ratio with a focus on office interiors in Apple + Severance diorama style. The generator features a straightforward user interface and supports batch processing of 45-60 images at once.

## Features

- **Clean Line Art Generation**: Creates black and white line art suitable for coloring books
- **Batch Processing**: Generate up to 60 images in a single batch
- **Customization Options**:
  - Line thickness adjustment
  - Text addition with font selection
  - Resolution control (512x512, 768x768, 1024x1024)
  - Margin size adjustment
- **Multiple Model Options**:
  - SD LineArt v1 (default)
  - Illuminutty Diffusion
  - SahastrakotiXL v10
- **Preview Functionality**: Test settings before generating full batches
- **Batch Gallery**: View and manage all generated images
- **Export Options**: Download individual images or entire batches as ZIP files

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Stability AI API key
- Modern web browser (Chrome, Firefox, Safari, or Edge)

### Installation

1. Clone or download the application files to your local machine
2. Install required dependencies:
   ```
   pip install flask flask-cors pillow python-dotenv requests
   ```
3. Create a `.env` file in the root directory with your API key:
   ```
   STABILITY_API_KEY=your_stability_ai_api_key_here
   ```
4. Run the deployment script:
   ```
   ./deploy.sh
   ```
5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Using the Application

### Basic Workflow

1. **Configure Settings**: Set your desired parameters in the control panel
2. **Generate Preview**: Click the "Generate Preview" button to test your settings
3. **Adjust Parameters**: Fine-tune settings based on the preview result
4. **Generate Batch**: Click "Generate Batch" to create multiple images
5. **View Results**: Browse generated images in the batch gallery
6. **Download**: Save individual images or download all as a ZIP file

### Control Panel Options

#### Theme Selection
- **Scene Type**: Choose the type of scene to generate (default: Office Interior)
- **Style Description**: Describe the visual style (default: Apple + Severance diorama style)

#### Batch Processing
- **Batch Size**: Number of images to generate (1-60)
- **Batch Name**: Prefix for filenames
- **Sequential Numbering**: Use sequential numbers in filenames

#### Image Customization
- **Dimensions**: Select resolution (512x512, 768x768, 1024x1024)
- **Line Properties**:
  - **Line Thickness**: Adjust from thin to thick
  - **Line Style**: Choose between clean, sketchy, detailed, or minimal
- **Margins**: Set white space around the image (0-15%)
- **Text Options**:
  - Enable/disable text
  - Text content
  - Font selection
  - Position (top or bottom)

#### Advanced Options
- **Seed Value**: Control randomness (-1 for random)
- **Model Selection**: Choose the AI model
- **Guidance Scale**: Control adherence to prompt (1-20)
- **Generation Steps**: Control detail level (20-100)

## Tips for Best Results

1. **Start with a Preview**: Always generate a preview before committing to a full batch
2. **Adjust Line Thickness**: Thinner lines work better for detailed scenes, thicker for simpler designs
3. **Optimize Resolution**: Higher resolutions (1024x1024) provide more detail but take longer to generate
4. **Experiment with Models**: Different models produce different line art styles
5. **Use Descriptive Style Text**: Be specific in your style description for better results
6. **Batch Naming**: Use descriptive batch names to organize your generated images

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Ensure your Stability AI API key is correctly entered in the .env file
   - Verify your API key has sufficient credits

2. **Generation Failures**:
   - Check server logs for specific error messages
   - Try reducing batch size or resolution
   - Ensure you have a stable internet connection

3. **Slow Generation**:
   - Higher resolutions and step counts increase generation time
   - Large batch sizes will take proportionally longer

4. **Image Quality Issues**:
   - Adjust guidance scale for better adherence to style
   - Increase generation steps for more detailed results
   - Try different models for varied line art styles

### Getting Help

If you encounter issues not covered in this guide, check the server logs (server.log) for detailed error messages or consult the Stability AI documentation for API-specific issues.

## Technical Details

This application uses:
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **Backend**: Python Flask server
- **Image Generation**: Stability AI API (Stable Diffusion)
- **Image Processing**: Python Pillow library

## License and Credits

- Stability AI for the image generation API
- Bootstrap for the frontend framework
- Flask for the backend server
- Various open-source libraries for image processing

---

*This application was created based on user requirements for a line art coloring book image generator with batch processing capabilities.*
