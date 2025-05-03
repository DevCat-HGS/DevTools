import os
import sys
import dns.resolver
from colorama import Fore, Style

def consultar_registros_dns(dominio, tipo_registro):
    try:
        respuesta = dns.resolver.resolve(dominio, tipo_registro)
        return [str(rdata) for rdata in respuesta]
    except Exception as e:
        return None

def ejecutar_verificador_dns():
    print(Fore.CYAN + "\n=== Verificador de DNS ===")
    dominio = input(Fore.GREEN + "\n>_ Ingrese el dominio a analizar: " + Style.RESET_ALL)
    
    try:
        # Tipos de registros DNS a consultar
        tipos_registro = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        print(Fore.YELLOW + "\n[*] Consultando registros DNS...")
        
        for tipo in tipos_registro:
            registros = consultar_registros_dns(dominio, tipo)
            
            if registros:
                print(Fore.GREEN + f"\n[+] Registros {tipo}:")
                for registro in registros:
                    print(Fore.CYAN + f"    - {registro}")
            else:
                print(Fore.RED + f"\n[-] No se encontraron registros {tipo}")
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Verificación interrumpida por el usuario.")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}")
    
    print(Style.RESET_ALL)