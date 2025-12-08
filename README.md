# ITNE352 Project - Group GC11

---

## Project Description
This project implements a Python-based client-server system that exchanges information about current news. The server retrieves news updates from [NewsAPI.org](https://newsapi.org/) and handles multiple client connections simultaneously using multithreading. Clients can search headlines and sources by keyword, category, country, or language, and request detailed information on selected items. The project emphasizes network communication, API integration, and proper coding practices.

---

## Semester
2025-2025-1

---

## Group
- **Group Name:** GC11  
- **Course Code:** ITNE352  
- **Section:** 3 
- **Student Name:** Mohammed Abdulghani Mohammed  
- **Student ID:** 202308038  
- **Student Name:** Ahmed Mohammed Omar  
- **Student ID:** 202307323
- **Student Name:** Ahmed Mohammed Amin Alsalim 
- **Student ID:** 202307672

---

## Table of Contents
1. [Project Description](#project-description)  
2. [Semester](#semester)  
3. [Group](#group)  
4. [Requirements](#requirements)  
5. [How to](#how-to)  
6. [The Scripts](#the-scripts)  
7. [Additional Concept](#additional-concept)  
8. [Acknowledgments](#acknowledgments)  
9. [Conclusion](#conclusion)  
10. [Resources](#resources)  

---

## Requirements
To set up and run this project locally
First Install:
1- Python: Install it from Python.org
2- Requests: pip install requests

And Get a API Key from NewsAPI.org.  



## How to
1. Running the Server

To start the server, run the following command:

python server.py


The server will start listening for incoming client connections.

Once a client connects, the server will display the client's name and all received requests.

2. Running the Client

To start the client:

python client.py

3. Interaction Steps

Enter your username (this name will be displayed on the server side).

Choose between:

Search Headlines

List of Sources

Quit

Inside each menu, you will find multiple search options such as:

search by keyword

search by category

search by country

search by language

After receiving a list the user may:

Select an item to get detailed information

Go back to the previous menu

Quit


## The Scripts

server.py

Main Functionalities

The server:

Accepts and manages multiple clients using multithreading

Receives search requests (headlines or sources)

Fetches news from NewsAPI

Sends JSON responses back to the client

Saves results into JSON files

Key Functions in server.py
1. fetch_headlines(param_name=None, param_value=None)

Fetches top headlines based on keyword, category, or country.

def fetch_headlines(param_name=None, param_value=None):
    url = f"https://newsapi.org/v2/top-headlines?{param_name}={param_value}&pageSize=15&apiKey={NEWSAPI_KEY}"


Purpose:

Queries NewsAPI

Returns a list of articles

Handles errors and API failures

2. fetch_sources(param_name=None, param_value=None)

Retrieves a list of news sources filtered by category, country, or language.

def fetch_sources(param_name=None, param_value=None):
    url = f"https://newsapi.org/v2/sources?{param_name}={param_value}&apiKey={NEWSAPI_KEY}"

3. send_json(conn, data)

Sends JSON data to the client through a socket.

def send_json(conn, data):
    conn.sendall(json.dumps(data).encode())

4. handle_client(conn, address)

Core function that handles menu navigation and user requests.

def handle_client(conn, address):
    user = conn.recv(1024).decode("utf-8").strip()


Responsibilities:

Reads user commands

Calls fetch_headlines() or fetch_sources()

Sends results back to the client

Stores fetched data into local JSON files

Handles article/source detail selection

Manages user disconnection

5. Server Startup Loop (Main Server Code)

This is where the server starts listening for clients:

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST, PORT))
    soc.listen(MAX_CONNECTIONS)
    while True:
        sock, address = soc.accept()
        threading.Thread(target=handle_client, args=(sock, address)).start()


Purpose:

Creates server socket

Accepts connections

Starts new thread for each client

client.py

Main Functionalities

The client:

Connects to the server

Sends user choices and search queries

Displays results in GUI popups using Tkinter

Allows selecting items for more details

Key Functions in client.py
1. recv_json(sock)

Receives and decodes JSON data from the server.

def recv_json(sock):
    buffer = ""
    while True:
        chunk = sock.recv(4096)


Purpose:

Handles incomplete packets

Converts JSON string into a Python dictionary/list

2. gui_input(prompt)

Displays a Tkinter input dialog.

def gui_input(prompt):
    return simpledialog.askstring("A1", prompt)

3. show_headlines(soc)

Handles the entire headlines-search flow.

soc.sendall("Search headlines".encode())


Features:

Sends user choices to server

Receives headlines summary

Displays list of articles

Sends selected index to server

Displays full article details

4. show_sources(soc)

Handles source-search options.

soc.sendall("List of sources".encode())

5. main()

The main logic of the client.

def main():
    user = gui_input("Enter your name:")
    soc.connect((HOST, PORT))


Responsibilities:

Takes username

Connects to server

Displays the main menu

Redirects choices to show_headlines() or show_sources()

Sends EXIT on quit

Additional Concepts
1. Multithreading (Server-Side)

Allows multiple clients to connect at the same time.

threading.Thread(target=handle_client, args=(sock, address)).start()

2. JSON Communication

Used to send structured data safely.

json.dumps(data)
json.loads(received_string)

3. Socket Programming

TCP connection between client and server.

socket.socket(socket.AF_INET, socket.SOCK_STREAM)

4. GUI with Tkinter

Used in the client to create input dialogs and message popups.

messagebox.showinfo("A1", detail_msg)

5. External API Integration

Server uses NewsAPI to fetch current news and sources.

requests.get(url, timeout=8)


## Acknowledgments

We  thank our instructor for the support and advice throughout the development of this project.
We also appreciate NewsAPI.org for making real-time news data available, which was essential for building our system.

## Conclusion

This project successfully demonstrates a working client-server application in Python. It combines network programming, multithreading, and API integration to allow multiple users to request and receive news at the same time.
The project highlights how Python can be used to handle real-world tasks like fetching live data, managing concurrent connections, and presenting information to users in a simple and interactive way.