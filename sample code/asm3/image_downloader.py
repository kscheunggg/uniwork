import time
import json
import redis
import requests
import base64


# Function to download and encode the image
def download_image(url):
    try:
    
        # Download the image
        response = requests.get(url)
        response.raise_for_status()
        
        # Encode the image data to base64
        encoded_image = base64.b64encode(response.content).decode("utf-8")
        
        return encoded_image
        
    except Exception as e:
        print("Error downloading image:", str(e))
        return None

# Continuously receive messages from the "download" queue
while True:
        
    # Receive message from the "download" queue
    message = r.brpop("download")
    data = json.loads(message[1])
    
    # Get the timestamp and URL from the received message
    timestamp = data["timestamp"]
    url = data["url"]
   
    # Download the image
    image_data = download_image(url)
    
    if image_data is not None:
        # Create the message for the "image" queue
        message = {
        "timestamp": timestamp,
        "url": url,
        "image": image_data
        }
        
        # Submit the message to the "image" queue
        r.lpush("image", json.dumps(message))