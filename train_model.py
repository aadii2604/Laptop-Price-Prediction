"""Run locally to compare models:  python train_model.py"""
from model_utils import train

model, metrics, df = train()
print(f"Rows: {len(df)}")
print(metrics.to_string(index=False))
