import socket
import threading


HOST = '127.0.0.1'
PORT = 59999        
MAX_CONNECTIONS = 3

def connection_accept(socket,address):

    client_name=socket.recv(1024).decode('ascii')
    print('\n' + 35 * '=')
    print(f"✅ CONNECTION ACCEPTED: Client Name: {client_name} | Address: {address}")
    print(35 * '=')

    while True:
     request = socket.recv(1024)
     client_request_text = request.decode('utf-8') 
     response_message = "Server received request: " + client_request_text
     response = response_message.encode('utf-8')
     socket.sendall(response)

with (socket.socket(socket.AF_INET,socket.SOCK_STREAM)) as soc:

    soc.bind((HOST, PORT))
    soc.listen(MAX_CONNECTIONS)
    print(f"\n==============================================")
    print(f"SERVER LISTENING on {HOST}:{PORT}")
    print(f"==============================================")

    while True:
        sock,address=soc.accept()
        t=threading.Thread(target=connection_accept,args=(sock,address))
        t.start()
   