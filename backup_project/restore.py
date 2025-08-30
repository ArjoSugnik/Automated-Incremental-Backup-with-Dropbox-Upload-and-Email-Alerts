import os
import shutil

backup_dir = 'backups'
restore_dir = 'data_to_backup'

# List backup folders
backups = [f for f in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, f))]
print("Available backups:")
for idx, bkp in enumerate(backups):
    print(f"{idx+1}: {bkp}")

choice = int(input("Enter the number of the backup you want to restore from: ")) - 1
selected_backup = os.path.join(backup_dir, backups[choice])

# List files in selected backup
files = os.listdir(selected_backup)
print("Files in backup:")
for idx, file in enumerate(files):
    print(f"{idx+1}: {file}")
print(f"{len(files)+1}: Restore ALL files")

file_choice = int(input("Enter number of the file to restore (or choose 'Restore ALL files'): "))

if file_choice == len(files)+1:
    # Restore all files
    for file in files:
        shutil.copy2(os.path.join(selected_backup, file), restore_dir)
    print("All files restored!")
else:
    # Restore selected file
    shutil.copy2(os.path.join(selected_backup, files[file_choice-1]), restore_dir)
    print(f"{files[file_choice-1]} restored!")
