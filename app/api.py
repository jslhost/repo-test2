from fastapi import FastAPI
from pydantic import BaseModel
from pickle import load
import pandas as pd
from src.utils import load_params
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://jslhost.github.io",  # Adresse GitHub Pages, à modifier avec votre identifiant github
    "http://localhost:8000",  # autorise les tests locaux
]


params = load_params()
model_path = params["model"]["path"]
preprocessor_path = params["model"]["preprocessor_path"]

with open(model_path, "rb") as f:
    model = load(f)

with open(preprocessor_path, "rb") as f:
    preprocessor = load(f)


class CustomerData(BaseModel):
    Surname: str
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


app = FastAPI(
    title="Prédiction de Churn",
    description="Application de prédiction de Churn 💸 <br>Une version par API pour faciliter la réutilisation du modèle 🚀",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)


@app.post("/predict", tags=["Predict"])
async def predict(data: CustomerData) -> str:
    """ """
    df = pd.DataFrame([data.model_dump()])

    preprocessed_data = preprocessor.transform(df)

    prediction = (
        "Exited" if int(model.predict(preprocessed_data)) == 1 else "Not Exited"
    )

    return prediction, "test MAJ!"
