import socket
import json
import tkinter as tk
from tkinter import ttk, messagebox

HOST = "127.0.0.1"
PORT = 59999  

class NewsClient:
    def __init__(self, root):
        self.root = root
        self.root.title("News Client")

        self.sock = None
        self.connected = False
        self.items = []

        # Username
        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.connect_btn = tk.Button(root, text="Connect", command=self.connect)
        self.connect_btn.pack()

        self.status_label = tk.Label(root, text="Not connected", fg="red")
        self.status_label.pack()
        
       # OPTIONS MENU (NEW)
        options_frame = tk.LabelFrame(root, text="Headlines Options")
        options_frame.pack(pady=10)

        tk.Label(options_frame, text="Select Option:").grid(row=0, column=0, padx=5)

        self.option_var = tk.StringVar()
        self.option_menu = ttk.Combobox(
            options_frame,
            textvariable=self.option_var,
            values=[
                "Search for keywords",
                "Search by category",
                "Search by country",
                "List all new headlines"
            ],
            state="readonly",
            width=30
        )
        self.option_menu.grid(row=0, column=1, padx=5)
        self.option_menu.current(0)

        tk.Label(options_frame, text="Value:").grid(row=1, column=0, padx=5)
        self.option_value_entry = tk.Entry(options_frame)
        self.option_value_entry.grid(row=1, column=1, padx=5)

        tk.Button(options_frame, text="Run Search", command=self.run_option_search).grid(row=2, column=0, columnspan=2, pady=5)