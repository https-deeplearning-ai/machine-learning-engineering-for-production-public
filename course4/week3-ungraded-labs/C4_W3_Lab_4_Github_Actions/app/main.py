import pickle
import numpy as np
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, conlist



app = FastAPI(title="Predicting Wine Class with batching")

# Open classifier in global scope
with open("models/wine.pkl", "rb") as file:
    clf = pickle.load(file)


class Wine(BaseModel):
    batches: List[conlist(item_type=float, min_items=13, max_items=13)]


@app.post("/predict")
def predict(wine: Wine):
    batches = wine.batches
    np_batches = np.array(batches)
    pred = clf.predict(np_batches).tolist()
    return {"Prediction": pred}
