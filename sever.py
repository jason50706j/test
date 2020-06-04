#!/usr/bin/python
#coding=UTF-8
 
"""
TCP/IP Server sample
"""
"""
import socket
import threading
import time
 
bind_ip = "0.0.0.0"
bind_port = 9999
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
server.bind((bind_ip, bind_port))
            
server.listen(5)
 
print ("[*] Listening on %s : %d" %(bind_ip, bind_port))
 
def handle_client(client_socket):
    
    request = client_socket.recv(1024)
    print ("[*] Received: %s" % request)
    
    client_socket.send("ACK!")
    client_socket.close()
    
while True:
    client, addr = server.accept()
    print ("[*] Acepted connection from: %s:%d" % (addr[0],addr[1]))
    
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
"""
# -*- coding: utf-8 -*-
import time
import socket
HOST = '172.31.35.127'   #ipv4
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立soket物件
server.bind((HOST, PORT)) 
server.listen(10) #允許幾個人同時進入

while True:
    conn, addr = server.accept()
    print ("[*] Acepted connection from: %s:%d" % (addr[0],addr[1]))
    clientMessage = str(conn.recv(1024), encoding='utf-8')

    print('Client message is:', clientMessage)

    serverMessage = 'I\'m here!'
    conn.sendall(serverMessage.encode())
    conn.close()
    
    time.sleep(1)
    break