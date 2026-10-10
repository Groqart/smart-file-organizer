#!/usr/bin/env python3
"""
Smart File Organizer CLI Tool
A lightweight Python script that automatically organizes messy directories
(like Downloads or Desktop) into clean categorized folders.
"""

import os
import shutil
from pathlib import Path

# Define category mappings
EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx", ".md"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".sql", ".sh"],
    "Media": [".mp4", ".mkv", ".avi", ".mov", ".mp3", ".wav"],
    "Executables": [".exe", ".dmg", ".pkg", ".deb", ".AppImage"]
}

def organize_directory(target_path: str, dry_run: bool = False):
    target = Path(target_path).resolve()
    if not target.exists():
        print(f"Error: Path '{target}' does not exist.")
        return

    print(f"Organizing directory: {target}")
    if dry_run:
        print("--- DRY RUN MODE (No files will be moved) ---")

    moved_count = 0

    for item in target.iterdir():
        if item.is_dir() or item.name.startswith('.'):
            continue  # Skip directories and hidden files

        ext = item.suffix.lower()
        category = "Others"

        for cat, exts in EXTENSIONS.items():
            if ext in exts:
                category = cat
                break

        dest_dir = target / category
        dest_file = dest_dir / item.name

        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            # Handle name collisions
            counter = 1
            while dest_file.exists():
                stem = item.stem
                dest_file = dest_dir / f"{stem}_{counter}{ext}"
                counter += 1
            shutil.move(str(item), str(dest_file))
        
        print(f"[{category}] {item.name} -> {dest_file.relative_to(target)}")
        moved_count += 1

    print(f"\nDone! Organized {moved_count} files.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean up and organize messy directories by file type.")
    parser.add_argument("path", nargs="?", default=".", help="Path to the directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    
    args = parser.parse_args()
    organize_directory(args.path, dry_run=args.dry_run)
