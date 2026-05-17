import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "scripts"
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
DEPENDENCY_MODULE_MAP = {
    "Pillow": "PIL",
}


class _NoColor:
    def __getattr__(self, _):
        return ""


try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    Fore = Style = _NoColor()


def clear_screen():
    """Rensa terminalen."""
    os.system("cls" if os.name == "nt" else "clear")


def center_text(text: str) -> str:
    """Centrera en text baserat på terminalbredden."""
    width = shutil.get_terminal_size(fallback=(80, 20)).columns
    return text.center(width)


def load_requirements() -> List[str]:
    """Läs in paket från requirements.txt."""
    if not REQUIREMENTS_FILE.exists():
        return []

    packages: List[str] = []
    with REQUIREMENTS_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            package_name = line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].strip()
            if package_name:
                packages.append(package_name)
    return packages


def get_module_name(package_name: str) -> str:
    return DEPENDENCY_MODULE_MAP.get(package_name, package_name.replace("-", "_"))


def is_package_installed(package_name: str) -> bool:
    module_name = get_module_name(package_name)
    return importlib.util.find_spec(module_name) is not None


def install_packages(packages: List[str]) -> bool:
    command = [sys.executable, "-m", "pip", "install", *packages]
    print(Fore.CYAN + center_text("Installerar saknade Python-paket..."))
    result = subprocess.run(command)
    return result.returncode == 0


def ensure_requirements() -> bool:
    """Kontrollera och installera saknade Python-dependency packages."""
    packages = load_requirements()
    if not packages:
        return True

    missing = [pkg for pkg in packages if not is_package_installed(pkg)]
    if not missing:
        return True

    print(Fore.YELLOW + center_text("Saknade beroenden upptäckta:"))
    print(Fore.YELLOW + "  " + ", ".join(missing))
    answer = input("Vill du installera dem nu? (j/n): ").strip().lower()
    if answer not in ("j", "ja", "y", "yes"):
        print(Fore.RED + center_text("Installationen avbryts."))
        return False

    return install_packages(missing)


def get_powershell_executable() -> Optional[str]:
    for executable in ("pwsh", "powershell.exe"):
        path = shutil.which(executable)
        if path:
            return path
    return None


def discover_scripts() -> List[Dict[str, object]]:
    """Hitta Python- och PowerShell-skript i scripts-mappen."""
    scripts: List[Dict[str, object]] = []
    if not SCRIPTS_DIR.exists():
        return scripts

    for path in sorted(SCRIPTS_DIR.iterdir()):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()
        if suffix not in {".py", ".ps1"}:
            continue

        scripts.append(
            {
                "name": path.stem.lower(),
                "display_name": path.stem,
                "path": path,
                "suffix": suffix,
            }
        )

    return scripts


def print_banner(scripts: List[Dict[str, object]]) -> None:
    clear_screen()
    print(Fore.MAGENTA + center_text("────── WARD 1.3 ──────\n"))
    print(Fore.YELLOW + center_text("─" * 50))
    print(Fore.CYAN + center_text("Välj ett skript att köra"))
    print(Fore.YELLOW + center_text("─" * 50))
    print()

    for index, script in enumerate(scripts, start=1):
        print(Fore.GREEN + center_text(f"[{index}] ➤ {script['display_name']}"))

    print()
    print(Fore.RED + center_text("[q] ➤ Avsluta"))
    print(Fore.YELLOW + center_text("─" * 50))


def select_script(scripts: List[Dict[str, object]], choice: str) -> Optional[Dict[str, object]]:
    choice = choice.strip().lower()
    if not choice:
        return None

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(scripts):
            return scripts[index]

    for script in scripts:
        if script["name"] == choice or script["display_name"].lower() == choice:
            return script

    return None


def run_python_script(script_path: Path) -> int:
    return subprocess.run([sys.executable, str(script_path)], cwd=str(script_path.parent)).returncode


def run_powershell_script(script_path: Path) -> int:
    powershell = get_powershell_executable()
    if not powershell:
        print(Fore.RED + center_text("PowerShell hittades inte på den här datorn."))
        return 1

    command = [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
    return subprocess.run(command, cwd=str(script_path.parent)).returncode


def run_script(script: Dict[str, object]) -> int:
    script_path = script["path"]
    suffix = script["suffix"]

    print()
    print(Fore.CYAN + center_text(f"Kör {script['display_name']}..."))
    print()

    if suffix == ".py":
        return run_python_script(script_path)
    if suffix == ".ps1":
        return run_powershell_script(script_path)

    print(Fore.RED + center_text("Okänt skripttyp."))
    return 1


def interactive_menu(scripts: List[Dict[str, object]]) -> None:
    while True:
        print_banner(scripts)
        print()
        choice = input("Ange nummer eller skriptnamn: ").strip()
        if choice.lower() in {"q", "quit", "exit"}:
            print(Fore.RED + center_text("👋 Avslutar programmet. Hej då!"))
            return

        selected = select_script(scripts, choice)
        if selected is None:
            print(Fore.RED + center_text("Ogiltigt val. Försök igen."))
            input("Tryck Enter för att fortsätta...")
            continue

        code = run_script(selected)
        print()
        print(Fore.YELLOW + center_text(f"Skriptet avslutade med returnkod {code}."))
        input("\nTryck Enter för att återgå till menyn...")


def main() -> int:
    parser = argparse.ArgumentParser(prog="ward", description="Ward skript-launcher")
    parser.add_argument("script", nargs="?", help="Skript att köra (nummer eller namn)")
    parser.add_argument("--list", action="store_true", help="Visa tillgängliga skript")
    parser.add_argument("--install-deps", action="store_true", help="Installera saknade beroenden och avsluta")
    args = parser.parse_args()

    scripts = discover_scripts()
    if not scripts:
        print(Fore.RED + center_text("Ingen scripts-mapp eller inga stödda skript hittades."))
        return 1

    if args.install_deps:
        return 0 if ensure_requirements() else 1

    if args.list:
        for index, script in enumerate(scripts, start=1):
            print(f"[{index}] {script['display_name']} ({script['suffix']})")
        return 0

    if not ensure_requirements():
        return 1

    if args.script:
        selected = select_script(scripts, args.script)
        if selected is None:
            print(Fore.RED + center_text("Skriptet kunde inte hittas. Kontrollera namnet eller numret."))
            return 2

        return run_script(selected)

    interactive_menu(scripts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
