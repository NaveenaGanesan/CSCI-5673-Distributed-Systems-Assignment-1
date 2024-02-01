import socket
import threading
import pickle

'''
File to run server for seller in the E-Market application
Server
- uses multi-threading to accept multiple clients
- connects clients with the server interface of the application which connects to the DB
- also calculates statistics and logs them:
    - Average response time for 10 function calls
    - Average throughput for a 1000 function calls
'''

class CustomerDB:
    def __init__(self):
        '''
        Initializes for binding server to port and keeps track of active connections over all clients 
        '''
        self.HEADER = 64
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 6080
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!DISCONNECT"
        self.active_connections = 0
        self.loadDB()
        self.initialize_server()
        self.start_server()

    def loadDB(self):
        with open ("customers_db.pkl", "rb") as f:
            self.db = pickle.load(f)

        # self.sellerTable = [{'id':1, 'username':"user1", 'password':'userone','thumbs_up_count':0,'thumbs_down_count':0,'items_sold':0 },\
        #                     {'id':2, 'username':"user2", 'password':'usertwo','thumbs_up_count':0,'thumbs_down_count':0,'items_sold':0 },
        #                     {'id':4, 'username':"user4", 'password':'userfour','thumbs_up_count':0,'thumbs_down_count':0,'items_sold':0 },
        #                     {'id':3, 'username':"user3", 'password':'userthree','thumbs_up_count':1,'thumbs_down_count':1,'items_sold':0 }]
        # self.db = {"seller":(self.sellerTable, {"lastrowid":4})}
        # with open ("customers_db.pkl", "wb") as f:
        #     pickle.dump(self.db,f)

        # print(self.db)
        # self.db["buyer"] = (,{lastrow})

    def initialize_server(self):
        '''
        Binds the server to the port
        '''
        self.server = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)
        print(f"Starting DB server at {self.PORT}...")

    
    def start_server(self):
        '''
        Listens to port and creates threads for incoming clients. Also updates the active threads.
        '''
        self.server.listen()
        while True:
            connection, address = self.server.accept()
            thread = threading.Thread(target = self.handleConnection, args=(connection, address))
            thread.start()
            self.active_connections = threading.active_count()-1
            print("Active DB connections ", self.active_connections)
    
    def insert_autoid(self,table_name, column_names , values):
        new_row = {}
        newid = self.db[table_name][1]['lastrowid'] + 1
        self.db[table_name][1]['lastrowid']+=1
        for col, val in enumerate(column_names,values):
            new_row[col]=val
        new_row['id'] = newid
        self.db[table_name][0].append(new_row)
        print(self.db)
        return newid
    
    def updateRowByColumn(self,table_name, column_names , values, condition_col, condition_val):
        table = self.db[table_name][0]
        for row in table:
            if row[condition_col] == condition_val:
                for col, val in zip(column_names,values):
                    row[col]=val
        print(self.db)
        return 1
    
    def getRowByColumn(self,table_name, column , search_value):
        table = self.db[table_name][0]
        response = tuple()
        for row in table:
            if row[column] == search_value:
                response = tuple(row.values())
        return response
    def getRowByColumns(self,table_name, columns , search_values):
        print(" parameters : ",columns,search_values)
        table = self.db[table_name][0]
        response = tuple()
        for row in table:
            satisfiesSearch = True
            for col,val in zip(columns,search_values):
                if row[col] != val:
                    satisfiesSearch=False
            if satisfiesSearch:
                return tuple(row.values())  
        return response

    def handleConnection(self,client, address):
        '''
        The entry point for each client.
        - receive messages from the client
        - send appropriate response
        '''

        print("New Connection: ", address)
        # keep track of connection to stop threa
        connected = True 
        # run loop until client indicates exit
        while connected:

            # Get string from bytes received by client 
            # first part of message - length of the actual message

            msg_len = client.recv(self.HEADER).decode(self.FORMAT) # blocking

            # if message is empty, ignore
            if msg_len:
                msg_len = int(msg_len)

                # second part of message - the content of client input
                msg = client.recv(msg_len).decode(self.FORMAT) 

                # pass the message directly to the interface, get response
                # response has 2 parts - msg and invokeTime (stats)
                

                # if client exits, detect via disconnect messaget
                msg = msg.split(";")
                command = msg[0]
                if(command == "INSERTAUTOID"):
                    table_name = msg[1]
                    columns = msg[2].split(",")
                    values = msg[3].split(",")
                    response = self.insert_autoid(table_name,columns,values)
                elif(command == "GETROWBYCOL"):
                    table_name = msg[1]
                    column = msg[2]
                    value = msg[3]
                    response = self.getRowByColumn(table_name,column,value)
                elif(command == "GETROWBYMULTICOL"):
                    table_name = msg[1]
                    columns = msg[2].split(",")
                    values = msg[3].split(",")
                    response = self.getRowByColumns(table_name,columns,values)
                elif(command == "UPDATEONE"):
                    table_name = msg[1]
                    columns = msg[2].split(",")
                    values = msg[3].split(",")
                    condition_col = msg[4]
                    condition_val = msg[5]
                    response = self.updateRowByColumn(table_name,columns,values, condition_col, condition_val)
                else:
                    # Continue to send the response message to client
                    connected = False
                
                self.send(client,response)
        client.close()

    # in this case did not send message length and just gave a big enough number for server response
    def send(self,client, msg):
        # print(msg, type(msg))
        message = str(msg).encode(self.FORMAT)
        msg_length = len(message)
        # send_length = str(msg_length).encode(self.FORMAT)
        padded_message = message + b" " * (self.HEADER-msg_length)
        # Header plus message
        # client.send(padded_send)
        client.send(padded_message)
        

customerDB = CustomerDB()
# customerDB.initialize_server()
# customerDB.start_server()

# customerDB.loadDB()