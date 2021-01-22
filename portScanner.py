#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import os


def get_options():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', dest='target', help='Dirección IP objetivo', required=True)
	parser.add_argument('-m', '--mode', dest='mode', help='Modo de escaneo. sS  (TCP SYN Stealth scan), sT (TCP Connect Scan), sU (UDP Scan), sI (ICMP Scan)', required=True)
	parser.add_argument('-p', '--port', dest='port', help='Puerto o rango de puertos, de la forma pInicial-pFinal', required=True)
	options = parser.parse_args()

	return options


os.system('clear')
print("\n")
print("__̴ı̴̴̡̡̡ ̡͌l̡̡̡ ̡͌l̡*̡̡ ̴̡ı̴̴̡ ̡̡͡|̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|̡̡̡ ̡ ̴̡ı̴̡̡ ̡͌l̡̡̡̡.___  portScanner.py __̴ı̴̴̡̡̡ ̡͌l̡̡̡ ̡͌l̡*̡̡ ̴̡ı̴̴̡ ̡̡͡|̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|̡̡̡ ̡ ̴̡ı̴̡̡ ̡͌l̡̡̡̡.___")
print("---------------------------------------------------------------------------")
print("[!] USO:")
print("-> -t, --target :  dirección IP objetivo")
print("-> -m, --mode : modo de scaneo.\n	- sS  (TCP SYN Stealth scan)\n	- sT (TCP Connect Scan)\n	- sU (UDP Scan)\n 	- sI (ICMP Scan)'")
print("-> -p, --port,ports : puerto o rango de puertos. EJ: 1-40")
print("---------------------------------------------------------------------------")
options = get_options()
print("\n---- Iniciando escaneo ----")
print(" OBJETIVO: ", options.target)
print(" MODO: ", options.mode)
print(" PUERTOS: ", options.port)
