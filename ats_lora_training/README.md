# ATS LoRA Fine-tuning & RAG Training System

This folder contains everything needed to fine-tune a small quantized language model using LoRA (Low-Rank Adaptation) for your ATS use case, with human feedback integration and semantic understanding.

## Overview

This system allows you to:
1. Collect user feedback on model responses (correct/incorrect points)
2. Build a feedback database with semantic embeddings
3. Create a RAG (Retrieval Augmented Generation) system
4. Fine-tune a quantized model using LoRA with the collected feedback

## Prerequisites

```bash
pip install -r requirements.txt
```

Required packages:
- transformers
- peft
- bitsandbytes
- torch
- sentence-transformers
- langchain
- faiss-cpu (or faiss-gpu)
- datasets
- accelerate
- trl

## Project Structure

```
ats_lora_training/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── feedback_collector.py              # Collect user feedback
├── database_builder.py                # Build training database
├── rag_builder.py                     # Build RAG system
├── lora_trainer.py                    # LoRA fine-tuning script
├── evaluate_model.py                  # Evaluate trained model
├── config.py                          # Configuration settings
├── feedback_db/                       # Feedback storage
│   ├── interactions.jsonl            # Raw interactions
│   ├── embeddings/                   # Vector embeddings
│   └── training_pairs/               # Processed training data
├── vector_store/                      # RAG vector database
├── models/                            # Trained model checkpoints
└── data/                              # ATS knowledge base documents
```

## Workflow

### Phase 1: Feedback Collection (Week 1-2)

Run the feedback collector alongside your ATS system:

```python
from feedback_collector import FeedbackCollector

collector = FeedbackCollector(db_path="feedback_db")

# After each model response
feedback = collector.collect_feedback(
    query="Analyze this resume for Software Engineer role",
    context=["retrieved context chunks"],
    response="Model's response here"
)
```

**Goal**: Collect 100-200 feedback samples with:
- User ratings (1-5)
- Correct points identified
- Incorrect points identified
- Ideal/corrected responses

### Phase 2: Database Building (Week 3)

Process collected feedback into training data:

```bash
python database_builder.py --input feedback_db/interactions.jsonl --output feedback_db/training_pairs
```

This creates:
- Positive examples (high-rated responses)
- Negative examples with corrections
- Semantic embeddings for all text
- Training/validation split

### Phase 3: RAG System (Week 3)

Build vector store from your ATS knowledge base:

```bash
python rag_builder.py --docs data/ats_docs --output vector_store
```

### Phase 4: LoRA Training (Week 4)

Fine-tune the model with collected feedback:

```bash
python lora_trainer.py \
    --base_model mistralai/Mistral-7B-v0.1 \
    --training_data feedback_db/training_pairs \
    --output_dir models/ats_lora_v1 \
    --epochs 3 \
    --batch_size 4
```

### Phase 5: Evaluation & Iteration (Week 5+)

Evaluate the trained model:

```bash
python evaluate_model.py --model models/ats_lora_v1 --test_data feedback_db/test_set.jsonl
```

Deploy, collect more feedback, and retrain iteratively.

## Configuration

Edit `config.py` to customize:

```python
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

# RAG settings
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
TOP_K_RETRIEVAL = 5
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Feedback settings
MIN_FEEDBACK_SAMPLES = 100
SEMANTIC_SIMILARITY_THRESHOLD = 0.75
```

## Integration with ATS Backend

To integrate feedback collection with your existing ATS backend (`ats_web/backend/main.py`):

1. Add feedback endpoint:
```python
from feedback_collector import FeedbackCollector

feedback_collector = FeedbackCollector(db_path="../ats_lora_training/feedback_db")

@app.post("/api/feedback")
async def submit_feedback(
    interaction_id: str,
    rating: int,
    correct_points: List[str],
    incorrect_points: List[str],
    ideal_response: str
):
    feedback = feedback_collector.save_feedback(
        interaction_id=interaction_id,
        rating=rating,
        correct_points=correct_points,
        incorrect_points=incorrect_points,
        ideal_response=ideal_response
    )
    return {"status": "success", "feedback_id": feedback["id"]}
```

2. Track interactions in your existing endpoints (e.g., `analyze_resume`, `ask_question`)

3. Add feedback UI component to frontend

## Key Features

### 1. Semantic Understanding
- Uses sentence-transformers to capture meaning, not just text matching
- Tracks semantic drift between model output and ideal responses
- Cosine similarity scoring for contextual alignment

### 2. Human-in-the-Loop
- User identifies correct/incorrect points in responses
- Provides ideal/corrected responses
- Ratings guide training data quality

### 3. Efficient Training
- 4-bit quantization reduces memory requirements
- LoRA adapters are small (~10-50MB vs full model GB)
- Can train on consumer GPUs (RTX 3060 12GB+)

### 4. Iterative Improvement
- Continuous feedback collection
- Periodic retraining with new data
- A/B testing between model versions

## Hardware Requirements

**Minimum** (for 7B model with 4-bit quantization):
- GPU: 12GB VRAM (RTX 3060, RTX 4060 Ti)
- RAM: 16GB
- Storage: 50GB

**Recommended**:
- GPU: 24GB VRAM (RTX 3090, RTX 4090, A5000)
- RAM: 32GB
- Storage: 100GB

**CPU-only** (slower but possible):
- RAM: 32GB+
- Expect 10-20x slower training

## Training Time Estimates

With RTX 3090 (24GB):
- 100 samples: ~30 minutes
- 500 samples: ~2 hours
- 1000 samples: ~4 hours

With RTX 3060 (12GB):
- 100 samples: ~1 hour
- 500 samples: ~4 hours
- 1000 samples: ~8 hours

## Troubleshooting

### Out of Memory (OOM)
- Reduce `BATCH_SIZE` to 1 or 2
- Reduce `LORA_R` to 8
- Use gradient checkpointing
- Switch to smaller base model (3B or 1B)

### Poor Model Performance
- Collect more diverse feedback samples
- Increase training epochs
- Adjust learning rate
- Check data quality in feedback_db

### Slow Training
- Enable gradient accumulation
- Use mixed precision (fp16)
- Reduce sequence length
- Use faster GPU or cloud instance

## Cloud Training Options

If local GPU is insufficient:

**Google Colab Pro** ($10/month):
- T4 GPU (16GB) - suitable for 7B models
- Easy setup with notebooks

**RunPod** (~$0.30/hour):
- RTX 3090, A5000, A6000 options
- Pay per use

**Lambda Labs** (~$0.50/hour):
- A100 GPUs for faster training
- Good for production

## Next Steps

1. **Now**: Set up feedback collection in your ATS frontend
2. **Week 1-2**: Collect initial feedback samples (target: 100+)
3. **Week 3**: Build RAG system and process feedback data
4. **Week 4**: First training run
5. **Week 5+**: Deploy, evaluate, iterate

## Questions?

When you're ready to start implementation, we'll:
1. Set up the feedback collection UI in your React frontend
2. Add feedback endpoints to your FastAPI backend
3. Build the database schema
4. Configure the training pipeline
5. Run the first training iteration

This is a complete system for continuous model improvement based on real user feedback!
