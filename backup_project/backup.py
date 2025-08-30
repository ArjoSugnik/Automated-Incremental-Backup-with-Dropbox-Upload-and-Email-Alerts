import os
import shutil
import datetime
import dropbox
import zipfile
import logging
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Dropbox access token from environment variable
ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Email configuration from environment variables
EMAIL_FROM = os.getenv('EMAIL_USER')
EMAIL_TO = os.getenv('EMAIL_RECIPIENT')  # Set recipient email in .env
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
SMTP_USERNAME = os.getenv('EMAIL_USER')
SMTP_PASSWORD = os.getenv('EMAIL_PASS')

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


def send_email(subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        logging.info('Email alert sent.')
        print('Email alert sent.')
    except Exception as e:
        logging.error(f'Failed to send email alert: {e}')
        print(f'Failed to send email alert: {e}')


def load_last_backup_time(file_path='last_backup.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            timestamp_str = f.read().strip()
            return datetime.datetime.fromisoformat(timestamp_str)
    return None


def save_last_backup_time(time, file_path='last_backup.txt'):
    with open(file_path, 'w') as f:
        f.write(time.isoformat())


def incremental_backup(source_dir, backup_dir):
    last_backup = load_last_backup_time()
    now = datetime.datetime.now()
    timestamp_folder = now.strftime('%Y-%m-%d_%H-%M-%S')
    dest_dir = os.path.join(backup_dir, f'backup_{timestamp_folder}')
    os.makedirs(dest_dir, exist_ok=True)

    files_copied = 0
    for root, _, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        backup_subdir = os.path.join(dest_dir, rel_path)
        os.makedirs(backup_subdir, exist_ok=True)

        for file in files:
            source_file = os.path.join(root, file)
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(source_file))
            if not last_backup or mod_time > last_backup:
                shutil.copy2(source_file, backup_subdir)
                files_copied += 1

    save_last_backup_time(now)
    logging.info(f'Incremental backup done! {files_copied} files copied to {dest_dir}')
    return dest_dir if files_copied > 0 else None


def compress_backup_folder(folder_path):
    zip_path = folder_path + '.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zf.write(full_path, arcname)
    logging.info(f'Compressed backup to {zip_path}')
    return zip_path


def upload_to_dropbox(local_path, dropbox_path):
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    logging.info(f'Uploaded {local_path} to Dropbox at {dropbox_path}')


if __name__ == '__main__':
    try:
        logging.info('Backup process started.')

        source = 'data_to_backup'
        backup_root = 'backups'

        backup_folder = incremental_backup(source, backup_root)
        if backup_folder:
            zip_file = compress_backup_folder(backup_folder)
            upload_to_dropbox(zip_file, '/' + os.path.basename(zip_file))
            logging.info('Backup and upload completed successfully.')
            send_email('Backup Success', f'Backup and upload completed successfully at {datetime.datetime.now()}.')
        else:
            logging.info('No new or changed files to back up.')
            send_email('Backup Skipped', 'No new or changed files detected since last backup.')
    except Exception as e:
        logging.error(f'Backup process failed: {e}')
        send_email('Backup Failed', f'Backup process failed with error: {e}')
