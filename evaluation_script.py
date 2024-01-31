import threading
from buyer_client import main as buyer_client_main

def run_buyer_instance():
    buyer_client_main()

def main():
    number_of_buyer_instances = 2
    threads = []
    print(f"Number of buyer instances: {number_of_buyer_instances}")
    for _ in range(number_of_buyer_instances):
        thread = threading.Thread(target=run_buyer_instance)
        thread.start()
        print("Active connections: ", threading.active_count()-1)
        threads.append(thread)

    # for thread in threads:
    #     thread.join()

if __name__ == "__main__":
    main()
