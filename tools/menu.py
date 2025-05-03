import os
import sys
from colorama import Fore, Style

def show_menu():
    while True:
        print(Fore.CYAN + "\n=== Herramientas de Desarrollo ===")
        print(Fore.YELLOW + "\nSeleccione una opción:")
        
        # Lista de herramientas disponibles
        tools = [
            "Send IP",
            "Japan",
            "Herramienta 3"
        ]
        
        # Mostrar opciones numeradas
        for i, tool in enumerate(tools, 1):
            print(f"[{i}] {tool}")
        
        print(Fore.RED + "[0] Salir" + Style.RESET_ALL)
        
        try:
            option = input(Fore.GREEN + "\n>_ Ingrese una opción: " + Style.RESET_ALL)
            if not option.isdigit():
                print(Fore.RED + "\n[!] Por favor, ingrese un número válido." + Style.RESET_ALL)
                continue
                
            option = int(option)
            
            if option == 0:
                print(Fore.YELLOW + "\n[*] Saliendo..." + Style.RESET_ALL)
                sys.exit(0)
            elif 1 <= option <= len(tools):
                if option == 1:  # Send IP
                    from tools.send_ip import show_send_ip_menu
                    show_send_ip_menu()
                elif option == 2:  # Japan
                    from tools.japan import show_japan_menu
                    show_japan_menu()
                else:
                    print(f"\n[*] Ejecutando {tools[option-1]}...")
                    # Aquí se implementará la lógica para ejecutar cada herramienta
                    input(Fore.CYAN + "\nPresione Enter para continuar..." + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n[!] Opción no válida" + Style.RESET_ALL)
                
        except ValueError:
            print(Fore.RED + "\n[!] Por favor, ingrese un número válido." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\n[*] Saliendo..." + Style.RESET_ALL)
            sys.exit(0)

if __name__ == '__main__':
    show_menu()