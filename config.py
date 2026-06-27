import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sup3r-s3cr3t-k3y-f0r-f4k3-n3ws'
    
    # Use /tmp for SQLite database if running on Vercel's read-only filesystem
    if os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL'):
        DATABASE_PATH = '/tmp/database.db'
    else:
        DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')
        
    MODEL_PATH = os.path.join(BASE_DIR, 'model', 'model.pkl')
    VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')

    # Basic limits
    MAX_INPUT_LENGTH = 10000 

    # Dynamic Analysis (Experimental)
    # Get your API key from https://aistudio.google.com/
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    ENABLE_DYNAMIC_VERIFICATION = True # Toggle to enable/disable web-searching
    
    # Model Strategy
    PRIMARY_MODEL = 'gemini-1.5-flash'
    FALLBACK_MODEL = 'gemini-1.5-flash-8b'
    MAX_RETRIES = 3 # Number of retries for transient errors
