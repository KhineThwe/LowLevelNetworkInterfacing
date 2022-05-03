from datetime import datetime
import socket

import pymongo

class TCPserver():
    def __init__(self):
        self.server_ip='localhost'
        self.server_port = 9997
        self.userInfoDict = {}
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        try:
            """MongoClient() is a method,it contains ip,port"""
            self.connection = pymongo.MongoClient("localhost", 27017)
            self.database = self.connection["myTestDB"]
            self.collection = self.database["myCollection"]
            print("Connection Successful")
        except Exception as err:
            print(err)
	    
    def main(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen(1)
        print(f'[*] Listening on {self.server_ip}:{self.server_port} >:')
        while True:
            client, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            self.handle_client(client)

    def insertData(self,data={}):
        try:
            result = self.collection.insert_one(data)
            print("Data are inserted!!!", result.inserted_id)
        except Exception as err:
            print(err)

    def userDuplicateChecking(self,c_username):
        try:
            query = {"username":c_username}
            result = self.collection.find_one(query)
            if result:
                return True
            else:
                return False
        except Exception as err:
            print(err)
            
    def handle_client(self,client_socket):
        with client_socket as sock:
            request = sock.recv(4096)
            print(f'[*] Received: {request.decode("utf-8")}')
            #need to decode clientinfo data
            clientInfo =request.decode("utf-8")
            c_username , c_password ,c_amount =clientInfo.split(" ")
            flag = self.userDuplicateChecking(c_username)
            print("Checking flag",flag,type(flag))
            if flag:
                sock.send(b'Username duplicate!!Please enter name again!!!')
            else:
                dataForm = {"username": c_username, "password": c_password, "amount": c_amount}
                self.userInfoDict.update(dataForm)
                print(self.userInfoDict)
                name = bytes(self.userInfoDict["username"], 'utf-8')
                sock.send(name+b'Data inserted into mongoDB')
                self.insertData(self.userInfoDict)
            
if __name__ == '__main__':
    Myserver = TCPserver()
    Myserver.main()
