import subprocess
import platform
import socket
import json
import requests
from colorama import Fore, Style
from datetime import datetime

def obtener_info_salto(ip):
    try:
        # Obtener nombre del host
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "No disponible"
            
        # Obtener información de geolocalización
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                data = response.json()
                geo_info = {
                    'país': data.get('country', 'Desconocido'),
                    'ciudad': data.get('city', 'Desconocida'),
                    'isp': data.get('isp', 'Desconocido'),
                    'org': data.get('org', 'Desconocida')
                }
            else:
                geo_info = {'error': 'No se pudo obtener información geográfica'}
        except:
            geo_info = {'error': 'Error al consultar información geográfica'}
            
        return {
            'hostname': hostname,
            'geo_info': geo_info
        }
    except Exception as e:
        return {'error': str(e)}

def ejecutar_traceroute():
    print(Fore.CYAN + "\n[*] Herramienta de Traceroute Avanzado" + Style.RESET_ALL)
    destino = input(Fore.GREEN + "\n>_ Ingrese la IP o dominio destino: " + Style.RESET_ALL)
    
    # Determinar el comando según el sistema operativo
    if platform.system().lower() == "windows":
        comando = ["tracert", "-d", destino]
    else:
        comando = ["traceroute", "-n", destino]
    
    print(Fore.YELLOW + "\n[+] Iniciando traceroute avanzado..." + Style.RESET_ALL)
    print("\nSalto\tIP\t\tLatencia\tHostname\t\tUbicación\t\tISP")
    print("-" * 100)
    
    try:
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salto_actual = 0
        
        for linea in proceso.stdout:
            if "*" in linea or "Request timed out" in linea:
                continue
                
            # Extraer IP y latencia de la línea
            partes = linea.split()
            if len(partes) >= 8:  # Asegurarse de que hay suficientes partes
                try:
                    salto_actual += 1
                    ip = partes[7]
                    latencia = partes[4].replace('ms', '') + ' ms'
                    
                    # Obtener información adicional del salto
                    info_salto = obtener_info_salto(ip)
                    hostname = info_salto['hostname']
                    geo_info = info_salto['geo_info']
                    
                    # Formatear y mostrar la información
                    print(f"{salto_actual}\t{ip}\t{latencia}\t{hostname[:20]}\t{geo_info['ciudad']}, {geo_info['país']}\t{geo_info['isp'][:30]}")
                except:
                    print(f"{salto_actual}\t{ip}\t{latencia}\tNo disponible\t\tNo disponible\t\tNo disponible")
    
    except Exception as e:
        print(Fore.RED + f"\n[!] Error durante el traceroute: {str(e)}" + Style.RESET_ALL)
    
    input(Fore.CYAN + "\nPresione Enter para continuar..." + Style.RESET_ALL)