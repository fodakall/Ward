import argparse
import os
import sys


# Class for textfinder
class textfinder:
    def __init__(self):
        # Skapa en parser för att hantera argumenten
        self.parser = argparse.ArgumentParser(
            prog="textfinder",
            description="CLI verktyg för att söka i filer",
        )

        # Lägg till argument i parsern
        self.parser.add_argument("filnamn", nargs="*", help="En eller flera filer att söka i")
        self.parser.add_argument("--search", action="append", help="För att ange söksträngar (kan anges flera gånger)")
        self.parser.add_argument("-n", "--line-number", action="store_true", help="Visa radnummer i resultatet")
        self.parser.add_argument("-i", "--invert-match", action="store_true",
                                 help="Visa rader som inte matchar söksträngen")
        self.parser.add_argument("-q", "--quiet", action="store_true", help="Tysta utskriften men behålla exit-koden")

        # Läs in argumenten
        self.args = self.parser.parse_args()

        # Om inga filnamn är angivna, fråga användaren
        if not self.args.filnamn:
            self.args.filnamn = input("Ange filnamn (separera med mellanslag om flera): ").split()

        # Om inga söksträngar är angivna, fråga användaren
        if not self.args.search:
            self.args.search = input("Ange söksträng (separera med mellanslag om flera): ").split()

        # Fråga om extra argument
        self.ask_optional_arguments()

    def ask_optional_arguments(self):
        """Fråga användaren om extra argument."""
        # Fråga om line-number argument
        if input("Vill du visa radnummer? (j/n): ").lower() == "j":
            self.args.line_number = True

        # Fråga om invert-match argument
        if input("Vill du invertera matchningen? (j/n): ").lower() == "j":
            self.args.invert_match = True

        # Fråga om quiet argument
        if input("Vill du tysta utskriften? (j/n): ").lower() == "j":
            self.args.quiet = True

    # Hantera filöppning och bearbetning
    def open_file(self, path):
        träffar = 0  # Räkna träffarna i denna fil

        try:
            with open(path, mode="r") as file:
                for raden, innehållet in enumerate(file, start=1):
                    # Kontrollera om raden matchar någon söksträng
                    matchar = False
                    if self.args.search:
                        for söksträng in self.args.search:
                            if söksträng in innehållet:
                                matchar = True
                                break

                    # Invertera matchningen om flaggan -i är satt
                    if self.args.invert_match:
                        matchar = not matchar

                    # Om vi har en match och inte är i tyst läge, skriv ut resultatet
                    if matchar:
                        träffar += 1  # Räkna träffen

                        if not self.args.quiet:  # Tysta läget ska inte skriva ut
                            if self.args.line_number:
                                print(f"{path}:{raden}:{innehållet.strip()}")
                            else:
                                print(f"{path}: {innehållet.strip()}")

        except FileNotFoundError:
            print(f"Kunde inte hitta filen: {path}")
        except PermissionError:
            print(f"Åtkomst nekad: {path}")
        except Exception as e:
            print(f"Ett fel uppstod: {e}")

        return träffar

    # Kör textfinder genom att iterera över alla filer
    def run(self):
        träffar_för_alla_filer = 0  # Totalt antal träffar i alla filer

        # Gå igenom varje fil som angetts
        for fil in self.args.filnamn:
            träffar_för_alla_filer += self.open_file(fil)

        # Om vi har några träffar, sätt exit-koden till 0, annars 1
        if träffar_för_alla_filer > 0:
            sys.exit(0)  # Lyckad körning
        else:
            sys.exit(1)  # Ingen träff hittades


# Skapa en instans av textfinder-klassen och kör den
if __name__ == "__main__":
    textfinder = textfinder()  # Skapa instansen
    textfinder.run()  # Kör programmet