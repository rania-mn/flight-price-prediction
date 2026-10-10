from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

FASTAPI_URL = "http://127.0.0.1:8000/predict"

# Options complètes pour le formulaire 
airlines = ['SpiceJet', 'AirAsia', 'Vistara', 'GO_FIRST', 'Indigo', 'Air_India']
source_cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']
departure_times = ['Evening', 'Early_Morning', 'Morning', 'Afternoon', 'Night', 'Late_Night']
stops_list = ['zero', 'one', 'two_or_more']
arrival_times = ['Night', 'Morning', 'Early_Morning', 'Afternoon', 'Evening', 'Late_Night']
destination_cities = ['Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai', 'Delhi']
classes = ['Economy', 'Business']

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

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None

    if request.method == "POST":
        #Si l'utilisateur importe un fichier JSON 
        if 'json_file' in request.files and request.files['json_file'].filename != "":
            file = request.files['json_file']
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                prediction = "Erreur : fichier JSON invalide"
                return render_template("index.html",prediction=prediction,
                        airlines=airlines,
                        source_cities=source_cities,
                        departure_times=departure_times,
                        arrival_times=arrival_times,
                        destination_cities=destination_cities,
                        stops_list=stops_list,
                        classes=classes)

          #sinon, saisir duration + days_left + options dropdown
        else:
            form = request.form
            data = {col: False for col in FEATURE_COLUMNS}
            try:
                data["duration"] = float(form["duration"])
                data["days_left"] = int(form["days_left"])
            except:
                prediction = "Veuillez saisir duration et days_left correctement"
                return render_template("index.html",prediction=prediction,
                        airlines=airlines,
                        source_cities=source_cities,
                        departure_times=departure_times,
                        arrival_times=arrival_times,
                        destination_cities=destination_cities,
                        stops_list=stops_list,
                        classes=classes)

            # One-Hot Encoding pour catégories
            # Airline
            airline = form["airline"]
            col = f"airline_{airline}"
            if col in data:
                data[col] = True

            # Source
            src = form["source_city"]
            data[f"source_city_{src}"] = True

            # Departure
            dep = form["departure_time"]
            if f"departure_time_{dep}" in data:
                data[f"departure_time_{dep}"] = True

            # Arrival
            arr = form["arrival_time"]
            if f"arrival_time_{arr}" in data:
                data[f"arrival_time_{arr}"] = True

            # Destination
            dst = form["destination_city"]
            data[f"destination_city_{dst}"] = True

            # Stops
            stops = form["stops"]
            if f"stops_{stops}" in data:
                data[f"stops_{stops}"] = True

            # Class
            cls = form["class"]
            if cls == "Economy":
                data["class_Economy"] = True

        # Envoi à FastAPI
        response = requests.post(FASTAPI_URL, json=data)

        if response.status_code == 200:
            prediction = response.json().get("predicted_price_real", None)
        else:
            prediction = "Erreur API"

    return render_template("index.html",prediction=prediction,
        airlines=airlines,
        source_cities=source_cities,
        departure_times=departure_times,
        arrival_times=arrival_times,
        destination_cities=destination_cities,
        stops_list=stops_list,
        classes=classes
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
