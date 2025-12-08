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

# Function to get input from user via GUI
def gui_input(prompt):
    while True:
        res = simpledialog.askstring("A1", prompt)
        if res:
            return res  # Return input if provided

 # Function to show headlines and handle headline-related operations
def show_headlines(soc):
    soc.sendall("Search headlines".encode())  # Tell server we want headlines
    options = {
        "1": "Search for keywords",
        "2": "Search by category",
        "3": "Search by country",
        "4": "List all new headlines",
        "5": "Back to the main menu"
    }
    while True:
        choice = gui_input(
            "Headlines Menu:\n1- Search for keywords\n2- Search by category\n3- Search by country\n4- List all new headlines\n5- Back to main menu"
        )
        option_text = options.get(choice)
        if not option_text:
            messagebox.showinfo("A1", "Invalid option")
            continue
        if option_text == "Back to the main menu":
            break

        soc.sendall(option_text.encode())  # Send chosen option to server
        value = None
        if option_text in ["Search for keywords", "Search by category", "Search by country"]:
            value = gui_input(f"Enter value for {option_text}")  # Ask for search term
            soc.sendall(value.encode())

        summary = recv_json(soc)  # Get results from server
        if summary is None:
            messagebox.showinfo("A1", "Server closed connection or invalid response.")
            return
        if isinstance(summary, dict) and summary.get("error"):
            messagebox.showinfo("A1", f"Error: {summary['error']}")
            continue
