# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

INPUT_FOLDER = os.getenv("INPUT_FOLDER")
if not INPUT_FOLDER:
    raise ValueError("Missing INPUT_FOLDER. Set it in .env")