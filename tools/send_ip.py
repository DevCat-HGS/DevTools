import os
import sys
from colorama import Fore, Style
import random
from tools.SendIP.analizar_ip import ejecutar

def show_send_ip_banner():
    colors = [Fore.BLUE]
    banner = f"""
    {random.choice(colors)}
    ┌─────────────────────────────────────────────────────────────┐
    │   ███████╗███████╗███╗   ██╗██████╗     ██╗██████╗          │
    │   ██╔════╝██╔════╝████╗  ██║██╔══██╗    ██║██╔══██╗         │
    │   ███████╗█████╗  ██╔██╗ ██║██║  ██║    ██║██████╔╝         │
    │   ╚════██║██╔══╝  ██║╚██╗██║██║  ██║    ██║██╔═══╝          │
    │   ███████║███████╗██║ ╚████║██████╔╝    ██║██║              │
    │   ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝     ╚═╝╚═╝              │
    │                                                             │
    │              >_ Herramientas de IP                          │
    │              >_ by DevHarold 🌐                            │
    └─────────────────────────────────────────────────────────────┘
    """
    print(banner + Style.RESET_ALL)
    print(Fore.CYAN + '\n        [ Módulo: ' + Fore.GREEN + 'Send IP' + Fore.CYAN + ' | Estado: ' + Fore.GREEN + 'Activo' + Fore.CYAN + ' ]' + Style.RESET_ALL)

def show_send_ip_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_send_ip_banner()
        print(Fore.YELLOW + "\nOpciones disponibles:")
        
        options = [
            "Analisis de IP",
            "Ataque DDoS",
            "Traceroute Avanzado",
            "Geolocalización IP",
            "Analizador de Latencia",
            "Monitor de Red",
            "Escáner de Subdominios",
            "Detector de WAF",
            "Analizador de Certificados SSL",
            "Verificador de DNS"
        ]
        
        for i, option in enumerate(options, 1):
            print(f"[{i}] {option}")
            
        print(Fore.RED + "[0] Volver al menú principal" + Style.RESET_ALL)
        
        try:
            choice = input(Fore.GREEN + "\n>_ Seleccione una opción: " + Style.RESET_ALL)
            if not choice.isdigit():
                print(Fore.RED + "\n[!] Por favor, ingrese un número válido." + Style.RESET_ALL)
                input("\nPresione Enter para continuar...")
                continue
                
            choice = int(choice)
            
            if choice == 0:
                from banner import show_banner
                os.system('cls' if os.name == 'nt' else 'clear')
                show_banner()
                return
            elif 1 <= choice <= len(options):
                print(f"\n[*] Ejecutando: {options[choice-1]}...")
                if choice == 1:  # Análisis de IP
                    ejecutar()
                elif choice == 2:  # Ataque DDoS
                    from tools.SendIP.ddos_attack import ejecutar_ddos
                    ejecutar_ddos()
                elif choice == 3:  # Traceroute Avanzado
                    from tools.SendIP.traceroute_avanzado import ejecutar_traceroute
                    ejecutar_traceroute()
                elif choice == 4:  # Geolocalización IP
                    from tools.SendIP.geolocalizacion_ip import ejecutar_geoip
                    ejecutar_geoip()
                elif choice == 5:  # Analizador de Latencia
                    from tools.SendIP.analizador_latencia import ejecutar_analisis_latencia
                    ejecutar_analisis_latencia()
                elif choice == 6:  # Monitor de Red
                    from tools.SendIP.monitor_red import ejecutar_monitor
                    ejecutar_monitor()
                elif choice == 7:  # Escáner de Subdominios
                    from tools.SendIP.scanner_subdominios import ejecutar_scanner_subdominios
                    ejecutar_scanner_subdominios()
                elif choice == 8:  # Detector de WAF
                    from tools.SendIP.detector_waf import ejecutar_detector_waf
                    ejecutar_detector_waf()
                elif choice == 9:  # Analizador de Certificados SSL
                    from tools.SendIP.analizador_ssl import ejecutar_analizador_ssl
                    ejecutar_analizador_ssl()
                elif choice == 10:  # Verificador de DNS
                    from tools.SendIP.verificador_dns import ejecutar_verificador_dns
                    ejecutar_verificador_dns()
                input(Fore.CYAN + "\nPresione Enter para continuar..." + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n[!] Opción no válida" + Style.RESET_ALL)
                input("\nPresione Enter para continuar...")
                
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(Fore.RED + f"\n[!] Error: {str(e)}" + Style.RESET_ALL)
            input("\nPresione Enter para continuar...")