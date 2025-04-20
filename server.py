            
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
