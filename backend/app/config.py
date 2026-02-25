import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---- Groq LLM Settings ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

# ---- HuggingFace Image Settings ----
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = os.getenv(
    "HUGGINGFACE_MODEL",
    "stabilityai/stable-diffusion-xl-base-1.0"
)

# ---- MongoDB Settings ----
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "narrative_engine")

# ---- App Settings ----
MAX_TURNS = int(os.getenv("MAX_TURNS", 10))
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "defaultsecretkey")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# ---- Validate Critical Keys ----
def validate_config():
    missing = []

    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not HUGGINGFACE_API_KEY:
        missing.append("HUGGINGFACE_API_KEY")
    if not MONGODB_URI:
        missing.append("MONGODB_URI")

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    print("✅ All configurations loaded successfully!")
    print(f"   → LLM Model     : {GROQ_MODEL}")
    print(f"   → Image Model   : {HUGGINGFACE_MODEL}")
    print(f"   → Database      : {MONGODB_DB_NAME}")
    print(f"   → Max Turns     : {MAX_TURNS}")

# Run validation when this file is loaded
validate_config()