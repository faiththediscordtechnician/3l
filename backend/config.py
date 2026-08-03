import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/3l_hub")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
CANLII_API_KEY = os.getenv("CANLII_API_KEY", "")
