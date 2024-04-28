import socket
import time


def service_b():
    # Create a socket and listen for incoming connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8005))
    sock.listen(1)
    print('Service B is listening...')

    # Accept a connection from Service A
    conn, addr = sock.accept()
    print('Service B connected to', addr)

    # Process the request from Service A and send multiple responses
    request = conn.recv(1024)
    if not request:
        return
    print('Received request:', request.decode())

    # Simulate progress by sending multiple responses
    response = f'Encoding the image in latent space...'.encode()
    conn.sendall(response)
    time.sleep(2)

    response = f'Forward diffusing the latents...'.encode()
    conn.sendall(response)
    time.sleep(3)

    response = f'Removing Gaussian noise...'.encode()
    conn.sendall(response)
    time.sleep(5)

    response = f'Decoding the latents into video...'.encode()
    conn.sendall(response)
    time.sleep(2)
    # Close the connection
    conn.close()
    sock.close()


if __name__ == '__main__':
    service_b()
