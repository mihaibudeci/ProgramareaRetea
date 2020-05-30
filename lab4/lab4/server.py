#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Verificarea parolei
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("hello", "utf8"))
        while True:
            connection = client.recv(24).decode("utf8")
            if connection == "1234":
                print(connection)
                client.send(bytes("Greetings from the cave!! Now type your name and press enter!", "utf8"))
                addresses[client] = client_address # se adauga clientul
                Thread(target=handle_client, args=(client,)).start() # se porneste firul
                break
                break
            elif connection == "hello":
                print(connection)
                client.send(bytes("password", "utf8"))
            else:
                print("{authentiffication Error}")
                client.send(bytes("{authentiffication Error}", "utf8"))
                break

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name # transmite un mesaj clientului
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name # mesaj catre toti participantii
    broadcast(bytes(msg, "utf8")) # datorita acestei functii se trimite mesajul
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg) # trimite pentru fiecare client mesajul

# variabilele initiale
clients = {} #clients list
addresses = {} #adressess list

HOST = '127.0.0.1'
PORT = 10000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM) #pornirea serverului
SERVER.bind(ADDR)

# are loc conexiunea
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections) # crearea unui fir de executie
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()