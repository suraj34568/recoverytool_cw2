# recovery_cli.py

import os
import shutil

def scan_files(scan_dir):
    found_files = []
    if not os.path.isdir(scan_dir):
        print("❌ Invalid scan directory.")
        return found_files

    print(f"🔍 Scanning '{scan_dir}' for .deleted and .txt files...\n")
    for root, dirs, files in os.walk(scan_dir):
        for file in files:
            if file.endswith(".deleted") or file.endswith(".txt"):
                full_path = os.path.join(root, file)
                found_files.append(full_path)

    if not found_files:
        print("✅ Scan complete. No matching files found.")
    else:
        print(f"✅ Scan complete. {len(found_files)} files found:\n")
        for idx, file in enumerate(found_files, 1):
            print(f"{idx}. {file}")

    return found_files

def recover_files(files, selected_indices, recover_dir):
    if not os.path.isdir(recover_dir):
        print("❌ Invalid recovery destination.")
        return

    count = 0
    for i in selected_indices:
        try:
            file_path = files[i]
            filename = os.path.basename(file_path)
            dest_path = os.path.join(recover_dir, filename)
            shutil.copy2(file_path, dest_path)
            count += 1
        except Exception as e:
            print(f"❌ Failed to recover {file_path}: {e}")

    print(f"\n✅ Recovery complete. {count} file(s) recovered.")

def main():
    print("=== Simple File Recovery Tool (CLI Version) ===\n")

    scan_dir = input("📁 Enter the folder path to scan: ").strip()
    found_files = scan_files(scan_dir)

    if not found_files:
        return

    print("\n📌 Enter the file numbers to recover (comma-separated):")
    try:
        choices = input("➤ ").strip()
        selected = [int(i) - 1 for i in choices.split(",") if i.strip().isdigit()]
        selected = [i for i in selected if 0 <= i < len(found_files)]
    except Exception:
        print("❌ Invalid input. Exiting.")
        return

    if not selected:
        print("⚠️ No valid files selected. Exiting.")
        return

    recover_dir = input("\n💾 Enter the recovery destination folder: ").strip()
    recover_files(found_files, selected, recover_dir)

if __name__ == "__main__":
    main()
