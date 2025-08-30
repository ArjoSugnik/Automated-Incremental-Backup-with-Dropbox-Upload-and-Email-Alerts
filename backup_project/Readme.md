Automated Incremental Backup with Dropbox Upload and Email Alerts
Overview
This project is a Python-based backup solution that performs incremental backups of your local data folder, compresses the backup into a zip file, uploads the backup to Dropbox cloud storage, and sends email alerts for success, skipped backup, or failure. It includes:

Incremental backup logic (only new or changed files are backed up)

Dropbox API integration for file upload with scoped access

Email notification using Gmail SMTP and secure app passwords

Logging of backup operations and errors

Features
Incremental backups save storage and time

Secure Dropbox upload with scoped tokens

Email alerts on backup success/failure

Configurable via .env environment variables

Logs all activities and errors to a log file

Prerequisites
Python 3.7+

Dropbox account with an app created (with correct permissions)

Gmail account with 2FA enabled and generated app password for SMTP

Installed Python packages:

bash
pip install dropbox python-dotenv
Configuration
Create a .env file in the project root directory with the following variables:

text
DROPBOX_ACCESS_TOKEN=your_dropbox_access_token
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASS=your_gmail_app_password
EMAIL_RECIPIENT=recipient_email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
Make sure:

DROPBOX_ACCESS_TOKEN has scopes including files.content.write

EMAIL_PASS is a Gmail app password, not your Gmail login password

Usage
Run the backup script using:

bash
python backup.py
The script will:

Create an incremental backup of the specified source directory (data_to_backup)

Compress the backup folder into a zip file

Upload the zip file to your Dropbox app folder

Send email alerts about backup status

Log all activities and errors to backup.log

Important Notes Before Uploading to GitHub
Do NOT commit your .env file or any file containing sensitive credentials (like access tokens, email passwords). Add .env to your .gitignore.

Review your code to ensure no sensitive keys or passwords are hardcoded.

Ensure all credentials are loaded securely from environment variables.

Optionally, provide a sample .env.example file with placeholder values (no real credentials).

Write clear commit messages describing changes and functionality.