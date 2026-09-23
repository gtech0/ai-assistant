import os
import sys
from dotenv import load_dotenv

if hasattr(sys, '_MEIPASS'):
    APP_ROOT = os.path.dirname(sys.executable)
    INTERNAL_DIR = sys._MEIPASS
else:
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    INTERNAL_DIR = APP_ROOT

load_dotenv(os.path.join(APP_ROOT, '.env'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///risk_assistant.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    INTERNAL_DIR = INTERNAL_DIR
    APP_ROOT = APP_ROOT

    raw_model_path = os.getenv('MODEL_PATH', 'Qwen3-4B-Instruct-2507-UD-Q4_K_XL.gguf')
    MODEL_PATH = os.path.join(APP_ROOT, raw_model_path.lstrip('./'))

    N_GPU_LAYERS = int(os.getenv('N_GPU_LAYERS', -1))
    CONTEXT_SIZE = int(os.getenv('CONTEXT_SIZE', 8192))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4096))
    TEMPERATURE_RISKS = float(os.getenv('TEMPERATURE_RISKS', 0.6))
    TEMPERATURE_IDEAS = float(os.getenv('TEMPERATURE_IDEAS', 0.7))
    TOP_P = float(os.getenv('TOP_P', 0.8))
    TOP_K = int(os.getenv('TOP_K', 20))
    REPEAT_PENALTY = float(os.getenv('REPEAT_PENALTY', 1.0))