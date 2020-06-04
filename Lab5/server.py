import socket, time 

host = socket.gethostbyname(socket.gethostname()) 
port = 9090

clients = []

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # se creaza un socket object
s.bind((host,port)) # facem bind host si port la socket

quit = False
print("[ Server Started ]")

while not quit:
	try:
		data, addr = s.recvfrom(1024) # primim raspuns de la client

		if addr not in clients: # daca adresa nu este in lista de clienti
			clients.append(addr) # atunci se anexeaza la lista

		thistime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

		print("["+addr[0]+"]=["+str(addr[1])+"]=["+thistime+"]/",end="")
		print(data.decode("utf-8"))

		for client in clients: #pentru fiecare client din lista de clienti
			if addr != client: # daca adresa nu corespunde clientului
				s.sendto(data,client) # se transmite data la client
	except:	
		print("\n[ Server Stopped ]")
		quit = True
		
s.close()
