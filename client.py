
import socket

#HOST = '3.22.229.250'
"""
HOST = "ec2-3-22-229-250.us-east-2.compute.amazonaws.com"
PORT = 80
"""
HOST = "127.0.0.1"
PORT =8001
clientMessage = 'Arts'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("連線中")
client.connect_ex((HOST, PORT))
print("成功")
client.sendall(clientMessage.encode())
print("以傳送")
column=[]
result_data=[]
number_data = str(client.recv(1024), encoding='utf-8')
print(number_data)
for i in range(0,19):
    column.append(str(client.recv(1024), encoding='utf-8'))
print(column)
for i in range(0, int(number_data)):
    tmp=[]
    for j in range(0, 19):
        tmp.append(str(client.recv(1024), encoding='utf-8'))
    result_data.append(tmp)
print(result_data)

client.close()
