import socket

class TCPserver():

    def __init__(self):
        self.server_ip='localhost'
        self.server_port=9998

    def runserver(self):
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((self.server_ip,self.server_port))
        server.listen(1)

        print(f'[**] Server Lisening on {self.server_ip} : {self.server_port}')

        while True:
            client , address =server.accept()

            print(f'[+] Server Acceptes connection from {address[0]} : {address[1]}')
            self.handle_client(client)

    def handle_client(self,client):
        with client as sock:
            requestSMS =sock.recv(1024)
            print(f'[+] Received message from Client  : {requestSMS.decode("utf-8")}')
            data: str = requestSMS.decode("utf-8")
            if data == "khine":
                 sock.send(b'Hello Admin')
            else:
                sock.send(requestSMS)


if __name__ =="__main__":
    myServer=TCPserver()
    myServer.runserver()
