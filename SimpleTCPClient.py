#client
from pydoc import cli
import socket

class Client:
    def __init__(self,client_sms) -> None:
        self.target_server = 'localhost'
        self.target_port=9997
        
        self.clientMessage = bytes(client_sms,'utf-8')
    
    def runClient(self):
        client =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((self.target_server,self.target_port))
        
        client.send(self.clientMessage)
        recvSMSMfromServer =client.recv(4096)
        print(f'[+] Received message from server :{recvSMSMfromServer.decode("utf-8")}')
        
        client.close()

if __name__ =="__main__":
    while True:
        clientSMS = input("Enter data to send server>:")
        tcp_client = Client(clientSMS)
        tcp_client.runClient()
