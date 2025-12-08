import socket  
import json    
from tkinter import Tk, simpledialog, messagebox  

HOST = '127.0.0.1'  
PORT = 59999 
root = Tk()
root.withdraw()  # Hide the main Tkinter window

# Function to receive JSON data from the server safely
def recv_json(sock):
    buffer = ""
    while True:
        chunk = sock.recv(4096)  # Receive data in chunks
        if not chunk:
            if buffer == "":
                return None
            try:
                return json.loads(buffer)  # Try to parse JSON
            except:
                return None
        try:
            buffer += chunk.decode('utf-8')  # Decode using UTF-8
        except:
            buffer += chunk.decode('latin-1')  # Fallback decoding
        try:
            return json.loads(buffer)  # Return JSON if valid
        except json.JSONDecodeError:
            continue  # Wait for more data if incomplete

 