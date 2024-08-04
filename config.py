import os
from dotenv import load_dotenv

load_dotenv()

DG_API_KEY = os.environ.get("DG_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
