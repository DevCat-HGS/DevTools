import os
import sys
import socket
import ssl
from datetime import datetime
from colorama import Fore, Style

def analizar_certificado_ssl(dominio, puerto=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((dominio, puerto)) as sock:
            with context.wrap_socket(sock, server_hostname=dominio) as ssock:
                cert = ssock.getpeercert()
                
                # Extraer información relevante
                emisor = dict(x[0] for x in cert['issuer'])
                sujeto = dict(x[0] for x in cert['subject'])
                fecha_inicio = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                fecha_fin = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                
                return {
                    'emisor': emisor.get('organizationName', 'N/A'),
                    'sujeto': sujeto.get('commonName', 'N/A'),
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'version': cert.get('version', 'N/A'),
                    'algoritmo': cert.get('signatureAlgorithm', 'N/A'),
                    'serial': cert.get('serialNumber', 'N/A')
                }
    except Exception as e:
        return None

def ejecutar_analizador_ssl():
    print(Fore.CYAN + "\n=== Analizador de Certificados SSL ===")
    dominio = input(Fore.GREEN + "\n>_ Ingrese el dominio a analizar: " + Style.RESET_ALL)
    
    try:
        print(Fore.YELLOW + "\n[*] Analizando certificado SSL...")
        
        info_cert = analizar_certificado_ssl(dominio)
        
        if info_cert:
            print(Fore.GREEN + "\n[+] Información del Certificado SSL:")
            print(Fore.CYAN + f"\n    Emisor: {info_cert['emisor']}")
            print(f"    Dominio: {info_cert['sujeto']}")
            print(f"    Válido desde: {info_cert['fecha_inicio'].strftime('%Y-%m-%d')}")
            print(f"    Válido hasta: {info_cert['fecha_fin'].strftime('%Y-%m-%d')}")
            print(f"    Versión: {info_cert['version']}")
            print(f"    Algoritmo de firma: {info_cert['algoritmo']}")
            print(f"    Número de serie: {info_cert['serial']}")
            
            # Verificar si el certificado está próximo a expirar
            dias_restantes = (info_cert['fecha_fin'] - datetime.now()).days
            if dias_restantes < 30:
                print(Fore.RED + f"\n[!] Advertencia: El certificado expirará en {dias_restantes} días.")
        else:
            print(Fore.RED + "\n[-] No se pudo obtener información del certificado SSL.")
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Análisis interrumpido por el usuario.")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}")
    
    print(Style.RESET_ALL)