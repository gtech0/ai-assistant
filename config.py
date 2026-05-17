import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///risk_assistant.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LLAMA_MODEL_PATH = os.getenv('LLAMA_MODEL_PATH')
    LLAMA_N_GPU_LAYERS = int(os.getenv('LLAMA_N_GPU_LAYERS', -1))
    LLAMA_CONTEXT_SIZE = int(os.getenv('LLAMA_CONTEXT_SIZE', 8192))
    LLAMA_MAX_TOKENS = int(os.getenv('LLAMA_MAX_TOKENS', 4096))
    LLAMA_TEMPERATURE_RISKS = float(os.getenv('LLAMA_TEMPERATURE_RISKS', 0.6))
    LLAMA_TEMPERATURE_IDEAS = float(os.getenv('LLAMA_TEMPERATURE_IDEAS', 0.7))
    LLAMA_TOP_P = float(os.getenv('LLAMA_TOP_P', 0.8))
    LLAMA_TOP_K = float(os.getenv('LLAMA_TOP_K', 20))
    LLAMA_REPEAT_PENALTY = float(os.getenv('LLAMA_REPEAT_PENALTY', 1))
