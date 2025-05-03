import subprocess
import platform
import statistics
from colorama import Fore, Style
from datetime import datetime
import time
import matplotlib.pyplot as plt
import numpy as np

def analizar_latencia(host, num_pings=100):
    parametro = "-n" if platform.system().lower() == "windows" else "-c"
    tiempos = []
    perdidos = 0
    jitter = []
    
    print(Fore.YELLOW + f"\n[+] Iniciando análisis de latencia con {num_pings} pings..." + Style.RESET_ALL)
    
    for i in range(num_pings):
        comando = ["ping", parametro, "1", host]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if resultado.returncode == 0:
            # Extraer el tiempo de respuesta
            tiempo_str = resultado.stdout.split("tiempo=")[-1].split("ms")[0].strip()
            try:
                tiempo = float(tiempo_str)
                tiempos.append(tiempo)
                if len(tiempos) > 1:
                    jitter.append(abs(tiempos[-1] - tiempos[-2]))
            except:
                perdidos += 1
        else:
            perdidos += 1
        
        # Mostrar progreso
        print(f"\rProgreso: {i+1}/{num_pings} pings completados", end="")
    
    print("\n")
    return tiempos, perdidos, jitter

def generar_grafico(tiempos, jitter):
    # Configurar el estilo del gráfico
    plt.style.use('seaborn')
    
    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Gráfico de latencia
    ax1.plot(tiempos, color='blue', label='Latencia')
    ax1.set_title('Análisis de Latencia')
    ax1.set_xlabel('Número de Ping')
    ax1.set_ylabel('Latencia (ms)')
    ax1.grid(True)
    
    # Gráfico de jitter
    ax2.plot(jitter, color='green', label='Jitter')
    ax2.set_title('Análisis de Jitter')
    ax2.set_xlabel('Número de Ping')
    ax2.set_ylabel('Jitter (ms)')
    ax2.grid(True)
    
    plt.tight_layout()
    
    # Guardar gráfico
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'latencia_analisis_{timestamp}.png'
    plt.savefig(filename)
    plt.close()
    return filename

def ejecutar_analisis_latencia():
    print(Fore.CYAN + "\n[*] Analizador de Latencia" + Style.RESET_ALL)
    host = input(Fore.GREEN + "\n>_ Ingrese el host a analizar: " + Style.RESET_ALL)
    num_pings = int(input(Fore.GREEN + ">_ Número de pings a realizar (recomendado: 100): " + Style.RESET_ALL) or "100")
    
    tiempos, perdidos, jitter = analizar_latencia(host, num_pings)
    
    if tiempos:
        # Calcular estadísticas
        min_latencia = min(tiempos)
        max_latencia = max(tiempos)
        avg_latencia = statistics.mean(tiempos)
        std_latencia = statistics.stdev(tiempos) if len(tiempos) > 1 else 0
        avg_jitter = statistics.mean(jitter) if jitter else 0
        
        # Mostrar resultados
        print("\nResultados del Análisis:")
        print("-" * 50)
        print(f"Paquetes enviados:\t{num_pings}")
        print(f"Paquetes recibidos:\t{len(tiempos)}")
        print(f"Paquetes perdidos:\t{perdidos} ({(perdidos/num_pings)*100:.2f}%)")
        print("\nEstadísticas de Latencia:")
        print("-" * 50)
        print(f"Mínima:\t\t{min_latencia:.2f} ms")
        print(f"Máxima:\t\t{max_latencia:.2f} ms")
        print(f"Promedio:\t{avg_latencia:.2f} ms")
        print(f"Desv. Estándar:\t{std_latencia:.2f} ms")
        print(f"Jitter promedio:\t{avg_jitter:.2f} ms")
        
        # Generar y guardar gráfico
        filename = generar_grafico(tiempos, jitter)
        print(f"\nGráfico guardado como: {filename}")
        
        # Evaluación de la calidad
        print("\nEvaluación de la Calidad:")
        print("-" * 50)
        if avg_latencia < 50 and avg_jitter < 10 and perdidos == 0:
            print(Fore.GREEN + "Excelente - Ideal para aplicaciones en tiempo real" + Style.RESET_ALL)
        elif avg_latencia < 100 and avg_jitter < 20 and perdidos/num_pings < 0.01:
            print(Fore.CYAN + "Buena - Adecuada para la mayoría de aplicaciones" + Style.RESET_ALL)
        elif avg_latencia < 150 and avg_jitter < 30 and perdidos/num_pings < 0.05:
            print(Fore.YELLOW + "Regular - Puede causar problemas en aplicaciones sensibles" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Pobre - Problemas de rendimiento probables" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[!] No se pudieron obtener mediciones válidas" + Style.RESET_ALL)
    
    input(Fore.CYAN + "\nPresione Enter para continuar..." + Style.RESET_ALL)