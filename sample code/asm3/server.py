from flask import Flask, request, jsonify
import json
import redis
import uuid

app = Flask(__name__)
r = redis.Redis() # Create Redis connection

@app.route("/process", methods=["POST"])
def process_request():
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    # Check if URL or image file is provided in the request
    if "url" in request.form:
        url = request.form["url"] # Extract the URL from the request
        
        message = {
        "timestamp": str(datetime.now()),
        "url": url
        } # Create a message for the "download" queue
       
        r.lpush("download", json.dumps(message)) # Push the message to the "download" queue
 
    elif "image" in request.files:
        image_file = request.files["image"] # Extract the uploaded image file from the request
        image_data = image_file.read() # Read the image data
        encoded_image = base64.b64encode(image_data).decode("utf-8") # Encode the image data to base64
        
        message = {
        "timestamp": str(datetime.now()),
        "url": "uploaded_image",
        "image": encoded_image
        } # Create a message for the "image" queue
        
        r.lpush("image", json.dumps(message)) # Push the message to the "image" queue
    
    else:
        # Return error response if URL or image file is not provided
        return jsonify({"error": "URL or image file not provided"}), 400
       
        # Return the task ID as the response
        return jsonify({"task_id": task_id}), 200
        
if __name__ == "__main__":
    app.run(host="localhost", port=5000)