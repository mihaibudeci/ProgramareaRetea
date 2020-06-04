import socket, threading, time

key = 8194

shutdown = False
join = False

def receving (name, sock):
	while not shutdown: # atat timp cat programul ruleaza
		try:
			while True:
				data, addr = sock.recvfrom(1024) # primește datele și adresa din datele primite

				decrypt = ""; k = False
				for i in data.decode("utf-8"):
					if i == ":":
						k = True
						decrypt += i
					elif k == False or i == " ":
						decrypt += i
					else:
						decrypt += chr(ord(i)^key)
				print(decrypt)
				# End

				time.sleep(0.2)
		except:
			pass
host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.0.104",9090)

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0) #setează blocarea la 0 (în esență, nu este blocată)

user = input("Name: ")

rT = threading.Thread(target = receving, args = ("RecvThread",s))
rT.start() # initializarea firului de executie

while shutdown == False:
	if join == False:
		s.sendto(("["+user + "] => join chat ").encode("utf-8"),server)
		join = True
	else:
		try:
			message = input()

			crypt = ""
			for i in message:
				crypt += chr(ord(i)^key)
			message = crypt

			if message != "":
				s.sendto(("["+user + "] :: "+message).encode("utf-8"),server)
			
			time.sleep(0.2)
		except:
			s.sendto(("["+user + "] <= left chat ").encode("utf-8"),server)
			shutdown = True

class Client_inteface:
    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.initialize_socket()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        host = '192.168.0.104'
        port = 9090
        self.client_socket.connect((host, port))

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start() # primirea mesajelor cu ajutorul firului de executie


    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')


rT.join()
s.close()
