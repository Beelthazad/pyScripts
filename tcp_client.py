import socket, sys

t_host = sys.argv[1]
t_port = 80

if "www." not in sys.argv[1]:
    t_host = "www."+sys.argv[1]

if t_host is not None:
    # Crea un objeto socket que use una dirección o hostname IPv4 (IF_INET) usando TCP (SOCK_STREAM)
     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     client.connect((t_host, t_port))
     # Envía datos
     eq = str.encode("GET / HTTP/1.1\r\nHost: "+t_host+"\r\n\r\n")
     client.send(req)
     resp = client.recv(4096)
     print(resp.decode(errors="ignore"))
