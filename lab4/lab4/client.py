#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8") # primirea mesajelor de pe server
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break # la eroare sa opreste


def send(event=None):  # event is passed by binders. Transmiterea mesajelor la server
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk() # implementare interfata grafica
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
# conexiune cu serverul
HOST = ("127.0.0.1")
PORT = 10000

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
# logarea la server
while True:
    connection = client_socket.recv(25).decode("utf8")
    if connection != "hello" and connection != "password" and connection != "" and \
            connection != "{authentiffication Error}":
        receive_thread = Thread(target=receive)
        print(connection)
        receive_thread.start()
        tkinter.mainloop()  # Starts GUI execution.
        break
    elif connection == "hello":
        client_socket.send(bytes("hello", "utf8"))
        print(connection)
    elif connection == "password":
        client_socket.send(bytes("1234", "utf8"))
        print(connection)
    elif connection == "{authentiffication Error}":
        print("connection not established!!, wrong password")
        break

