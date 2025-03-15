import argparse
import os
import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract

# Ange sökvägen till tesseract om den inte finns i systemets PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Justera detta efter din installation

# Class for textgrabber
class textgrabber:
    def __init__(self):
        # Skapa en parser för att hantera argumenten
        self.parser = argparse.ArgumentParser(
            prog="textgrabber",
            description="CLI verktyg för att extrahera text från bilder",
        )

        # Lägg till argument i parsern
        self.parser.add_argument("bildfil", nargs="?", help="Bildfilen att extrahera text från")
        self.parser.add_argument("--output", "-o", help="Spara den extraherade texten till en fil")

        # Läs in argumenten
        self.args = self.parser.parse_args()

        # Om ingen bildfil är angiven, öppna en filväljardialog
        if not self.args.bildfil:
            self.args.bildfil = self.open_file_dialog()

    def open_file_dialog(self):
        """Öppna en filväljardialog och låt användaren välja en bildfil."""
        root = tk.Tk()
        root.withdraw()  # Dölj huvudfönstret
        file_path = filedialog.askopenfilename(
            title="Välj en bildfil",
            filetypes=[("Bilder", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])  # Filtyper för bilder
        return file_path

    def extract_text_from_image(self, bildfil):
        """Extrahera text från en bildfil med hjälp av pytesseract."""
        try:
            # Öppna bilden med Pillow
            image = Image.open(bildfil)

            # Använd pytesseract för att extrahera text från bilden
            extracted_text = pytesseract.image_to_string(image)
            return extracted_text
        except Exception as e:
            print(f"Fel vid extraktion av text från bilden: {e}")
            sys.exit(1)

    def save_text_to_file(self, text, output_path):
        """Spara den extraherade texten till en textfil."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Texten har sparats i filen: {output_path}")
        except Exception as e:
            print(f"Fel vid sparande av fil: {e}")
            sys.exit(1)

    def run(self):
        if not self.args.bildfil:
            print("Ingen bildfil vald.")
            sys.exit(1)

        print(f"Vald bildfil: {self.args.bildfil}")

        # Extrahera text från bilden
        extracted_text = self.extract_text_from_image(self.args.bildfil)

        # Fråga användaren om de vill skriva ut i terminalen eller spara till fil
        print("\nVill du:")
        print("1. Skriva ut texten i terminalen")
        print("2. Spara texten till en fil")

        choice = input("Välj ett alternativ (1 eller 2): ")

        if choice == '1':
            # Om användaren väljer 1, skriv ut texten i terminalen
            print("\nExtraherad text:")
            print(extracted_text)
        elif choice == '2':
            # Om användaren väljer 2, fråga efter filnamn och spara texten i en fil
            output_path = input("Ange filnamn för att spara texten (t.ex. resultat.txt): ")
            self.save_text_to_file(extracted_text, output_path)
        else:
            print("Ogiltigt val! Programmet avslutas.")
            sys.exit(1)

# Skapa en instans av textgrabber-klassen och kör den
if __name__ == "__main__":
    textgrabber = textgrabber()  # Skapa instansen
    textgrabber.run()  # Kör programmet