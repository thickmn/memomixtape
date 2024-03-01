import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = '' #  Discord App Token 
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URL = 'http://localhost:8080/'
OAUTH_URL = f'' # Generated URL
CLIENT_ID = os.environ.get('CLIENT_ID')
DESCOPE_ID = os.environ.get('DESCOPE_PROJECT_ID')