#client
import socket
import sys

class Client:
    def __init__(self,client_sms) -> None:
        self.target_server = 'localhost'
        self.target_port=9997
        
        self.clientMessage = bytes(client_sms,'utf-8')
        # self.optionMessage = bytes(option,'utf-8')
    
    def runClient(self):
        client =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((self.target_server,self.target_port))
        
        client.send(self.clientMessage)
        recvSMSMfromServer =client.recv(4096)
        print(f'[+] Received message from server :{recvSMSMfromServer.decode("utf-8")}')
        
        client.close()

if __name__ =="__main__":
    while True:
        # Testing for transfer method
        username = input("Enter username to transfer: ")
        amount = input("Enter amount to transfer: ")
        clientSMS = username+" "+amount
        tcp_client = Client(clientSMS)
        tcp_client.runClient()
        # if tcp_client.runClient:
        #     option = input("Welcome,available options are: 1)Transfer money 2)Deposit 3)Withdraw")
        #     if option == "1":
        #         clientSMS = "transfer"
        #         tcp_client = Client(clientSMS)
        #         tcp_client.runClient()
        
        
