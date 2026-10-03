"""API locale de prédiction pour le modèle Military-NER-TASS."""
from pathlib import Path
import os
import sys
import time

DEVELOPMENT_DIR = Path(__file__).resolve().parents[1] / "02_Code_Developpement"
sys.path.insert(0, str(DEVELOPMENT_DIR))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from predict import load_model, predict_entities

app = FastAPI(title="Military-NER-TASS API", version="1.0.0")
START_TIME = time.time()

class PredictionRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    try:
        load_model()
        return {"status": "ok", "model_loaded": True}
    except Exception as error:
        return {"status": "error", "model_loaded": False, "error": str(error)}

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        entities = predict_entities(request.text)
        return {"entities": entities, "entity_count": len(entities)}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@app.get("/metrics")
def metrics():
    return {"uptime_seconds": round(time.time() - START_TIME, 2), "service": "military-ner-tass"}
