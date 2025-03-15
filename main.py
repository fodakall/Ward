import os
import sys
import subprocess
import keyboard
import shutil  # För att få terminalens bredd
from colorama import Fore, Style, init

# Initiera colorama
init(autoreset=True)

# Hämta den aktuella katalogen där main.py ligger
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dynamiskt sätt att hitta scripts-mappen
SCRIPT_PATH = os.path.join(BASE_DIR, "scripts")

def clear_screen():
    """Rensa terminalen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    """Centrera en text baserat på terminalbredden."""
    width = shutil.get_terminal_size().columns
    return text.center(width)

def banner():
    """Visa en centrerad banner."""
    clear_screen()
    print(Fore.MAGENTA + center_text("────── WARD 1.0 ──────\n"))
    print(Fore.YELLOW + center_text("─" * 50))
    print(Fore.CYAN + center_text("Välj ett alternativ"))
    print(Fore.YELLOW + center_text("─" * 50))
    print("\n")
    print(Fore.GREEN + center_text("[1] ➤ Starta TextFinder"))
    print(Fore.BLUE + center_text("[2] ➤ Starta TextGrabber"))
    print(Fore.RED + center_text("[3] ➤ Avsluta programmet"))
    print("\n")
    print(Fore.YELLOW + center_text("─" * 50))

def visa_huvudmeny():
    """Visa huvudmenyn och låt användaren välja genom att trycka på en knapp."""
    while True:
        banner()
        print("\n" + Fore.WHITE + center_text("Tryck [1], [2] eller [3] för att välja:"))

        while True:
            event = keyboard.read_event(suppress=True)  # Väntar på en tangent och dämpar utskrift
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "1":
                    kör_textfinder()
                    break
                elif event.name == "2":
                    kör_textgrabber()
                    break
                elif event.name == "3":
                    print(Fore.RED + center_text("👋 Avslutar programmet. Hej då!"))
                    sys.exit(0)

def kör_textfinder():
    """Kör TextFinder."""
    script = os.path.join(SCRIPT_PATH, "textfinder.py")
    if os.path.exists(script):
        print("\n" + Fore.GREEN + center_text("🔍 Startar TextFinder..."))
        subprocess.run(["python", script])
    else:
        print(Fore.RED + center_text(f"❌ Hittade inte {script}!"))

    input("\n" + Fore.WHITE + center_text("Tryck på Enter för att återgå till huvudmenyn..."))

def kör_textgrabber():
    """Kör TextGrabber."""
    script = os.path.join(SCRIPT_PATH, "textgrabber.py")
    if os.path.exists(script):
        print("\n" + Fore.BLUE + center_text("📂 Startar TextGrabber..."))
        subprocess.run(["python", script])
    else:
        print(Fore.RED + center_text(f"❌ Hittade inte {script}!"))

    input("\n" + Fore.WHITE + center_text("Tryck på Enter för att återgå till huvudmenyn..."))

if __name__ == "__main__":
    visa_huvudmeny()