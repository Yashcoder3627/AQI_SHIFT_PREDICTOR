from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pickle
import numpy as np

app = FastAPI()

# Templates folder setup
templates = Jinja2Templates(directory="templates")

# Trained model load karein
model = pickle.load(open("model.pkl", "rb"))

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Naye syntax mein request ko pehle paas karte hain
    return templates.TemplateResponse(request, "index.html", {"prediction": None})

@app.post("/", response_class=HTMLResponse)
def predict(
    request: Request,
    temp_anomaly: float = Form(...),
    wind_speed: float = Form(...),
    industrial_emission: float = Form(...),
    traffic_density: float = Form(...)
):
    # Features ko array mein convert karein jaise model expect karta hai
    input_data = np.array([[temp_anomaly, wind_speed, industrial_emission, traffic_density]])
    
    # Prediction run karein
    prediction = model.predict(input_data)[0]
    
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "prediction": round(float(prediction), 2),
            "temp_anomaly": temp_anomaly,
            "wind_speed": wind_speed,
            "industrial_emission": industrial_emission,
            "traffic_density": traffic_density
        }
    )