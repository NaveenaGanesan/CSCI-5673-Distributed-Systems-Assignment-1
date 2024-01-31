import socket
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

is_logged_in = False
buyer_id = None

def get_local_ip():
    try:
        # Attempt to connect to an arbitrary public IP address.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error: {e}")
        return None

def initialize_connection():
    SERVER = get_local_ip()
    ADDR  = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Client connected to : ", ADDR)
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # send_length = send_length.strip() 
    send_length += b' ' * (HEADER - len(send_length))
    # print(f"[Message length in client...] {send_length}")
    client.send(send_length)
    # time.sleep(0.1)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))
    server_response = client.recv(2048).decode(FORMAT)
    # print(server_response)
    return server_response

def create_account(username, password, name):
    create_account_response = send(f"CREATE_ACCOUNT {username} {password} {name}")
    print(create_account_response)

def login(client, username, password):
    global is_logged_in
    global buyer_id

    login_response = send(client, f"LOGIN {username} {password}")
    print(f"Login Response: {login_response}, Username: {username}, Password: {password}")
    if "Login successful" in login_response:
        is_logged_in = True
        buyer_id_response = client.recv(2048).decode(FORMAT)  
        buyer_id = buyer_id_response.split()[-1]
        print(f"Buyer Id: {buyer_id}")

def search_item(query):
    search_results = send(f"SEARCH {query}")
    # search_results = client.recv(2048).decode(FORMAT)
    print(f"Search Results:\n{search_results}")

def add_to_cart(product_id, quantity):
    global buyer_id
    server_response = send(f"ADD_TO_CART {buyer_id} {product_id} {quantity}")
    print(server_response)

def remove_item_from_cart(product_id, quantity):
    global buyer_id
    server_response = send(f"REMOVE_ITEM_FROM_CART {buyer_id} {product_id} {quantity}")
    print(server_response)

def clear_cart():
    global buyer_id
    server_response = send(f"CLEAR_CART {buyer_id}")
    print(server_response)

def display_cart(client):
    global buyer_id
    cart_items = send(client, f"DISPLAY_CART {buyer_id}")
    # print(cart_items)

def get_seller_rating(seller_id): #this yet to be tested
    seller_rating = send(f"GET_SELLER_RATING {seller_id}")
    print(f"Seller Rating: {seller_rating}")

def provide_feedback(): #feedback for the latest order
    global buyer_id
    purchased_items = send(f"PROVIDE_FEEDBACK {buyer_id}")

    if "No purchase was made" in purchased_items or "Failed to retrieve product details" in purchased_items:
        return
    
    product_id = input("Please enter the product ID for which you want to provide feedback: ")
    feedback_response = send(product_id)

    if "Feedback already provided" in feedback_response:
        return
    
    feedback_type = input("Enter your feedback (Thumbs Up or Thumbs Down): ")
    send(feedback_type)

def buyer_purchase_history():
    global buyer_id
    purchase_history = send(f"PURCHASE_HISTORY {buyer_id}")
    print(f"Buyer Purchase History: {purchase_history}")

def logout(client):
    global is_logged_in
    global buyer_id

    response = send(client, f"LOGOUT {buyer_id}")
    if "Logout successful" in response:
        is_logged_in = False
    print(response)

def measure_responsetime():
    print("Measuring response time...")
    responsetimes = []
    for _ in range(10):
        start = time.time()
        display_cart()
        end = time.time()
        responsetimes.append(end-start)
    print("Response time: ",sum(responsetimes)/10)

def measure_throughput(client):
    print("Measuring throughput...")
    client_operations = 1
    total_time = 0

    for _ in range(client_operations):
        start = time.time()
        display_cart(client)
        end = time.time()
        total_time += (end - start)

    throughput = client_operations / total_time
    print(f"Throughput: {throughput} operations/second")

def show_initial_options():
    print("Welcome to the Online Marketplace!")
    print("Please select an option:")
    print("1. Create an account")
    print("2. Login")
    print("3. Exit")

def show_logged_in_options():
    print("\n")
    print("4. Search for Items")
    print("5. Add an item to cart")
    print("6. Remove an item in cart")
    print("7. Clear Cart")
    print("8. Display Cart")
    print("9. Purchase History")
    print("10. Provide Feedback")
    print("11. Get Seller Rating")
    print("12. Logout")
    print("13. Measure Server Throughput")
    print("14. Measure Response Time")

def init():   
    global is_logged_in

    while True:
        if not is_logged_in:
            show_initial_options()
        else:
            show_logged_in_options()

        option = input("\nEnter your choice: ")
        handle_option(option)

        if option == '3' and not is_logged_in: 
            break
        elif option == '12':
            break

def handle_option(option):
    if option == '1':
        username = input("Choose your username: ")
        password = input("Choose your password: ")
        name = input("Enter your name: ")
        create_account(username, password, name)
    elif option == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        login(username, password)
    elif option == '3':
        client.close()
    elif option == '4':
        query = input("Enter search query: ")
        search_item(query)
    elif option == '5':
        product_id = input("Enter product id: ")
        quantity = input("Enter quantity: ")
        add_to_cart(product_id, quantity)
    elif option == '6':
        product_id = input("Enter product id: ")
        quantity = input("Enter quantity: ")
        remove_item_from_cart(product_id, quantity)
    elif option == '7':
        clear_cart()
    elif option == '8':
        display_cart()
    elif option == '9':
        buyer_purchase_history()
    elif option == '10':
        provide_feedback()
    elif option == '11':
        seller_id = input("Enter seller ID to get rating: ")
        get_seller_rating(seller_id)
    elif option == '12':
        logout()
    elif option == '13':
        measure_throughput()
    elif option == '14':
        measure_responsetime()
    else:
        print("Invalid option, please try again.")
        init()

def main():
    client = initialize_connection()
     # init()
    login(client, "katie","testkatie")
    measure_throughput(client)
    logout(client)
    send(client, DISCONNECT_MSG)
    client.close()

if __name__ == "__main__":
    main()
