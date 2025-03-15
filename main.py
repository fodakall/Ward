import os
import sys
import time
import subprocess
from colorama import Fore, Style, init


# Initiera colorama
init(autoreset=True)


SCRIPT_PATH = r"C:\Users\fadiw\Ward\scripts"

def clear_screen():
    """Rensa terminalen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """Visa en statisk banner med en färg."""
    font = fr"""{Fore.MAGENTA}
           .---.                                          ,---,       ,----..    
          /. ./|                        ,---,          ,`--.' |      /   /   \   
      .--'.  ' ;             __  ,-.  ,---.'|         /    /  :     /   .     :  
     /__./ \ : |           ,' ,'/ /|  |   | :        :    |.' '    .   /   ;.  \ 
 .--'.  '   ' .  ,--.--.  '  | |' |  |   | |        `----':  |   .   ;   /  ` ; 
/___/ \ |    ' ' /       \\ |  |   ,',--.__| |           '   ' ;   ;   |  ; \ ; | 
;   \  \;      :.--.  .-. |'  :  / /   ,'   |           |   | |   |   :  | ; | ' 
 \   ;  `      | \__\/: . .|  | ' .   '  /  |           '   : ;   .   |  ' ' ' : 
  .   \    .\  ; ," .--.; |;  : | '   ; |:  |           |   | '   '   ;  \; /  | 
   \   \   ' \ |/  /  ,.  ||  , ; |   | '/  '           '   : | ___\   \  ',  /  
    :   '  |--";  :   .'   \---'  |   :    :|           ;   |.'/  .\;   :    /   
     \   \ ;   |  ,     .-./       \   \  /             '---'  \_ ; |\   \ .'    
      '---"     `--`---'            `----'                     /  ,"  `---`      
                                                              '--'               
    {Fore.CYAN}"""

    # Visa bannern och vänta tills användaren trycker på en tangent innan vi fortsätter
    print(font)

def visa_huvudmeny():
    """Visa huvudmenyn."""
    while True:
        # Visa huvudmeny efter bannern utan att rensa skärmen
        print("\n🎯 Välkommen till CLI-huvudmenyn 🎯")
        print("1. Starta TextFinder (söka text i filer)")
        print("2. Starta TextGrabber (extrahera eller manipulera text från bilder)")
        print("3. Avsluta programmet")

        val = input("\nVälj ett alternativ (1-3): ")

        if val == "1":
            kör_textfinder()
        elif val == "2":
            kör_textgrabber()
        elif val == "3":
            print("👋 Avslutar programmet. Hej då!")
            sys.exit(0)
        else:
            print("❌ Ogiltigt val. Försök igen.")

def kör_textfinder():
    """Kör TextFinder."""
    try:
        print("\n🔍 Startar TextFinder...")
        subprocess.run(["python", os.path.join(SCRIPT_PATH, "textfinder.py")])
    except KeyboardInterrupt:
        print("\n🚪 Återvänder till huvudmenyn...")
    input("\nTryck på Enter för att återgå till huvudmenyn...")

def kör_textgrabber():
    """Kör TextGrabber."""
    try:
        print("\n📂 Startar TextGrabber...")
        subprocess.run(["python", os.path.join(SCRIPT_PATH, "textgrabber.py")])
    except KeyboardInterrupt:
        print("\n🚪 Återvänder till huvudmenyn...")
    input("\nTryck på Enter för att återgå till huvudmenyn...")

if __name__ == "__main__":
    banner()  # Visa den statiska bannern med en färg
    visa_huvudmeny()  # Ladda huvudmenyn