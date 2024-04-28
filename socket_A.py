import socket


def service_a():
    # Establish a connection with Service B
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))

    # Send a request to Service B
    request = b'Request'
    sock.sendall(request)

    # Receive and process multiple responses from Service B
    while True:
        response = sock.recv(1024)
        if not response:
            break
        print('Received:', response.decode())

    # Close the connection
    sock.close()


if __name__ == '__main__':
    service_a()
