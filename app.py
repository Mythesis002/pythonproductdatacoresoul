from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS library
import cloudinary
import cloudinary.uploader
from gradio_client import Client, handle_file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up Cloudinary credentials
cloudinary.config(
    cloud_name="dkr5qwdjd",
    api_key="797349366477678",
    api_secret="9HUrfG_i566NzrCZUVxKyCHTG9U"
)

# Initialize Gradio client
client = Client("ChrisJohnson111/test4")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Retrieve the cloth image URL from the form data
    cloth_img_url = request.form.get('cloth')
    if not cloth_img_url:
        return jsonify({'error': 'No cloth image URL provided'}), 400

    try:
        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(file, folder="Mythesis_images")
        if 'secure_url' in upload_result:
            image_url = upload_result['secure_url']
            
            print("Uploaded Image URL:", image_url)
            print("Cloth Image URL:", cloth_img_url)

            # Ensure the predict function parameters match your Gradio setup
            result = client.predict(
                dict={"background": handle_file(image_url), "layers": [], "composite": None},
                garm_img=handle_file(cloth_img_url),
                garment_des="Hello!!",
                is_checked=True,
                is_checked_crop=False,
                denoise_steps=30,
                seed=42,
                api_name="/tryon"
            )

            processed_image_stream = result[0]  # Adjust based on actual Gradio output

            # Upload the processed image directly to Cloudinary
            processed_upload_result = cloudinary.uploader.upload(
                processed_image_stream,
                folder="Mythesis_images",
                public_id="processed_image",
                overwrite=True
            )

            if 'secure_url' in processed_upload_result:
                processed_image_url = processed_upload_result['secure_url']
                return jsonify({'processedImageUrl': processed_image_url}), 200
            else:
                return jsonify({'error': 'Failed to upload processed image to Cloudinary'}), 500
        else:
            return jsonify({'error': 'Failed to upload image to Cloudinary'}), 500
    except Exception as e:
        print(f"Exception occurred: {e}")  # Print exception for debugging
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
