# CSCI-5673-Distributed-Systems

## Technology stack
- python: libraries socket, threading, time
- DB : PostgreSQL

## System Design

1. ### 6 components

1 server and 1 client for role 'Seller', 1 server and client for role 'Buyer'. 1 Products DB and 1 Customers DB. They are running on same machine, however, the clients and servers can easily shift to remote systems by giving different IP addresses and port numbers.

2. ### Database description

Customers DB has 4 tables. 'buyer','seller', 'cart' and 'cart_items'. The buyer and seller tables are used to store login credentials and also the associated characteristics described in the assignment. The cart and cart_items table store the cart details for all the buyers.

Products DB has a 'product' table, storing all the details ascribed to an 'item for sale' as well as seller id (as a foreign ID ) and feedback columns.

3. ### Buyer class
The server handles all the necessory functions. The client send the request to the server and the server performs operations based on the requests made by the client. The server interacts with db classes to fetch neccesary details from the databases. The server also validates all the requests. The db interface classes 'CustomersDatabase' and 'ProductsDatabase' handles all the incoming db requests and performs required operations in the databases. 

4. ### Seller side interface

The server is responsible for 'serving' the available options, taking input and invoking functions at the backend. The entry point to functionalities is through the SellerPortal object. This object uses two more objects ('Seller' and 'Products') to register and validate inputs, while also communicating with the DB Interface classes.

Two DB interface classes (customerInterface and productInterface) are responsible for handling DB connection, creating queries and returning the responses.

5. ### Evaluation

The times for calculating Average Server throughput and Average Response Times are only measured for API function calls, (and not when gathering input). To calculate for multiple clients, averages of all values over different clients has been reported. ( Detailed logs available in the evaluation_logs folder)

## Assumptions

Seller - Login is done assuming unique usernames. The feedback is actually updated in DB only when the user wants to see their rating and not in real time. Bad and empty client inputs are handled, or otherwise validated. In one session, some information is persisted in server (seller id, logged in status). It is assumed the client does not have any idea about the server functionalities when it connects.

Buyer -Same as seller login is doneassuming unique usernames. And in a session, some information is persisted in the server. 

DB - For connecting to PostgreSQL, it is assumed it uses sockets and TCP/IP underneath the library API (based on the documentaion)

Evaluation - The evaluation is carried out only using read functions (fetching products or cart items).


# What doesn't work
There are a few edge cases that are not handled. The seller can upload same product multiple times with all details same as long as ID is autoincremented. Ideally, the quantity should be increased. But similar edge case for adding an item to the cart is handled. In Buyer, one edge case where the number of specific products should be less than or equal to the quantiy of the product is not handled. 
