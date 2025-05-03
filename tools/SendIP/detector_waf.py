import os
import sys
import requests
from colorama import Fore, Style

def detectar_waf(url):
    # Firmas comunes de WAF
    waf_signatures = {
        'Cloudflare': ['__cfduid', 'cf-ray', 'cloudflare'],
        'ModSecurity': ['mod_security', 'NOYB'],
        'AWS WAF': ['x-amzn-RequestId', 'x-amz-cf-id'],
        'Imperva': ['incap_ses_', '_incap_'],
        'Akamai': ['akamai'],
        'F5 BIG-IP': ['BigIP', 'F5'],
        'Sucuri': ['sucuri'],
        'Fortinet': ['fortigate']
    }
    
    try:
        # Realizar petición con headers personalizados para provocar respuesta del WAF
        headers = {
            'User-Agent': 'WAFTest/1.0',
            'X-Forwarded-For': '127.0.0.1',
            'Accept': '*/*'
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        headers_str = str(response.headers).lower()
        
        waf_detectado = []
        for waf, signatures in waf_signatures.items():
            for signature in signatures:
                if signature.lower() in headers_str:
                    waf_detectado.append(waf)
                    break
        
        return list(set(waf_detectado))
        
    except Exception as e:
        return None

def ejecutar_detector_waf():
    print(Fore.CYAN + "\n=== Detector de WAF ===")
    url = input(Fore.GREEN + "\n>_ Ingrese la URL del sitio web a analizar: " + Style.RESET_ALL)
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        print(Fore.YELLOW + "\n[*] Analizando la presencia de WAF...")
        
        waf_detectado = detectar_waf(url)
        
        if waf_detectado:
            print(Fore.GREEN + "\n[+] WAF detectado:")
            for waf in waf_detectado:
                print(Fore.CYAN + f"    - {waf}")
        else:
            print(Fore.RED + "\n[-] No se detectó ningún WAF conocido.")
            print(Fore.YELLOW + "    Nota: El sitio podría estar usando un WAF no reconocido.")
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Detección interrumpida por el usuario.")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}")
    
    print(Style.RESET_ALL)