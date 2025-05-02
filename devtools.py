import sys
import time
import os
from colorama import init, Fore, Style
from tqdm import tqdm
import random

# Inicializar colorama para Windows
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_effect(text, delay=0.05, color=Fore.GREEN):
    cursor = '█'
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
        # Efecto de cursor parpadeante
        sys.stdout.write(color + cursor + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.01)
        sys.stdout.write('\b')
    print()

def show_banner():
    colors = [Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    banner = f"""
    {random.choice(colors)}
    ┌─────────────────────────────────────────────────────────────────┐
    │  ██████╗ ███████╗██╗   ██╗████████╗ ██████╗  ██████╗ ██╗      │
    │  ██╔══██╗██╔════╝██║   ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║      │
    │  ██║  ██║█████╗  ██║   ██║   ██║   ██║   ██║██║   ██║██║      │
    │  ██║  ██║██╔══╝  ╚██╗ ██╔╝   ██║   ██║   ██║██║   ██║██║      │
    │  ██████╔╝███████╗ ╚████╔╝    ██║   ╚██████╔╝╚██████╔╝███████╗ │
    │  ╚═════╝ ╚══════╝  ╚═══╝     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ │
    │                                                                 │
    │                 >_ Herramientas de Desarrollo                  │
    │                 >_ powered by DevHarold 🐾                     │
    └─────────────────────────────────────────────────────────────────┘
    """
    print(banner + Style.RESET_ALL)
    print(Fore.CYAN + '\n        [ GITHUB: ' + Fore.GREEN + 'DevCat-HGS' + Fore.CYAN + ' | Version: ' + Fore.GREEN + 'Developer' + Fore.CYAN + ' ]' + Style.RESET_ALL)

def main():
    clear_screen()
    show_banner()
    
    # Preguntar si está listo
    print(Fore.YELLOW + "\n¿Estás listo para comenzar?" + Style.RESET_ALL)
    input(Fore.CYAN + "Presiona Enter para continuar..." + Style.RESET_ALL)
    
    # Mostrar el prompt y ejecutar el comando
    print()
    type_effect('~$ sudo cat /dev/tools', delay=0.03)
    
    # Importar y mostrar el menú de herramientas
    from tools.menu import show_menu
    show_menu()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[*] Saliendo..." + Style.RESET_ALL)
        sys.exit(0)