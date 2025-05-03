import socket
import platform
import subprocess
import re
import nmap  # Asegúrate de tener instalado python-nmap
from tqdm import tqdm  # Para la barra de progreso

def ping_host(ip):
    print(f"[+] Haciendo ping a {ip}...")
    parametro = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", parametro, "1", ip]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if resultado.returncode == 0:
        print("[✔] IP Activa")
        return True, resultado.stdout
    else:
        print("[✘] IP Inactiva")
        return False, resultado.stdout

def obtener_ttl(salida_ping):
    ttl_match = re.search(r"ttl[=|:](\d+)", salida_ping.lower())
    if ttl_match:
        ttl = int(ttl_match.group(1))

        # Valores comunes de TTL predeterminados por sistema o dispositivo
        if ttl <= 30:
            dispositivo = "Probablemente un dispositivo embebido (IoT, routers, firewalls)"
        elif 31 <= ttl <= 64:
            if ttl in [32, 60, 64]:
                dispositivo = "Linux/Unix, BSD o Android"
            elif ttl < 50:
                dispositivo = "Dispositivo de red intermedio o personalizado"
            else:
                dispositivo = "Linux/Unix o sistema basado en POSIX"
        elif 65 <= ttl <= 128:
            if ttl in [128]:
                dispositivo = "Windows (default)"
            elif ttl in [100, 106, 108]:
                dispositivo = "Windows modificado o dispositivos Cisco"
            else:
                dispositivo = "Windows o servidor intermedio"
        elif 129 <= ttl <= 255:
            if ttl == 255:
                dispositivo = "Cisco, Solaris, FreeBSD, macOS o red protegida"
            elif ttl > 200:
                dispositivo = "POSIX-like con configuración alta o red de seguridad"
            else:
                dispositivo = "Dispositivo desconocido con TTL alto (posible spoofing o NAT)"
        else:
            dispositivo = "TTL fuera de rango conocido"
        return ttl, dispositivo

    return None, "No se pudo determinar el TTL"


def escanear_puertos(ip):
    print(f"[+] Iniciando análisis exhaustivo de puertos en {ip}...")
    scanner = nmap.PortScanner()
    try:
        # Escaneo completo con detección de versiones y scripts de vulnerabilidades
        print("[*] Fase 1: Escaneo inicial de puertos...")
        # Primero obtenemos el total de puertos a escanear (65535)
        total_puertos = 65535
        with tqdm(total=total_puertos, desc="Escaneando puertos", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            scanner.scan(ip, arguments='-p- -T4 --min-rate 1000')
            pbar.update(total_puertos)  # Completamos la barra cuando termina el escaneo inicial
        
        puertos_abiertos = []
        for protocolo in scanner[ip].all_protocols():
            puertos = scanner[ip][protocolo].keys()
            for puerto in puertos:
                if scanner[ip][protocolo][puerto]['state'] == 'open':
                    puertos_abiertos.append(str(puerto))
        
        if not puertos_abiertos:
            print("[i] No se encontraron puertos abiertos.")
            return []
        
        puertos_str = ','.join(puertos_abiertos)
        print(f"[+] Encontrados {len(puertos_abiertos)} puertos abiertos. Analizando servicios y vulnerabilidades...")
        
        # Escaneo detallado de los puertos abiertos
        with tqdm(total=len(puertos_abiertos), desc="Analizando servicios", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            scanner.scan(ip, ports=puertos_str, arguments='-sC -sV -A --version-intensity 5')
            pbar.update(len(puertos_abiertos))  # Completamos la barra cuando termina el análisis
        
        resultados = []
        for protocolo in scanner[ip].all_protocols():
            puertos = scanner[ip][protocolo].keys()
            for puerto in puertos:
                info = scanner[ip][protocolo][puerto]
                servicio = info.get('name', 'desconocido')
                version = info.get('version', 'desconocida')
                producto = info.get('product', 'desconocido')
                scripts = info.get('script', {})
                
                vulnerabilidades = []
                for script_name, output in scripts.items():
                    if any(x in script_name.lower() for x in ['vuln', 'exploit', 'security', 'unsafe']):
                        vulnerabilidades.append(f"{script_name}: {output}")
                
                resultados.append({
                    'puerto': puerto,
                    'protocolo': protocolo,
                    'servicio': servicio,
                    'version': version,
                    'producto': producto,
                    'vulnerabilidades': vulnerabilidades
                })
        
        return resultados
    except Exception as e:
        print(f"[!] Error durante el escaneo: {e}")
        return []

def ejecutar():
    ip = input("Ingresa la IP a analizar: ").strip()
    activa, salida_ping = ping_host(ip)
    
    if activa:
        ttl, sistema = obtener_ttl(salida_ping)
        print(f"[i] TTL: {ttl} → Probable sistema: {sistema}")
        
        resultados = escanear_puertos(ip)
        if resultados:
            print("\n[+] Análisis detallado de puertos y servicios:")
            for info in resultados:
                print(f"\n[*] Puerto {info['puerto']}/{info['protocolo']}:")
                print(f"  - Servicio: {info['servicio']}")
                print(f"  - Producto: {info['producto']}")
                print(f"  - Versión: {info['version']}")
                
                if info['vulnerabilidades']:
                    print("  - Vulnerabilidades detectadas:")
                    for vuln in info['vulnerabilidades']:
                        print(f"    → {vuln}")
                else:
                    print("  - No se detectaron vulnerabilidades conocidas")
        else:
            print("[i] No se detectaron puertos abiertos.")
    else:
        print("[!] No se puede obtener más información porque la IP no está activa.")
