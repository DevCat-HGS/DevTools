import os
import sys
import dns.resolver
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

def scan_subdominio(dominio, subdominio):
    try:
        url = f"http://{subdominio}.{dominio}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return subdominio
    except:
        pass
    return None

def ejecutar_scanner_subdominios():
    print(Fore.CYAN + "\n=== Escáner de Subdominios ===")
    dominio = input(Fore.GREEN + "\n>_ Ingrese el dominio objetivo (ejemplo.com): " + Style.RESET_ALL)
    
    try:
        # Lista de subdominios comunes para escanear
        subdominios = [
            'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test',
            'api', 'secure', 'shop', 'store', 'portal', 'cloud',
            'webmail', 'cpanel', 'support', 'forum', 'docs'
        ]
        
        print(Fore.YELLOW + "\n[*] Iniciando escaneo de subdominios...")
        
        # Usar ThreadPoolExecutor para escaneo paralelo
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scan_subdominio, dominio, sub) for sub in subdominios]
            subdominios_encontrados = [f.result() for f in futures if f.result() is not None]
        
        if subdominios_encontrados:
            print(Fore.GREEN + "\n[+] Subdominios encontrados:")
            for sub in subdominios_encontrados:
                print(Fore.CYAN + f"    - {sub}.{dominio}")
        else:
            print(Fore.RED + "\n[-] No se encontraron subdominios activos.")
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Escaneo interrumpido por el usuario.")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}")
    
    print(Style.RESET_ALL)