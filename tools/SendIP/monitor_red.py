import psutil
import time
from colorama import Fore, Style
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def obtener_estadisticas_red():
    stats = psutil.net_io_counters(pernic=True)
    return stats

def formatear_bytes(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"

def calcular_velocidad(bytes_anterior, bytes_actual, intervalo):
    bytes_transferidos = bytes_actual - bytes_anterior
    velocidad = bytes_transferidos / intervalo  # bytes por segundo
    return velocidad

def generar_grafico(tiempos, datos_entrada, datos_salida, interfaz):
    plt.style.use('seaborn')
    plt.figure(figsize=(12, 6))
    
    # Convertir datos a MB/s para mejor visualización
    datos_entrada = [x/1024/1024 for x in datos_entrada]
    datos_salida = [x/1024/1024 for x in datos_salida]
    
    plt.plot(tiempos, datos_entrada, label='Entrada', color='blue')
    plt.plot(tiempos, datos_salida, label='Salida', color='red')
    
    plt.title(f'Tráfico de Red - {interfaz}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (MB/s)')
    plt.legend()
    plt.grid(True)
    
    # Guardar gráfico
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'trafico_red_{timestamp}.png'
    plt.savefig(filename)
    plt.close()
    return filename

def ejecutar_monitor():
    print(Fore.CYAN + "\n[*] Monitor de Red en Tiempo Real" + Style.RESET_ALL)
    
    # Obtener interfaces de red disponibles
    interfaces = psutil.net_if_stats().keys()
    print("\nInterfaces de red disponibles:")
    for i, iface in enumerate(interfaces, 1):
        print(f"{i}. {iface}")
    
    # Seleccionar interfaz
    while True:
        try:
            seleccion = int(input(Fore.GREEN + "\n>_ Seleccione el número de interfaz a monitorear: " + Style.RESET_ALL))
            interfaz = list(interfaces)[seleccion-1]
            break
        except:
            print(Fore.RED + "[!] Selección inválida" + Style.RESET_ALL)
    
    # Configurar duración del monitoreo
    try:
        duracion = int(input(Fore.GREEN + ">_ Duración del monitoreo en segundos (default: 60): " + Style.RESET_ALL) or "60")
        intervalo = float(input(Fore.GREEN + ">_ Intervalo de muestreo en segundos (default: 1.0): " + Style.RESET_ALL) or "1.0")
    except:
        print(Fore.RED + "[!] Valores inválidos, usando valores por defecto" + Style.RESET_ALL)
        duracion = 60
        intervalo = 1.0
    
    print(Fore.YELLOW + f"\n[+] Iniciando monitoreo de {interfaz} por {duracion} segundos..." + Style.RESET_ALL)
    
    # Inicializar variables para el monitoreo
    tiempo_inicio = time.time()
    stats_anterior = obtener_estadisticas_red()[interfaz]
    bytes_enviados_anterior = stats_anterior.bytes_sent
    bytes_recibidos_anterior = stats_anterior.bytes_recv
    
    # Listas para almacenar datos históricos
    tiempos = []
    velocidades_entrada = []
    velocidades_salida = []
    
    try:
        while (time.time() - tiempo_inicio) < duracion:
            time.sleep(intervalo)
            
            # Obtener estadísticas actuales
            stats_actual = obtener_estadisticas_red()[interfaz]
            tiempo_actual = time.time() - tiempo_inicio
            
            # Calcular velocidades
            velocidad_entrada = calcular_velocidad(
                bytes_recibidos_anterior,
                stats_actual.bytes_recv,
                intervalo
            )
            velocidad_salida = calcular_velocidad(
                bytes_enviados_anterior,
                stats_actual.bytes_sent,
                intervalo
            )
            
            # Almacenar datos históricos
            tiempos.append(tiempo_actual)
            velocidades_entrada.append(velocidad_entrada)
            velocidades_salida.append(velocidad_salida)
            
            # Mostrar estadísticas en tiempo real
            print(f"\rTiempo: {tiempo_actual:.1f}s | "
                  f"Entrada: {formatear_bytes(velocidad_entrada)}/s | "
                  f"Salida: {formatear_bytes(velocidad_salida)}/s", end="")
            
            # Actualizar valores anteriores
            bytes_enviados_anterior = stats_actual.bytes_sent
            bytes_recibidos_anterior = stats_actual.bytes_recv
        
        print("\n\nEstadísticas Finales:")
        print("-" * 50)
        print(f"Duración total: {duracion} segundos")
        print(f"Muestras tomadas: {len(tiempos)}")
        print(f"Velocidad promedio de entrada: {formatear_bytes(sum(velocidades_entrada)/len(velocidades_entrada))}/s")
        print(f"Velocidad promedio de salida: {formatear_bytes(sum(velocidades_salida)/len(velocidades_salida))}/s")
        print(f"Velocidad máxima de entrada: {formatear_bytes(max(velocidades_entrada))}/s")
        print(f"Velocidad máxima de salida: {formatear_bytes(max(velocidades_salida))}/s")
        
        # Generar y guardar gráfico
        filename = generar_grafico(tiempos, velocidades_entrada, velocidades_salida, interfaz)
        print(f"\nGráfico guardado como: {filename}")
        
    except KeyboardInterrupt:
        print("\n\n[!] Monitoreo interrumpido por el usuario")
    except Exception as e:
        print(Fore.RED + f"\n[!] Error durante el monitoreo: {str(e)}" + Style.RESET_ALL)
    
    input(Fore.CYAN + "\nPresione Enter para continuar..." + Style.RESET_ALL)