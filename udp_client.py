import socket, sys

t_host = "127.0.0.1"
t_port = 80


if t_host is not None:
    # Crea un objeto socket que use una dirección o hostname IPv4 (IF_INET) usando UDP (SOCK_DGRAM)
     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     #client.connect((t_host, t_port)) --> UDP is CONNECTIONLESS, dude!
     # Envía datos
     req = str.encode("AABBCC")
     client.sendto(req, (t_host, t_port))
     resp, addr = client.recvfrom(1024)
     print(resp.decode(errors="ignore"))
