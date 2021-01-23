#!/usr/bin/env python3
# made for the sake of clarity - to understand these techniques, not performance
# you can learn more at https://nmap.org/book/man-port-scanning-techniques.html
from scapy.all import *
import argparse
import os
import sys
from datetime import datetime
conf.verb = 0

def check_host(ip):
	ping = sr1(IP(dst=ip, ttl=20)/ICMP(), timeout=10)
	if not (ping is None):
		print("\033[92m[+]  Host", ip , "activo\033[0m")
		return True
	else:
		print("\033[91[-]  Host", ip, "no activo.\nParando ejecución...\033[0m")
		quit()


def get_ports(pstr):
	if "-" not in pstr:
		return int(pstr)
	else:
		ports = pstr.split("-", 1)
		ports[0] = int(ports[0])
		ports[1] = int(ports[1])
		return ports


def syn_stealth(port, ip):
	# Cliente envía SYN
	# Si el puerto está abierto, recibe SYN-ACK y envía RST para no completar el handshake
	# Si recibe RST (0x14) o no recibe respuesta, cerrado
	# Si recibe ICMP ERROR tipo 3 con códigos 1,2,3,9,10 o 13, el puerto está filtrado y no se puede saber si está A/C.
	s_port = RandShort()
	synack = sr1(IP(dst=ip)/TCP(sport=s_port,dport=port, flags='S'),timeout=10) #Enviamos un paquete desde un puerto aleatorio
	if 'NoneType' in str(type(synack)):
		print("--> Puerto", port, "\033[93mfiltrado\033[0m")
	else:
		if synack.getlayer(TCP).flags == 0x12:
			s_rst = sr1(IP(dst=ip)/TCP(sport=s_port, dport=port, flags='AR'), timeout=10)
			print("--> Puerto", port, "\033[92mabierto\033[0m")
		else:
			if not synack or synack.getlayer(TCP).flags == 0x14: # 0x14 = RST
				print("--> Puerto", port, "\033[91mcerrado\033[0m")
			elif int(synack.getlayer(ICMP).code) in [1,2,3,9,10,13]:
				print("--> Puerto", port, "\033[93mfiltrado\033[0m")


def init_ss(port, ip):
	if check_host(ip):
		if isinstance(port, list):
			port_range = range(port[0], port[1]+1)
			try:
				for i in port_range:
					syn_stealth(i, ip)
			except KeyboardInterrupt:
				sys.exit(1)
		else:
			syn_stealth(port, ip)


def tcp_connect(port, ip):
	s_port = RandShort()
	synack = sr1(IP(dst=ip)/TCP(sport=s_port,dport=port, flags='S'),timeout=10) #Enviamos un paquete desde un puerto aleatorio
	if 'NoneType' in str(type(synack)):
		print("--> Puerto", port, "\033[93mfiltrado\033[0m")
	else:
		if synack.getlayer(TCP).flags == 0x12:
			ack = sr1(IP(dst=ip)/TCP(sport=s_port, dport=port, flags='A', ack=synack[TCP].seq+1), timeout=10) #Termina el handshake
			print("--> Puerto", port, "\033[92mabierto\033[0m")
		else:
			if not synack or synack.getlayer(TCP).flags == 0x14: # 0x14 = RST
				print("--> Puerto", port, "\033[91mcerrado\033[0m")
			elif int(synack.getlayer(ICMP).code) in [1,2,3,9,10,13]:
				print("--> Puerto", port, "\033[93mfiltrado\033[0m")


def init_st(port, ip):
        if check_host(ip):
                if isinstance(port, list):
                        port_range = range(port[0], port[1]+1)
                        try:
                                for i in port_range:
                                        tcp_connect(i, ip)
                        except KeyboardInterrupt:
                                sys.exit(1)
                else:
                        tcp_connect(port, ip)


def udp_connect(port, ip):
	udp_resp = sr1(IP(dst=ip)/UDP(dport=port),timeout=5)
	if 'NoneType' in str(type(udp_resp)):
		print("--> Puerto", port, "\033[92mabierto|filtrado\033[0m")
	elif udp_resp.haslayer(UDP):
		print("--> Puerto", port, "\033[92mabierto\033[0m")
	elif udp_resp.haslayer(ICMP):
		if int(udp_resp.getlayer(ICMP).type)==3 and int(udp_resp.getlayer(ICMP).code) == 3:
			print("--> Puerto", port, "\033[91mcerrado\033[0m")
		elif int(udp_resp.getlayer(ICMP).type)==3 and int(udp_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]:
			print("--> Puerto", port, "\033[93mfiltrado\033[0m")


def init_su(port, ip):
        if check_host(ip):
                if isinstance(port, list):
                        port_range = range(port[0], port[1]+1)
                        try:
                                for i in port_range:
                                        udp_connect(i, ip)
                        except KeyboardInterrupt:
                                sys.exit(1)
                else:
                        udp_connect(port, ip)


def xmas_scan(port, ip):
	# Se envía un paquete TCP con las flags PSH, FIN y URG.
	# Si está abierto, no recibe respuesta.
	xmas_resp = sr1(IP(dst=ip)/TCP(dport=port, flags="FPU"), timeout=10)
	if not xmas_resp or str(type(xmas_resp))=="<class 'NoneType'>":
		print("--> Puerto", port, "\033[92mabierto|filtrado\033[0m")
	elif xmas_resp.getlayer(TCP).flags == 0x14:
		print("--> Puerto", port, "\033[91mcerrado\033[0m")
	elif int(synack.getlayer(ICMP).type)==3 and int(synack.getlayer(ICMP).type) in [1,2,3,9,10,13]:
		print("--> Puerto", port, "\033[93mfiltrado\033[0m")



def init_sx(port, ip):
        if check_host(ip):
                if isinstance(port, list):
                        port_range = range(port[0], port[1]+1)
                        try:
                                for i in port_range:
                                        xmas_scan(i, ip)
                        except KeyboardInterrupt:
                                sys.exit(1)
                else:
                        xmas_scan(port, ip)


def start_scan(options):
	modes = {
		"sS":init_ss,
		"sT":init_st,
		"sU":init_su,
		"sX":init_sx,
	}
	scan = modes.get(options.mode, lambda:"Modo incorrecto")
	port = get_ports(options.port)
	print(" Puerto/Rango de puertos:", port)
	print("---------------------------------------------------------------------------")
	scan(port, options.target)


def get_options():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', dest='target', help='Dirección IP objetivo', required=True)
	parser.add_argument('-m', '--mode', dest='mode', help='Modo de escaneo. sS  (TCP SYN Stealth scan), sT (TCP Connect Scan), sU (UDP Scan), sX (XMAS Scan)', required=True)
	parser.add_argument('-p', '--port', dest='port', help='Puerto o rango de puertos, de la forma pInicial-pFinal', required=True)
	options = parser.parse_args()

	return options


os.system('clear')
print("\n")
print("\033[1m\033[91m__̴ı̴̴̡̡̡ ̡͌l̡̡̡ ̡͌l̡*̡̡ ̴̡ı̴̴̡ ̡̡͡|̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|̡̡̡ ̡ ̴̡ı̴̡̡ ̡͌l̡̡̡̡.___  portScanner.py __̴ı̴̴̡̡̡ ̡͌l̡̡̡ ̡͌l̡*̡̡ ̴̡ı̴̴̡ ̡̡͡|̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|̡̡̡ ̡ ̴̡ı̴̡̡ ̡͌l̡̡̡̡.___\033[0m")
print("---------------------------------------------------------------------------")
print("[!] USO:")
print("-> -t, --target :  dirección IP objetivo")
print("-> -m, --mode : modo de scaneo.\n	- sS  (TCP SYN Stealth scan)\n	- sT (TCP Connect Scan)\n	- sU (UDP Scan)\n 	- sX (XMAS Scan)'")
print("-> -p, --port,ports : puerto o rango de puertos. EJ: 1-40")
print("---------------------------------------------------------------------------")
options = get_options()
print("\n---- Iniciando escaneo ----")
print(" OBJETIVO: ", options.target)
print(" MODO: ", options.mode)
init_time = datetime.now()
start_scan(options)
print("Escaneo finalizado tras", datetime.now() - init_time, "segundos")
