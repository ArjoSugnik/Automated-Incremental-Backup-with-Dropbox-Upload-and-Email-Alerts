from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_FROM = os.getenv('EMAIL_USER')
SMTP_USERNAME = os.getenv('EMAIL_USER')
SMTP_PASSWORD = os.getenv('EMAIL_PASS')
