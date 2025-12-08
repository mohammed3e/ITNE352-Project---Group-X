import socket
import json
import tkinter as tk
from tkinter import ttk, messagebox

HOST = "127.0.0.1"
PORT = 59999

# Function to safely receive JSON data from the server.
# The server may send data in multiple chunks, so we store
# the data in a buffer until a full valid JSON object is received.

def recv_json(sock):
    buffer = ""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            return None

        # Try decoding normally, fallback if needed
        try:
            buffer += chunk.decode('utf-8')
        except:
            buffer += chunk.decode('latin-1')

        # Attempt to convert buffer to JSON
        try:
            return json.loads(buffer)
        except json.JSONDecodeError:
            # If JSON is incomplete, continue receiving
            continue


# Main Client GUI Class
# Handles the user interface, communication with server,
# and all client interaction logic.
class NewsClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("News Client - ITNE352 Project")
        self.master.geometry("650x520")

        self.sock = None  # Will hold socket connection to server

        #  User Login Section
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(pady=10)

        tk.Label(self.top_frame, text="Enter your name:", font=("Arial", 11)).grid(row=0, column=0)
        self.username_entry = tk.Entry(self.top_frame, width=25)
        self.username_entry.grid(row=0, column=1, padx=5)

        # Connect button that initializes connection with server
        self.connect_btn = tk.Button(self.top_frame, text="Connect", command=self.connect_to_server)
        self.connect_btn.grid(row=0, column=2, padx=5)

        #  Main Menu Buttons
        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(pady=10)

        self.headlines_btn = tk.Button(self.menu_frame, text="Search Headlines", width=20,
                                       command=self.open_headlines_menu, state="disabled")
        self.sources_btn = tk.Button(self.menu_frame, text="List of Sources", width=20,
                                     command=self.open_sources_menu, state="disabled")
        self.quit_btn = tk.Button(self.menu_frame, text="Quit", width=20,
                                  command=self.quit_app, state="disabled")

        self.headlines_btn.grid(row=0, column=0, padx=5)
        self.sources_btn.grid(row=0, column=1, padx=5)
        self.quit_btn.grid(row=0, column=2, padx=5)

        #  Results Listbox
        # Displays headlines or sources returned from server
        self.results_box = tk.Listbox(master, width=90, height=12)
        self.results_box.pack(pady=10)

        #  Details Text Box
        tk.Label(master, text="Details:", font=("Arial", 11, "bold")).pack()
        self.details_text = tk.Text(master, width=90, height=10)
        self.details_text.pack(pady=5)

    # Establish connection with the server using socket
    # Sends the username and enables menu buttons after connecting.
    def connect_to_server(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showinfo("Error", "Please enter a username.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))

            # Send username to server
            self.sock.sendall(username.encode())

            # Enable menu buttons after successful connection
            self.headlines_btn.config(state="normal")
            self.sources_btn.config(state="normal")
            self.quit_btn.config(state="normal")
            self.connect_btn.config(state="disabled")

            messagebox.showinfo("Connected", "Successfully connected to the server.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    # Open sub-menu for headline search options
    def open_headlines_menu(self):
        menu = tk.Toplevel(self.master)
        menu.title("Headlines Menu")
        menu.geometry("300x260")

        options = [
            ("Search for keywords", self.headlines_option),
            ("Search by category", self.headlines_option),
            ("Search by country", self.headlines_option),
            ("List all new headlines", self.headlines_option),
        ]

        for text, cmd in options:
            tk.Button(menu, text=text, width=25, command=lambda t=text: cmd(t)).pack(pady=5)

        tk.Button(menu, text="Close", command=menu.destroy).pack(pady=10)

    # Handle selected headline search option
    # Sends the required command/value to the server
    def headlines_option(self, option_text):
        self.results_box.delete(0, tk.END)
        self.details_text.delete("1.0", tk.END)

        self.sock.sendall("Search headlines".encode())
        self.sock.sendall(option_text.encode())

        # Options that require user input (keyword, category, country)
        if option_text in ["Search for keywords", "Search by category", "Search by country"]:
            val = self.simple_input(f"Enter value for {option_text}:")
            if not val:
                return
            self.sock.sendall(val.encode())

        # Receive headline results from server
        summary = recv_json(self.sock)

        # If server returned an error message
        if isinstance(summary, dict) and summary.get("error"):
            messagebox.showinfo("Error", summary["error"])
            return

        self.display_list(summary, is_headline=True)

    
    # Open sub-menu for sources search options
    def open_sources_menu(self):
        menu = tk.Toplevel(self.master)
        menu.title("Sources Menu")
        menu.geometry("300x260")

        options = [
            ("Search by category", self.sources_option),
            ("Search by country", self.sources_option),
            ("Search by language", self.sources_option),
            ("List all", self.sources_option),
        ]

        for text, cmd in options:
            tk.Button(menu, text=text, width=25, command=lambda t=text: cmd(t)).pack(pady=5)

        tk.Button(menu, text="Close", command=menu.destroy).pack(pady=10)

    # Handle selected sources option and request data from server
    def sources_option(self, option_text):
        self.results_box.delete(0, tk.END)
        self.details_text.delete("1.0", tk.END)

        self.sock.sendall("List of sources".encode())
        self.sock.sendall(option_text.encode())

        # If option requires a user-entered value
        if option_text in ["Search by category", "Search by country", "Search by language"]:
            val = self.simple_input(f"Enter value for {option_text}:")
            if not val:
                return
            self.sock.sendall(val.encode())

        summary = recv_json(self.sock)

        # Check if server returned an error
        if isinstance(summary, dict) and summary.get("error"):
            messagebox.showinfo("Error", summary["error"])
            return

        self.display_list(summary, is_headline=False)

    # Display items (headlines or sources) in the Listbox
    # Also binds double-click event to show details
    def display_list(self, summary, is_headline):
        self.results_box.delete(0, tk.END)
        
        for idx, item in enumerate(summary, 1):
            if is_headline:
                self.results_box.insert(tk.END, f"{idx}. {item.get('title')} ({item.get('source')})")
            else:
                self.results_box.insert(tk.END, f"{idx}. {item.get('name')}")

        # Bind double-click event to load details
        self.results_box.bind("<Double-1>", lambda event: self.get_details(is_headline))

    # Request the detailed info of one selected item from server
    def get_details(self, is_headline):
        index = self.results_box.curselection()
        if not index:
            return

        idx = index[0] + 1

        # Send index to server to request details
        self.sock.sendall(str(idx).encode())

        details = recv_json(self.sock)
        if not details:
            return

        self.details_text.delete("1.0", tk.END)

        # Format output based on type (headline or source)
        if is_headline:
            source = details.get("source", {})
            if isinstance(source, dict):
                source = source.get("name")

            text = (
                f"Source: {source}\n"
                f"Author: {details.get('author')}\n"
                f"Title: {details.get('title')}\n"
                f"Description: {details.get('description')}\n"
                f"URL: {details.get('url')}\n"
            )

            if details.get("publishedAt"):
                date, time = details["publishedAt"].split("T")
                time = time.replace("Z", "")
                text += f"Published Date: {date}\nPublished Time: {time}\n"

        else:
            text = (
                f"Name: {details.get('name')}\n"
                f"Country: {details.get('country')}\n"
                f"Category: {details.get('category')}\n"
                f"Language: {details.get('language')}\n"
                f"Description: {details.get('description')}\n"
                f"URL: {details.get('url')}\n"
            )

        self.details_text.insert(tk.END, text)

    # Popup window to ask user for a single input value
    # Used for keyword/category/country searches
    def simple_input(self, message):
        top = tk.Toplevel(self.master)
        top.title("Input")
        tk.Label(top, text=message).pack(pady=5)
        entry = tk.Entry(top, width=30)
        entry.pack(pady=5)

        result = {"val": None}

        def submit():
            result["val"] = entry.get().strip()
            top.destroy()

        tk.Button(top, text="OK", command=submit).pack(pady=5)
        top.wait_window()
        return result["val"]

    # Cleanly close the client and notify server
    def quit_app(self):
        if self.sock:
            try:
                self.sock.sendall("EXIT".encode())
            except:
                pass
        self.master.destroy()



# Start GUI Application

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsClientGUI(root)
    root.mainloop()
