# Line Art Coloring Book Generator - Requirements

## API Keys Required

To use this application, you'll need to obtain an API key from Stability AI:

1. Visit [Stability AI](https://stability.ai/) and create an account
2. Navigate to your account dashboard and generate an API key
3. Copy the API key for configuration

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher (for development only)
- pip (Python package manager)

### Backend Setup

1. Clone the repository or download the source code
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required Python packages:
   ```
   pip install flask flask-cors pillow python-dotenv requests
   ```
4. Create a `.env` file in the root directory with your API key:
   ```
   STABILITY_API_KEY=your_stability_ai_api_key_here
   ```

### Running the Application

1. Start the backend server:
   ```
   python server.py
   ```
   This will start the Flask server on http://localhost:5000

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage Instructions

### Basic Usage

1. Select "Office Interior" from the Scene Type dropdown
2. Adjust the style description if needed (default is "Apple + Severance diorama style")
3. Set your desired batch size (between 1-60 images)
4. Click "Generate Preview" to see a sample image
5. Once satisfied with the preview, click "Generate Batch" to create multiple images
6. Download individual images or the entire batch as a ZIP file

### Advanced Options

- **Line Properties**: Adjust thickness and style of the line art
- **Margins**: Set the white space around the image (as percentage)
- **Text Options**: Add custom text to the top or bottom of images
- **Resolution**: Choose between 512x512, 768x768, or 1024x1024 pixels
- **Model Selection**: Choose between different line art models:
  - SD LineArt v1 (default)
  - Illuminutty Diffusion
  - SahastrakotiXL v10
- **Guidance Scale**: Control how closely the image follows your prompt (7 is default)
- **Generation Steps**: Control the number of diffusion steps (more steps = more detail but slower generation)

## Troubleshooting

- If images fail to generate, check your API key configuration
- For large batch sizes, ensure you have sufficient API credits
- If the application seems unresponsive during batch generation, be patient as high-resolution images take longer to generate
- Check the server logs (server.log) for detailed error messages

## Credits

This application uses the following technologies:
- Stability AI API for image generation
- Flask for the backend server
- Bootstrap for the frontend UI
- Various open-source libraries for image processing
