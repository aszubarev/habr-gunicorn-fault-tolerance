import threading
from datetime import datetime
from time import sleep

from http_client import HTTP11Client



def scenario_1():
    client_1 = HTTP11Client('127.0.0.1', 80, client_name='client 1')
    client_2 = HTTP11Client('127.0.0.1', 80, client_name='client 2')

    try:
        client_1.connect()
        client_2.connect()

        client_1.do_request('GET', '/')

        timeout = 5
        print(f'[{datetime.now()}] sleep {timeout} sec')
        sleep(timeout)
        
        client_2.do_request('GET', '/')

    except Exception as e:
        print(f"[{datetime.now()}] Ошибка: {e}")
    finally:
        client_1.close()
        client_2.close()


def scenario_2():
    client_1 = HTTP11Client('127.0.0.1', 80)

    try:
        client_1.connect()

        client_1.do_request('GET', '/')

        timeout = 5
        print(f'[{datetime.now()}] sleep {timeout} sec')
        sleep(timeout)

        client_1.do_request('GET', '/')

    except Exception as e:
        print(f"[{datetime.now()}] Ошибка: {e}")
    finally:
        client_1.close()


def scenario_3():
    client_1 = HTTP11Client('127.0.0.1', 80, client_name='client 1')
    client_2 = HTTP11Client('127.0.0.1', 80, client_name='client 2')

    try:
        client_1.connect()
        client_2.connect()

        client_1.do_request('GET', '/')
        client_2.do_request('GET', '/')

        timeout = 5
        print(f'[{datetime.now()}] sleep {timeout} sec')
        sleep(timeout)

        client_1.do_request('GET', '/')

    except Exception as e:
        print(f"[{datetime.now()}] Ошибка: {e}")
    finally:
        client_1.close()
        client_2.close()


def scenario_4():
    client_1 = HTTP11Client('127.0.0.1', 80, client_name='client 1')
    client_2 = HTTP11Client('127.0.0.1', 80, client_name='client 2')

    try:
        client_1.connect()
        client_2.connect()

        client_1_thread = threading.Thread(target=client_1.do_request, args=('GET', '/'))
        client_2_thread = threading.Thread(target=client_2.do_request, args=('GET', '/'))

        client_1_thread.start()
        client_2_thread.start()

        client_1_thread.join()
        client_2_thread.join()

        timeout = 1
        print(f'[{datetime.now()}] sleep {timeout} sec')
        sleep(timeout)

        client_1.do_request('GET', '/')

    except Exception as e:
        print(f"[{datetime.now()}] Ошибка: {e}")
    finally:
        client_1.close()
        client_2.close()


def scenario_5():
    client_1 = HTTP11Client('127.0.0.1', 80, client_name='client 1')
    client_2 = HTTP11Client('127.0.0.1', 80, client_name='client 2')

    try:
        client_1.connect()
        client_2.connect()

        client_1_thread = threading.Thread(target=client_1.do_request, args=('GET', '/'))
        client_2_thread = threading.Thread(target=client_2.do_request, args=('GET', '/'))

        client_1_thread.start()
        client_2_thread.start()

        client_1_thread.join()
        client_2_thread.join()

        timeout = 10
        print(f'[{datetime.now()}] sleep {timeout} sec')
        sleep(timeout)

        client_1.do_request('GET', '/')

        timeout = 10
        print(f'[{datetime.now()}] sleep {timeout} sec')
        sleep(timeout)

        client_2.do_request('GET', '/')

    except Exception as e:
        print(f"[{datetime.now()}] Ошибка: {e}")
    finally:
        client_1.close()
        client_2.close()


def scenario_6():
    clients_total = 100
    clients = []
    clients_threads = []

    for i in range(clients_total):
        client = HTTP11Client('127.0.0.1', 80, client_name=f'client {i:02d}')
        clients.append(client)

    for client in clients:
        client.connect()

    for client in clients:
        client_thread = threading.Thread(target=client.do_request, args=('GET', '/'))
        clients_threads.append(client_thread)

    for client_thread in clients_threads:
        client_thread.start()

    for client_thread in clients_threads:
        client_thread.join()


def scenario_7():
    client_1 = HTTP11Client('127.0.0.1', 80, client_name='client 1')
    client_2 = HTTP11Client('127.0.0.1', 80, client_name='client 2')

    try:
        client_1.connect()
        client_2.connect()

        client_1_thread = threading.Thread(target=client_1.do_request, args=('GET', '/'))
        client_2_thread = threading.Thread(target=client_2.do_request, args=('GET', '/'))

        client_1_thread.start()
        client_2_thread.start()

        client_1_thread.join()
        client_2_thread.join()

        client_1.do_request('GET', '/')

        timeout = 1
        print(f'[{datetime.now()}] sleep {timeout} sec')
        sleep(timeout)

        # client_2.do_request('GET', '/')
        client_2.do_request('POST', '/', body='123')

    except Exception as e:
        print(f"[{datetime.now()}] Ошибка: {e}")
    finally:
        client_1.close()
        client_2.close()


if __name__ == "__main__":
    scenario_6()