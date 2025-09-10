import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
USE_SQLITE = os.getenv("USE_SQLITE", "1") == "1"
