import threading
import socket

host="127.0.0.1"
port=5555

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Internet socket, protocol:TCP
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
        break

def receive():
    while True:
        client, address=server.accept()
        print(f'connected with {str(address)}')


        client.send("Nickname ?".encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        nicknames.append(nickname)

        print(f'{nickname} joined the server')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('connected to server'.encode('ascii'))


        thread=threading.Thread(target=handle, args=(clients,))
        thread.start()

        
print("Server is listening")
receive()