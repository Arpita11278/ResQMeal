import os
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

MYSQL_HOST = os.environ.get("MYSQL_HOST", "b2nefrhzgt6s5ik2rufs-mysql.services.clever-cloud.com")
MYSQL_USER = os.environ.get("MYSQL_USER", "u90mrcwewzpcp7wq")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "0oHIIMEfeUMH0w8V6jOg")
MYSQL_DB = os.environ.get("MYSQL_DB", "b2nefrhzgt6s5ik2rufs")
