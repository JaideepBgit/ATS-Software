"""Configuration settings for LoRA training and RAG system"""

# Model settings
BASE_MODEL = "mistralai/Mistral-7B-v0.1"  # or "meta-llama/Llama-2-7b-hf"
QUANTIZATION = "4bit"  # 4bit or 8bit

# LoRA settings
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
TARGET_MODULES = ["q_proj", "v_proj", "k_proj", "o_proj"]

# Training settings
LEARNING_RATE = 2e-4
BATCH_SIZE = 4
GRADIENT_ACCUMULATION_STEPS = 4
MAX_STEPS = 1000
WARMUP_STEPS = 100
SAVE_STEPS = 100
EVAL_STEPS = 50
MAX_SEQ_LENGTH = 2048

# RAG settings
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
TOP_K_RETRIEVAL = 5
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Feedback settings
MIN_FEEDBACK_SAMPLES = 100
SEMANTIC_SIMILARITY_THRESHOLD = 0.75

# Paths
FEEDBACK_DB_PATH = "feedback_db"
VECTOR_STORE_PATH = "vector_store"
MODELS_PATH = "models"
DATA_PATH = "data"
