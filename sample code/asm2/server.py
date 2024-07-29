import socket
import threading
import queue
import json
import base64
from PIL import Image
import numpy as np
import tensorflow as tf

# Pre-load the pre-trained Inception V3 model
# You will need to replace this with your own model loading code
# model = tf.keras.applications.InceptionV3(weights='imagenet')
model = tf.keras.applications.ResNet50(
    include_top=True,
    weights="imagenet",
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation="softmax",
)
preprocess_input = tf.keras.applications.resnet50.preprocess_input(image, data_format = None)

preds = model_resnet50.predict(image_batch)

queue = queue.Queue() # Create a queue to pass client sockets from the main thread to the second thread

def listen_connections(): # Thread 1 - Listening for Incoming Connections

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
    server_address = ('localhost', 5000) # Bind the server address and port
    server_socket.bind(server_address)
    server_socket.listen(5) # Listen for incoming connections
    
    while True:
        client_socket, address = server_socket.accept() # Accept a client connection
        queue.put(client_socket) # Pass the client socket to the second thread

def communicate_clients(): # Thread 2 - Communicating with Clients
    while True:
        client_socket = queue.get() # Get the client socket from the queue
        
        try:
            message = sock.recv(1024).decode() # Receive data from the server
            # Check if the message is fully received
            if '##END##' in message:
                response += message.split('##END##')[0]
                break
            response += message # Read the message from the client
            
            data = json.loads(message) # Decode the JSON data
            image_data = base64.b64decode(data['image_data']) # Decode the base64-encoded image data
            image = Image.open(io.BytesIO(image_data)) # Create an image object from the decoded data
            image = tf.expand_dims(image, axis = 0) #required
            image = preprocess_input(image) # Pre-process the image to fit the model
            predictions = model.predict(image) # Perform inference on the image using the pre-trained model
            # Get the predicted classes and probabilities
            top_predictions = tf.keras.applications.imagenet_utils.decode_predictions(predictions, top=5)[0]
            predicted_classes = [label for (_, label, _) in top_predictions]
            probabilities = [prob for (_, _, prob) in top_predictions]
            
            response = {'classes' : {predicted_classes}, 'probabilities': {probabilities}} # Create a response dictionary inclusing classes and probabilities
            json_response = json.dumps(response) # Convert the response to a JSON-encoded string
            message = json_response + '##END##'
            client_socket.sendall(message.encode()) # Send the response back to the client
        finally:
            client_socket.close() # Close the client socket
            
# Create and start the threads
listen = threading.Thread(target = listen_connections, args=(queue,))
communicate = threading.Thread(target = communicate_clients, args=(queue,))

listen.start()
communicate.start()

listen.join()
communicate.join()