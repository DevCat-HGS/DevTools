import requests
import json
from colorama import Fore, Style
from datetime import datetime

def obtener_info_geoip(ip):
    try:
        # Usar la API de ip-api.com para obtener información geográfica
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,continent,country,regionName,city,district,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting')
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'continente': data.get('continent', 'Desconocido'),
                    'país': data.get('country', 'Desconocido'),
                    'región': data.get('regionName', 'Desconocida'),
                    'ciudad': data.get('city', 'Desconocida'),
                    'distrito': data.get('district', 'Desconocido'),
                    'código_postal': data.get('zip', 'Desconocido'),
                    'latitud': data.get('lat', 'Desconocida'),
                    'longitud': data.get('lon', 'Desconocida'),
                    'zona_horaria': data.get('timezone', 'Desconocida'),
                    'isp': data.get('isp', 'Desconocido'),
                    'organización': data.get('org', 'Desconocida'),
                    'as': data.get('as', 'Desconocido'),
                    'es_móvil': data.get('mobile', False),
                    'es_proxy': data.get('proxy', False),
                    'es_hosting': data.get('hosting', False)
                }
        return {'error': 'No se pudo obtener la información geográfica'}
    except Exception as e:
        return {'error': f'Error al consultar la información: {str(e)}'}

def ejecutar_geoip():
    print(Fore.CYAN + "\n[*] Herramienta de Geolocalización IP" + Style.RESET_ALL)
    ip = input(Fore.GREEN + "\n>_ Ingrese la IP a geolocalizar: " + Style.RESET_ALL)
    
    print(Fore.YELLOW + "\n[+] Obteniendo información geográfica detallada..." + Style.RESET_ALL)
    
    info = obtener_info_geoip(ip)
    if 'error' not in info:
        print("\nInformación Geográfica:")
        print("-" * 50)
        print(f"Continente:\t{info['continente']}")
        print(f"País:\t\t{info['país']}")
        print(f"Región:\t\t{info['región']}")
        print(f"Ciudad:\t\t{info['ciudad']}")
        print(f"Distrito:\t{info['distrito']}")
        print(f"Código Postal:\t{info['código_postal']}")
        print(f"Coordenadas:\t{info['latitud']}, {info['longitud']}")
        print(f"Zona Horaria:\t{info['zona_horaria']}")
        
        print("\nInformación de Red:")
        print("-" * 50)
        print(f"ISP:\t\t{info['isp']}")
        print(f"Organización:\t{info['organización']}")
        print(f"AS:\t\t{info['as']}")
        
        print("\nCaracterísticas Adicionales:")
        print("-" * 50)
        print(f"Red Móvil:\t{'Sí' if info['es_móvil'] else 'No'}")
        print(f"Proxy/VPN:\t{'Sí' if info['es_proxy'] else 'No'}")
        print(f"Hosting:\t{'Sí' if info['es_hosting'] else 'No'}")
    else:
        print(Fore.RED + f"\n[!] {info['error']}" + Style.RESET_ALL)
    
    input(Fore.CYAN + "\nPresione Enter para continuar..." + Style.RESET_ALL)