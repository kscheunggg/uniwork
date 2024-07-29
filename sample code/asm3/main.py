import threading
import time
import json
import redis

# Create Redis connection
r = redis.Redis()

# Function to prompt user for image URL
def prompt_user():

    while True:
        url = input("Enter the Image URL: ")
        if url.startswith("http://") or url.startswith("https://"):
            # Create message
            message = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "url": url,
                "predictions": listen_predictions.data["predictions"] # Replace it with the object recognition results
            }
            r.lpush("download", json.dumps(message))

# Function to listen for predictions
def listen_predictions():
    while True:
        # Listen for message from prediction queue
        message = r.blpop("prediction")
        data = json.loads(message[1])
        
        # Print results on the screen
        print("Timestamp:", data["timestamp"])
        print("URL:", data["url"])
        print("Predictions:", data["predictions"])
        print()
        
# Create and start threads
if __name__ == "__main__":
    prompt_thread = threading.Thread(target=prompt_user)
    prediction_thread = threading.Thread(target=listen_predictions)
   
    prompt_thread.start()
    prediction_thread.start()