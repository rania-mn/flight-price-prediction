from fastapi import FastAPI
import numpy as np
import pickle
from pydantic import BaseModel

# Charger le modèle
model = pickle.load(open("flight_price_model.pkl", "rb"))

app = FastAPI(
    title="Flight Price Prediction API",
    description="API pour prédire le prix des vols après preprocessing",
    version="1.0"
)

# Colonnes EXACTES du modèle (30 features)
FEATURE_COLUMNS = [
    'duration', 'days_left', 'airline_Air_India', 'airline_GO_FIRST',
    'airline_Indigo', 'airline_SpiceJet', 'airline_Vistara',
    'source_city_Chennai', 'source_city_Delhi', 'source_city_Hyderabad',
    'source_city_Kolkata', 'source_city_Mumbai',
    'departure_time_Early_Morning', 'departure_time_Evening',
    'departure_time_Late_Night', 'departure_time_Morning',
    'departure_time_Night', 'stops_two_or_more', 'stops_zero',
    'arrival_time_Early_Morning', 'arrival_time_Evening',
    'arrival_time_Late_Night', 'arrival_time_Morning', 'arrival_time_Night',
    'destination_city_Chennai', 'destination_city_Delhi',
    'destination_city_Hyderabad', 'destination_city_Kolkata',
    'destination_city_Mumbai', 'class_Economy'
]

# Model d'entrée correspondant EXACTEMENT au modèle
# les colonnes booleennes aient par défaut la valeur false
class FlightInput(BaseModel):
    duration: float
    days_left: int
    airline_Air_India:  bool = False
    airline_GO_FIRST:  bool = False
    airline_Indigo:  bool = False
    airline_SpiceJet:  bool = False
    airline_Vistara:  bool = False
    source_city_Chennai:  bool = False
    source_city_Delhi:  bool = False
    source_city_Hyderabad:  bool = False
    source_city_Kolkata:  bool = False
    source_city_Mumbai:  bool = False
    departure_time_Early_Morning:  bool = False
    departure_time_Evening:  bool = False
    departure_time_Late_Night:  bool = False
    departure_time_Morning:  bool = False
    departure_time_Night:  bool = False
    stops_two_or_more:  bool = False
    stops_zero:  bool = False
    arrival_time_Early_Morning:  bool = False
    arrival_time_Evening:  bool = False
    arrival_time_Late_Night:  bool = False
    arrival_time_Morning:  bool = False
    arrival_time_Night:  bool = False
    destination_city_Chennai:  bool = False
    destination_city_Delhi:  bool = False
    destination_city_Hyderabad:  bool = False
    destination_city_Kolkata:  bool = False
    destination_city_Mumbai:  bool = False
    class_Economy:  bool = False

@app.get("/")
def home():
    return {"message": "Flight Price Prediction API is running!"}

@app.post("/predict")
def predict_price(data: FlightInput):

    # Récupérer les valeurs SANS modifications
    values = [int(getattr(data, col)) if isinstance(getattr(data, col), bool) 
          else getattr(data, col) for col in FEATURE_COLUMNS]

    # Transformer en 2D
    array_input = np.array(values).reshape(1, -1)

    # Prédiction (prix standarisé)
    prediction_scaled = model.predict(array_input)[0]

    # Déscaler pour obtenir le prix réel
    #selon statistiques numériques de Clean_Dataset: PRICE_MEAN :20889.660523 ET PRICE_STD:  22697.767366 
    PRICE_MEAN = 20889.660523
    PRICE_STD  = 22697.767366 
    predicted_price_real = prediction_scaled * PRICE_STD + PRICE_MEAN  

    return {
        "predicted_price_scaled": float(prediction_scaled),
        "predicted_price_real": float(predicted_price_real),
        "note": "Le prix réel est recalculé à partir du prix standardisé."
    }

