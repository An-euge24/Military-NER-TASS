from pathlib import Path
import sys

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

from predict import predict_entities

def test_prediction_returns_list():
    result = predict_entities("Rostec develops military equipment.")
    assert isinstance(result, list)
    assert all("text" in entity and "label" in entity for entity in result)
