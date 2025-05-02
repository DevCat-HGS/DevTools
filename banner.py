import sys
import time
import os
from colorama import init, Fore, Back, Style
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

def show_initialization():
    type_effect('~$ sudo cat /dev/tools', delay=0.03)
    time.sleep(0.3)
    
    # Barra de progreso de inicialización
    print(Fore.CYAN + '\nInicializando Software...' + Style.RESET_ALL)
    for _ in tqdm(range(100), desc='Progreso', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
        time.sleep(0.01)
    
    print('\n' + Fore.GREEN + '[✓] Software inicializado correctamente' + Style.RESET_ALL)
    type_effect('>_ Software Diseñado con fines Educativos y para uso Etico', delay=0.03, color=Fore.YELLOW)
    time.sleep(0.5)

def show_banner():
    colors = [Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    banner = f"""
    {random.choice(colors)}
    ┌─────────────────────────────────────────────────────────────────┐
    │  ██████╗ ███████╗██╗   ██╗████████╗ ██████╗  ██████╗ ██╗        │
    │  ██╔══██╗██╔════╝██║   ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║        │
    │  ██║  ██║█████╗  ██║   ██║   ██║   ██║   ██║██║   ██║██║        │
    │  ██║  ██║██╔══╝  ╚██╗ ██╔╝   ██║   ██║   ██║██║   ██║██║        │
    │  ██████╔╝███████╗ ╚████╔╝    ██║   ╚██████╔╝╚██████╔╝███████╗   │
    │  ╚═════╝ ╚══════╝  ╚═══╝     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝   │
    │                                                                 │
    │                 >_ Herramientas de Desarrollo                   │
    │                 >_ powered by DevHarold 🐾                     │
    └─────────────────────────────────────────────────────────────────┘
    """
    print(banner + Style.RESET_ALL)
    print(Fore.CYAN + '\n        [ GITHUB: ' + Fore.GREEN + 'DevCat-HGS' + Fore.CYAN + ' | Version: ' + Fore.GREEN + 'Developer' + Fore.CYAN + ' ]' + Style.RESET_ALL)

def main():
    clear_screen()
    show_initialization()
    time.sleep(0.5)
    clear_screen()
    show_banner()
    
    # Importar y mostrar el menú de herramientas
    from tools.menu import show_menu
    show_menu()

if __name__ == '__main__':
    main()