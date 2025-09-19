import os
import re
import time
import argparse

def add_self_include(filepath, file):

    # Read file content
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.readlines()

    include_line = f'#include "{file}"\n'

    # Skip if the include is already there
    if any(line.strip() == include_line.strip() for line in content):
        return
    else:
        # Prepend the include line
        new_content = [include_line] + content

        # Write back
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_content)

def main():
    parser = argparse.ArgumentParser(description="Add #include to code files in sources")
    parser.add_argument("--sources", required=True, help="Path to the skia directory")
    args = parser.parse_args()

    abs_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(abs_path)
    print(f"Root: {root_dir}")
    symbols_file = os.path.normpath(os.path.join(root_dir, "..", "change_symbols", "change_symbols.h"))
    print(f"Symbols: {symbols_file}")

    # Collect files
    files_to_process = []
    for root, _, files in os.walk(args.sources):
        for file in files:
            if file.endswith((".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hh", ".hxx", ".mm")):
                files_to_process.append(os.path.join(root, file))

    previous_progress = None
    total_files = len(files_to_process)
    for idx, file in enumerate(files_to_process):
        progress = round((idx / total_files) * 100)
        if progress != previous_progress:
            print(f"{idx}/{total_files} ({progress:.0f}%)")
            previous_progress = progress
        add_self_include(file, symbols_file)

if __name__ == "__main__":
    main()