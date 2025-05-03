import os
import sys
from colorama import Fore, Style

def show_japan_banner():
    banner = f"""
    {Fore.CYAN}
    ┌───────────────────────────────────────────────────────────┐
    │     ██╗ █████╗ ██████╗  █████╗ ███╗   ██╗                 │
    │     ██║██╔══██╗██╔══██╗██╔══██╗████╗  ██║                 │
    │     ██║███████║██████╔╝███████║██╔██╗ ██║                 │
    │██   ██║██╔══██║██╔═══╝ ██╔══██║██║╚██╗██║                 │
    │╚█████╔╝██║  ██║██║     ██║  ██║██║ ╚████║                 │
    │ ╚════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝                 │
    │                                                           │
    │           >_ Herramientas de Spoofing                     │
    │           >_ By DevHarold    🎌                          │
    └───────────────────────────────────────────────────────────┘
    """
    print(banner + Style.RESET_ALL)
    print(Fore.CYAN + '\n        [ Módulo: ' + Fore.GREEN + 'Japan' + Fore.CYAN + ' | Version: ' + Fore.GREEN + '1.0' + Fore.CYAN + ' ]' + Style.RESET_ALL)

def show_japan_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_japan_banner()
        print(Fore.YELLOW + "\nSeleccione una herramienta:")
        
        tools = [
            "SMS Bomber",
            "Call Bomber",
            "Mail Bomber",
            "Whatsapp Bomber",
            "Facebook Bomber",
            "Instagram Bomber",
            "Twitter Bomber",
            "Telegram Bomber",
            "Discord Bomber"
        ]
        
        for i, tool in enumerate(tools, 1):
            print(f"[{i}] {tool}")
            
        print(Fore.RED + "[0] Volver al Menú Principal" + Style.RESET_ALL)
        
        try:
            option = input(Fore.GREEN + "\n>_ Ingrese una opción: " + Style.RESET_ALL)
            if not option.isdigit():
                print(Fore.RED + "\n[!] Por favor, ingrese un número válido." + Style.RESET_ALL)
                continue
                
            option = int(option)
            
            if option == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                from banner import show_banner
                show_banner()
                return
            elif 1 <= option <= len(tools):
                print(f"\n[*] Ejecutando {tools[option-1]}...")
                # Aquí se implementará la lógica para cada herramienta
                input(Fore.CYAN + "\nPresione Enter para continuar..." + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n[!] Opción no válida" + Style.RESET_ALL)
                
        except ValueError:
            print(Fore.RED + "\n[!] Por favor, ingrese un número válido." + Style.RESET_ALL)
        except KeyboardInterrupt:
            return

if __name__ == '__main__':
    show_japan_menu()