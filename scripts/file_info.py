import argparse
import hashlib
import json
import mimetypes
import os
from datetime import datetime
from pathlib import Path


def human_readable_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def compute_hash(file_path: Path, algorithm: str) -> str:
    hash_func = hashlib.new(algorithm)
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def gather_file_info(file_path: Path, hash_algorithms: list[str]) -> dict:
    stat = file_path.stat()
    mime_type, encoding = mimetypes.guess_type(str(file_path))

    info = {
        "path": str(file_path.resolve()),
        "name": file_path.name,
        "stem": file_path.stem,
        "suffix": file_path.suffix,
        "size_bytes": stat.st_size,
        "size_readable": human_readable_size(stat.st_size),
        "created": format_timestamp(stat.st_ctime),
        "modified": format_timestamp(stat.st_mtime),
        "accessed": format_timestamp(stat.st_atime),
        "mime_type": mime_type or "unknown",
        "encoding": encoding or "none",
    }

    if hash_algorithms:
        info["hashes"] = {algo: compute_hash(file_path, algo) for algo in hash_algorithms}

    return info


def print_info(info: dict, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return

    print(f"File: {info['path']}")
    print(f"Name: {info['name']}")
    print(f"Type: {info['mime_type']} {info['suffix']}")
    print(f"Size: {info['size_readable']} ({info['size_bytes']} bytes)")
    print(f"Created: {info['created']}")
    print(f"Modified: {info['modified']}")
    print(f"Accessed: {info['accessed']}")
    if info.get("hashes"):
        print("Hashes:")
        for algorithm, digest in info["hashes"].items():
            print(f"  {algorithm}: {digest}")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="file_info",
        description="Visa metadata och valfria hash-värden för en fil.",
    )
    parser.add_argument("file", nargs="?", help="Sökväg till filen som ska analyseras")
    parser.add_argument(
        "--hash",
        choices=["md5", "sha1", "sha256", "sha512"],
        action="append",
        help="Beräkna en eller flera hash-värden för filen. Kan anges flera gånger.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Utmatningsformat.",
    )
    args = parser.parse_args()

    file_path = args.file
    if not file_path:
        file_path = input("Ange filväg: ").strip()

    if not file_path:
        print("Ingen fil angiven.")
        return 1

    path = Path(file_path)
    if not path.exists() or not path.is_file():
        print(f"Filen hittades inte eller är inte en vanlig fil: {file_path}")
        return 1

    info = gather_file_info(path, args.hash or [])
    print_info(info, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
