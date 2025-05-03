import sys
import time
import os
from colorama import init, Fore, Style
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

def show_warning():
    colors = [Fore.YELLOW]
    warning = f"""
    {random.choice(colors)}
    ┌─────────────────────────────────────────────────────────────────┐
    │                    ¡ADVERTENCIA IMPORTANTE!                     │
    │                                                                 │
    │    Este software debe de ser usado con suma precaucion          │
    │    Versión: Developer                                           │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
    """
    print(warning + Style.RESET_ALL)

def main():
    clear_screen()
    show_warning()
    
    # Preguntar si está listo
    print(Fore.BLUE + "\n¿Estás listo para comenzar?" + Style.RESET_ALL)
    input(Fore.CYAN + "Presiona Enter para continuar..." + Style.RESET_ALL)
    
    # Transferir control a banner.py
    import banner
    banner.main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[*] Saliendo..." + Style.RESET_ALL)
        sys.exit(0)