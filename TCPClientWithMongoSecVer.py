#client
import socket
import sys

class Client:
    def __init__(self,loginInfo) -> None:
        self.target_server = 'localhost'
        self.target_port=9997
        self.client_info = loginInfo
        
        self.clientMessage = bytes(self.client_info,'utf-8')
    
    def runClient(self):
        client =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((self.target_server,self.target_port))
        
        client.send(self.clientMessage)
        recvSMSMfromServer =client.recv(4096)
        print(f'[+] Received message from server :{recvSMSMfromServer.decode("utf-8")}')
        
        client.close()

def option():
    try:
        option = int(input("1:For Register:\n2: For Login:"))
        if option==1:
            c_username = input("Enter username:")
            c_password = input("Enter password")
            c_amount   = int(input("Enter amount"))
            client_info= c_username+" "+c_password+" "+str(c_amount)
            clineObj=Client(client_info)
            clineObj.runClient()
        else:
            pass
                # ယခု နေရာတွင် Registration ကို စစ်ဆေးရန် ရေးရမည်
    except Exception as err:
        print(err)
        print("Try Again ! Invalid Option ")

if __name__ =="__main__":
    while True:
        option()
        
        
