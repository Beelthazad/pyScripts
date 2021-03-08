import sys, socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8081)
print('[+] Iniciando en {}:{}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('[*] Esperando conexión')
    connection, client_address = sock.accept()
    try:
        print('[!] Conexión desde ', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('Recibido {!r}'.format(data))
            if data:
                print('[!] Reenviando datos al cliente...')
                connection.sendall(data)
            else:
                print('[X] NO se recibieron datos', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
