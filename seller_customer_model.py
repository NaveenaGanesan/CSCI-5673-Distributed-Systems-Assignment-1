import socket 
import os
from ast import literal_eval
# '''INSERT INTO TABLE customers ({ newid }
# )'''


class CustomerInterface:
    def __init__(self):
        '''
        Initializes required parameters for socket connection and also begins communication. 
        '''
        self._HEADER = 64
        self._SERVER = socket.gethostbyname(socket.gethostname())
        self._PORT = 6080
        self._ADDRESS = (self._SERVER, self._PORT)
        self._FORMAT = "utf-8"
        self.DISCONNECT_MSG = "bye"
        self._RECEIVE = 1024
        self.inititate_connection()

    def inititate_connection(self):
        self.db = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
        self.db.connect(self._ADDRESS)

    def insertCustomer(self, un, pw):
        try:
            msg = f"INSERTAUTOID;seller;username,password;{un},{pw}"
            self.send(msg)
            response = self.db.recv(self._RECEIVE).decode(self._FORMAT)
        except Exception as e:
            print(e)
            return -1

        print("last row id",response)
        return response
    
        
    def getUser(self, un, pw=None):
        user = None
        try:
            # self.cursor.execute("INSERT INTO ")
            # self.table.append({"id": newid, "username": un,"password":pw})
            if pw:
                msg = f"GETROWBYMULTICOL;seller;username,password;{un},{pw}"
                self.send(msg)
                user = self.db.recv(self._RECEIVE).decode(self._FORMAT)
            else:
                msg = f"GETROWBYCOL;seller;username;{un}"
                self.send(msg)
                user = self.db.recv(self._RECEIVE).decode(self._FORMAT)
            print("user: ", user)
        except Exception as e:
            print(e)
            return -1
        user = literal_eval(user)
        return user
        

        # for row in self.table:
        #     # print("Current row ==>", row, row["username"], row["password"])
        #     if row["username"]== un and  row["password"] == pw:
        #         return row
        # return None
    
    def updateFeedback(self, seller_id,tu,td):
        msg = f"UPDATEONE;seller;thumbs_up_count,thumbs_down_count;{tu},{td};id;{seller_id}"
        self.send(msg)
        didUpdate = self.db.recv(self._RECEIVE).decode(self._FORMAT)
        return didUpdate
    
    def send(self, msg):
        '''
        Conducts one send cycle - requires two messages to be sent
        '''
        # As number of bytes have to be known to receive message in python, db 
        # first sends the length of the message in bytes and then the actual message   
        message = msg.encode(self._FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._FORMAT)
        padded_send = send_length+ b" "*(self._HEADER-len(send_length))
        self.db.send(padded_send)
        self.db.send(message)