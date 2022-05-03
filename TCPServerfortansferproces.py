from datetime import datetime
import socket
import pymongo

class TCPServerformongo():

    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9997
        self.userInfoDict = {}
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        try:
            """MongoClient() is a method,it contains ip,port"""
            self.connection = pymongo.MongoClient("localhost", 27017)
            self.database = self.connection["myAssDB"]
            self.collection = self.database["myCollection"]
            print("Connection Successful")
        except Exception as err:
            print(err)

    """Inserting Data into mongodb"""
    def insertData(self,data={}):
        try:
            result = self.collection.insert_one(data)
            print("Data are inserted!!!", result.inserted_id)
        except Exception as err:
            print(err)

    def checkingLoginInfo(self,username,password):
        try:
            query = {"username": username,"password":password}
            result = self.collection.find(query)
            for i in result:
                idNo = i.get("_id")
                print("Id No: ",idNo)
            return idNo
        except Exception as err:
            print(err)

    def login(self):
        print("********This is From Login route*********\n")
        l_username: str = input("\nPls enter email address to Login:")
        l_password: str = input("\nPls enter password to Login:")
        loginId = self.checkingLoginInfo(l_username, l_password)
        if loginId:
            print("\n\n\n ___Login Successful___\n")
            print("~~~~~Welcome from login Page~~~~:  {0} ".format(l_username))
            # self.user_menu(loginId)
        else:
            print("\n\n\n~~~Login Fail~~~\n\n\n")
            # self.main_menu()

    def returnId(self, username):
        try:
            query = {"username": username}
            result = self.collection.find(query)
            for i in result:
                idNo = i.get("_id")
                print("Return id: ", idNo)
            return idNo
        except Exception as err:
            print(err)

    def get_amount(self, loginId):
        try:
            query = {"_id": loginId}
            result = self.collection.find(query)
            for i in result:
                amount = i.get("amount")
                print("Amount: ", amount)
            return amount
        except Exception as err:
            print(err)

    def updateAmount(self,idNo,amount):
        try:
            oAmount = self.get_amount(idNo)
            query = {"_id": idNo,"amount":oAmount}
            newQuery = {"$set":{"_id": idNo,"amount":amount}}
            self.collection.update_one(query,newQuery)
            print("Updating amount successful!!!")
        except Exception as err:
            print(err)

    def runserver(self):
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((self.server_ip,self.server_port))
        server.listen(1)

        print(f'[**] Server Listening on {self.server_ip} : {self.server_port}')

        while True:
            client , address =server.accept()

            print(f'[+] Server Acceptes connection from {address[0]} : {address[1]}')
            self.handle_client(client)

    def handle_client(self,client):
        with client as sock:
            #Testing for transfer
            requestSMS =sock.recv(1024)
            # optionSMS = sock.recv(1024)
            print(f'[+] Received message from Client  : {requestSMS.decode("utf-8")}')
            data :str = requestSMS.decode('utf-8')
            name, amount = data.split(" ")
            print("You can transfer money to",name)
            receiverId: int = self.returnId(name)
            receiverMoney: int = self.get_amount(receiverId)
            rFMoney = int(receiverMoney)
            rMoney = rFMoney + int(amount)
            self.updateAmount(receiverId, rMoney)
            print(f'Transaction completed. Current Balance of receiver: ₹{rMoney}', name)

if __name__ =="__main__":
    myServer=TCPServerformongo()
    myServer.runserver()
