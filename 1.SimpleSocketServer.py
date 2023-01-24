import socket

#host = socket.gethostbyname(socket.gethostname())#can get ip address automatically

HOST = '192.168.100.63'#localhost
PORT = 9090

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(5)#how many unacceptable connection do we allow before we reject new ones

while True:
    communication_socket , address = server.accept()#communication socket ---> addr of the client,socket that we can
    #use to talk to that client
    print(f"Connected to {address}")
    message = communication_socket.recv(1024).decode("utf-8")#in bytes
    print(f"Message from client is {message}")
    communication_socket.send(f"Got your message.Thank you".encode("utf-8"))
    communication_socket.close()
    print(f"Connection with {address} ended!")
