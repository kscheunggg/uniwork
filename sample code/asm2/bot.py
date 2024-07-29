import socket
import base64
from io import BytesIO
import telepot
from telepot.loop import MessageLoop
import urllib.request
import threading
import time
import queue
import json
from PIL import Image


# Create Queues
queue1 = queue.Queue() # For passing image and chat_id from Thread 1 to Thread 2
queue2 = queue.Queue()

# Thread 1 - Receiving Messages
def receive_messages(queue1):
    while True:
        # Receive message from Telegram
        # Check if the message contains an image or URL
        def handle(msg):
        
            content_type, chat_type, chat_id = telepot.glance(msg)
            if content_type == 'text':
                link = msg['text']
                urllib.request.urlretrieve(link, 'file.png')
                image = Image.open('file.png') 
            if content_type == 'photo':
                bot.download_file(msg['photo'][-1]['file_id'], 'file.png')
                image = Image.open('file.png') 
    
        # If it does, extract the image and chat_id
        queue1.put((image, chat_id)) # Put the image and chat_id into queue1

# Thread 2 - Client Thread
def send_images(queue1, queue2): 
    while True:
        image, chat_id = queue1.get() # Get the image and chat_id from queue1
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        encoded_image = base64.b64encode(buffered.getvalue())
                
        # Create a TCP socket and send the image data and chat_id to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        data = {
            'image' : encoded_image,
            'chat_id' : chat_id
        } # Create a dictionary containing the image data and chat_id
        
        json_data = json.dumps(data) # Convert the dictionary to a JSON-encoded string
        message = json_data + '##END##' # Append a special string to delimit the message
        sock.sendall(message.encode()) # Send the message to the server
        
        # Receive the response from the server
        response = ''
        while True:
            data = sock.recv(1024).decode() # Receive data from the server
            # Check if the message is fully received
            if '##END##' in data:
                response += data.split('##END##')[0]
                break
            response += data
        sock.close() # Close the socket
        queue2.put(response) # Put the response into queue2

# Thread 3 - Sending messages

def handle(queue2):
    
    reply = queue2.get()
    
    # Send the predicted sentiment and probability back to the user
    bot.sendMessage(chat_id, reply)

if __name__ == "__main__":
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    bot = telepot.Bot("6528697947:AAEhVb5_vDMmaZkYUlRIeEohK3j7Nj8EOCs")
    MessageLoop(bot, handle).run_as_thread()
    # while True:
    # # Something else to do in the main thread
    #     time.sleep(10)

# Create and start the threads
receive_messages = threading.Thread(target = receive_messages, args=(queue1,))
send_images = threading.Thread(target = send_images, args=(queue1, queue2))
handle = threading.Thread(target = handle, args=(queue2,))

receive_messages.start()
send_images.start()
handle.start()

receive_messages.join()
send_images.join()
handle.join()