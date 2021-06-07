import socket
import sys
from threading import Thread
import requests
from datetime import datetime

def handleGet(socket, addr):
    header = ""
    while True:
        data = socket.recv(buffer)
        header += data.decode("utf-8")
        if len(data) < buffer:
            break
    headers = list(map(str, header.strip().split("\r\n")))
    getRequest = requests.get(list(map(str, headers[0].split(" ")))[1])
    if getRequest.status_code == 200:
        currentTime = datetime.now()
        date_str = currentTime.strftime("%d/%m/%Y %H:%M:%S")
        response = "HTTP/1.0 200 OK\n"+date_str+"\n"
        socket.send(response.encode("utf-8"))
        socket.sendall(getRequest.text.encode("utf-8"))
    else:
        response = "Something Wrong Happened\n"
        socket.send(response.encode("utf-8"))


if __name__ == '__main__':
    localHost = "127.0.0.1"
    port = int(sys.argv[1])
    newSocket = socket.socket()
    try:
        newSocket.bind((localHost, port))
        newSocket.listen(10)
    except socket.error as e:
        print(str(e))
    Threads = set()
    buffer = 4096
    while True:
        print("Starting Proxy......")
        socket, addr = newSocket.accept()
        thread = Thread(target=handleGet, args=(socket, addr))
        Threads.add(thread)
        thread.start()