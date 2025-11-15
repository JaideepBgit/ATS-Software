"""LoRA fine-tuning script"""

import json
import argparse
import torch
from pathlib import Path
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
from config import *

class LoRATrainer:
    def __init__(
        self,
        base_model: str,
        training_data_path: str,
        output_dir: str,
        epochs: int = 3,
        batch_size: int = 4
    ):
        self.base_model = base_model
        self.training_data_path = Path(training_data_path)
        self.output_dir = Path(output_dir)
        self.epochs = epochs
        self.batch_size = batch_size
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_training_data(self):
        """Load training data from JSONL"""
        train_file = self.training_data_path / "train.jsonl"
        val_file = self.training_data_path / "val.jsonl"
        
        train_data = []
        with open(train_file, "r", encoding="utf-8") as f:
            for line in f:
                train_data.append(json.loads(line))
        
        val_data = []
        if val_file.exists():
            with open(val_file, "r", encoding="utf-8") as f:
                for line in f:
                    val_data.append(json.loads(line))
        
        return Dataset.from_list(train_data), Dataset.from_list(val_data) if val_data else None
    
    def format_prompt(self, example):
        """Format example into prompt"""
        prompt = f"""### Instruction:
{example['instruction']}

### Context:
{example['context']}

### Response:
{example['response']}"""
        return {"text": prompt}
    
    def setup_model_and_tokenizer(self):
        """Setup quantized model with LoRA"""
        print(f"Loading base model: {self.base_model}")
        
        # Quantization config
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True if QUANTIZATION == "4bit" else False,
            load_in_8bit=True if QUANTIZATION == "8bit" else False,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.base_model, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        
        # Prepare for training
        model = prepare_model_for_kbit_training(model)
        
        # LoRA config
        lora_config = LoraConfig(
            r=LORA_R,
            lora_alpha=LORA_ALPHA,
            target_modules=TARGET_MODULES,
            lora_dropout=LORA_DROPOUT,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
        
        return model, tokenizer
    
    def train(self):
        """Main training loop"""
        print("Loading training data...")
        train_dataset, val_dataset = self.load_training_data()
        print(f"Train samples: {len(train_dataset)}")
        if val_dataset:
            print(f"Validation samples: {len(val_dataset)}")
        
        # Format datasets
        train_dataset = train_dataset.map(self.format_prompt)
        if val_dataset:
            val_dataset = val_dataset.map(self.format_prompt)
        
        # Setup model
        model, tokenizer = self.setup_model_and_tokenizer()
        
        # Tokenize
        def tokenize_function(examples):
            return tokenizer(
                examples["text"],
                truncation=True,
                max_length=MAX_SEQ_LENGTH,
                padding="max_length"
            )
        
        train_dataset = train_dataset.map(tokenize_function, batched=True)
        if val_dataset:
            val_dataset = val_dataset.map(tokenize_function, batched=True)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=self.epochs,
            per_device_train_batch_size=self.batch_size,
            gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
            learning_rate=LEARNING_RATE,
            warmup_steps=WARMUP_STEPS,
            logging_steps=10,
            save_steps=SAVE_STEPS,
            eval_steps=EVAL_STEPS if val_dataset else None,
            evaluation_strategy="steps" if val_dataset else "no",
            save_total_limit=3,
            fp16=True,
            optim="paged_adamw_8bit",
            report_to="none"
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset
        )
        
        print("\nStarting training...")
        trainer.train()
        
        print(f"\n✓ Training complete! Model saved to {self.output_dir}")
        
        # Save final model
        model.save_pretrained(str(self.output_dir / "final"))
        tokenizer.save_pretrained(str(self.output_dir / "final"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoRA fine-tuning")
    parser.add_argument("--base_model", default=BASE_MODEL, help="Base model name")
    parser.add_argument("--training_data", default="feedback_db/training_pairs", help="Training data directory")
    parser.add_argument("--output_dir", default="models/ats_lora_v1", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size")
    
    args = parser.parse_args()
    
    trainer = LoRATrainer(
        base_model=args.base_model,
        training_data_path=args.training_data,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size
    )
    
    trainer.train()
