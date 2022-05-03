import pymongo
import sys
from datetime import datetime
class MongoTesting:

    def __init__(self):
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

    def insertData(self,data={}):
        try:
            result = self.collection.insert_one(data)
            print("Data are inserted!!!", result.inserted_id)
        except Exception as err:
            print(err)

    def findDatawithId(self,loginId):
        try:
            query = {"_id":loginId}
            result = self.collection.find(query)
            for i in result:
               return i.get("username")
        except Exception as err:
            print(err)

    def userCount(self):
        try:
            result = self.collection.find({},{"_id":0,"username":1})
            no = []
            for i in result:
                no.append(i)
            print(no)
            count = len(no)
            print("Total Count",count)
            return count+1
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

    def register(self):
        print("********This is From Registration route*********\n")
        name = input("Enter username to register")
        password = input("Enter password to register")
        amount = input("Enter amount to register")
        id = self.userCount()
        dataform = {"_id":id,"username":name,"password":password,"amount":amount}
        self.insertData(dataform)

    def login(self):
        print("********This is From Login route*********\n")
        l_username: str = input("\nPls enter email address to Login:")
        l_password: str = input("\nPls enter password to Login:")
        loginId = self.checkingLoginInfo(l_username, l_password)
        if loginId:
            print("\n\n\n ___Login Successful___\n")
            print("~~~~~Welcome from login Page~~~~:  {0} ".format(l_username))
            self.user_menu(loginId)
        else:
            print("\n\n\n~~~Login Fail~~~\n\n\n")
            self.main_menu()

    def main_menu(self):
        print()
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Welcome to the Python Bank System")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1) login")
        print("2) Register")
        print("3) Quit Python Bank System")
        print(" ")
        option:int = int(input("Choose your option: "))
        if option == 1:
            self.login()
        elif option == 2:
            self.register()
            print("Registration successful at {}".format(self.current_time))
        else:
            print("~~~~~~BYE BYE NOW~~~~~~")
            sys.exit()

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

    def get_name(self, loginId):
        try:
            query = {"_id": loginId}
            result = self.collection.find(query)
            for i in result:
                name = i.get("username")
                print("Name: ", name)
            return name
        except Exception as err:
            print(err)

    def get_password(self, loginId):
        try:
            query = {"_id": loginId}
            result = self.collection.find(query)
            for i in result:
                passcode = i.get("password")
                print("Password: ", passcode)
            return passcode
        except Exception as err:
            print(err)

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

    def updateAmount(self,idNo,amount):
        try:
            oAmount = self.get_amount(idNo)
            query = {"_id": idNo,"amount":oAmount}
            newQuery = {"$set":{"_id": idNo,"amount":amount}}
            self.collection.update_one(query,newQuery)
            print("Updating amount successful!!!")
        except Exception as err:
            print(err)

    def transferMoney(self,loginId):
        transferFlag=None
        no=self.userCount()-1
        if(no==1):
            print(f'Transaction cannot do,we only have user 1')
            # self.run_user_options()
        else:
            senderId: int = loginId
            senderMoney: int = self.get_amount(senderId)
            sFMoney = int(senderMoney)
            senderName = self.get_name(senderId)
            receiverName = input("\n Please input receiver surname: ")
            receiverId: int = self.returnId(receiverName)
            print("\n\nWE get to Transer id:", receiverId)
            print("myId", loginId)
            amount: int = int(input(
                "\n Please input the amount to be transferred to {}: ".format(receiverName)))
            receiverMoney: int = self.get_amount(receiverId)
            rFMoney = int(receiverMoney)
            if sFMoney>500:
                sMoney = sFMoney - amount
                rMoney = rFMoney + amount
                # update query amount here
                self.updateAmount(senderId, sMoney)
                self.updateAmount(receiverId, rMoney)
                print(f'Transaction completed. Current Balance of sender: ₹{sMoney}', senderName)
                print(f'Transaction completed. Current Balance of receiver: ₹{rMoney}', receiverName)
                transferFlag = True
                return transferFlag
            else:
                print("Insufficient amount to transfer")

    def deposit(self,loginId):
        amount:int = int(input('Enter the deposit amount: '))
        fMoney:int = self.get_amount(loginId)
        loginName = self.get_name(loginId)
        iFmoney = int(fMoney)
        iFmoney+=amount
        self.updateAmount(loginId,iFmoney)
        print(f'Deposit Transaction completed. Current Balance: ₹{iFmoney}',  loginName)

    def withdraw(self,loginId):
        amount:int = int(input('Enter the withdraw amount: '))
        id:int = loginId
        fMoney:int = self.get_amount(loginId)
        loginName = self.get_name(loginId)
        iFmoney = int(fMoney)
        iFmoney -= amount
        if (iFmoney>500):
            self.updateAmount(loginId,iFmoney)
            print(f'Withdraw Transaction completed. Current Balance: ₹{iFmoney}', loginName)
        else:
            print("Insufficient amount!!!")

    def updateName(self, loginId, nName):
        try:
            oldName = self.get_name(loginId)
            query = {"_id": loginId, "username": oldName}
            newQuery = {"$set": {"_id": loginId, "username": nName}}
            self.collection.update_one(query, newQuery)
            print("Updating name: {} to {} successful!!!".format(oldName, nName))
        except Exception as err:
            print(err)

    def updatePassword(self, loginId, nPwd):
        try:
            oldPwd = self.get_password(loginId)
            query = {"_id": loginId, "password": oldPwd}
            newQuery = {"$set": {"_id": loginId, "password": nPwd}}
            self.collection.update_one(query, newQuery)
            print("Updating password: {} to {} successful!!!".format(oldPwd, nPwd))
        except Exception as err:
            print(err)

    def print_all_accounts_details(self):
        try:
            result = self.collection.find({}, {"_id": 0})
            for i in result:
                print(i)
        except Exception as err:
            print(err)

    def user_menu(self,loginId):
        # print the options you have
        name=self.findDatawithId(loginId)
        print(" ")
        print(
            "Welcome User %s : Avilable options are:" % (name))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1) Transfer money")
        print("2) Deposit")
        print("3) Withdraw")
        print("4) Update customer's Name")
        print("5) Update customer's Password")
        print("6) Print all customers detail")
        print("7) Sign out")
        print(" ")
        option = int(input("Choose your option: "))
        if option == 1:
            print("This is from Transfer route")
            self.transferMoney(loginId)
        elif option == 2:
            print("This is from Deposit route")
            self.deposit(loginId)
        elif option == 3:
            print("This is from Withdraw route")
            self.withdraw(loginId)
        elif option == 4:
            print("This is from Update customer's Name route")
            nName = input("Enter your new name to update: ")
            self.updateName(loginId,nName)
        elif option == 5:
            print("This is from Update customer's Password route")
            nPwd = input("Enter your new password to update: ")
            self.updatePassword(loginId,nPwd)
        elif option == 6:
            print("This is from customer's details route")
            self.print_all_accounts_details()
        else:
            self.main_menu()

if __name__ =="__main__":
    while True:
        test = MongoTesting()
        test.main_menu()
#Db file to connect to mongoDB
