import socket
import time
import re
import requests
import bs4 as bs
import os
import threading
import ssl
import urllib.request
import urllib3

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
    mysocket.connect(("unite.md", 80))
    mysocket.sendall(b"GET / HTTP/1.1\r\nHost: unite.md\r\n\r\n")
    # mysocket.connect(("utm.md", 443))
    # mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    # mysocket.sendall(b"GET / HTTP/1.1\r\nHost: utm.md\r\n\r\n")

    print(str(mysocket.recv(52), 'utf-8'))

def get_url_images_in_text(source):
# Finds image's urls
    urls = []
    results = re.findall(r'\/images\/[^\"]*(?:png|jpg|gif)', source)
    # results = re.findall(r'\/wp-content\/[^\"]*(?:png|jpg)', source)
   
    for x in results:
        if 'http://' not in x:
        # if 'https://' not in x:
            x = 'http://unite.md' + x 
            # x = 'https://utm.md' + x 
        urls.append(x)
    urls = list(set(urls)) 
    print('Links of images detected: ' + str(len(urls)))
    return urls

def get_images_from_url(url):
    
    resp = requests.get(url)
    urls = get_url_images_in_text(resp.text)
    print('\nUrls of images:\n', urls)
    return urls

links = get_images_from_url('http://unite.md/')

http = urllib3.PoolManager()

N = 0; 
#  Counter that helps to rename the downloaded files
print ("Downloading images...")
for link in links:
    r = http.request('GET',link)
    Name =str(N+1) 
    N += 1
    with open("file" + Name + ".png", "wb") as fcont:
        fcont.write(r.data)
print ("Download Done!")

# def get_images_from_url(url):
#   domain = url.split("//")[-1].replace("/","")
#   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
#     mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
#     mysocket.connect ( (socket.gethostbyname(domain), 443 ) )
#     mysocket.sendall(b"GET / HTTP/1.1\r\nHost: utm.md\r\n\r\n")
#     mysocket.sendall ("GET / HTTP/1.1\r\nHost: {0}\r\nConnection: close\r\n\r\n".format(domain).encode("latin1"))
#     list_links = ""

#     while True: 
#       data = mysocket.recv(1024)
#       if len(data) == 0:
#         break
#       list_links += data.decode("latin1")

#     return get_url_images_in_text(list_links)

# def download_images(path):
#   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
#     mysocket.connect(("utm.md" , 443))
#     mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
#     mysocket.sendall("GET {0} HTTP/1.1\r\nHost: utm.md\r\nConnection: close\r\n\r\n".format(path).encode("latin1"))

#     images = b''

#     while True:
#       data = mysocket.recv(1024)
#       if not data:
#         images = images.split(b"\r\n\r\n")
#         if "200" not in images[0].decode("latin1"):
#           print(path)
#         image_path = os.path.join(os.getcwd(), "Utm_Images", path.rpartition("/")[-1])
#         with open(image_path, "wb") as fcont:
#           fcont.write(images[-1])
#         break

#       images+=data
# img_list = get_images_from_url("utm.md")

# thread_list_of_images = [ ]

# for img in img_list:
#   t = threading.Thread(target=download_images, args=(img,))
#   thread_list_of_images.append(t)
#   t.start()

# for img in thread_list_of_images:
#   img.join()
# print ("Download Done!")
