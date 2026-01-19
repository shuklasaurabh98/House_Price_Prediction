
from flask import Flask, render_template_string, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

model = joblib.load("house_price_model_with_location.pkl")

# STATE_ENCODING = {
#     "Karnataka": 4,
#     "Uttar Pradesh": 3,
#     "Uttrakhand": 3,
#     "Kerala": 4,
#     "Bihar": 2
# }
CITY_ENCODING = {
    "Bengaluru": 4, "Mysuru": 3, "Mangaluru": 3,
    "Lucknow": 3, "Noida": 4, "Kanpur": 2,
    "Dehradun": 3, "Haridwar": 2, "Rishikesh": 2,
    "Kochi": 4, "Trivandrum": 3, "Kozhikode": 3,
    "Patna": 3, "Gaya": 2, "Muzaffarpur": 2
}

# HTML = '''
# <!DOCTYPE html>
# <html>
# <head>
#     <title>House Price Prediction</title>
#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
# </head>
# <body class="bg-light">
# <div class="container mt-5">
#     <div class="card shadow p-4">
#         <h2 class="text-center mb-4">🏠 AI House Price Prediction</h2>
#         <form method="POST">
#             <div class="mb-3">
#                 <label class="form-label">Area (sqft)</label>
#                 <input type="number" class="form-control" name="area" required>
#             </div>
#             <div class="mb-3">
#                 <label class="form-label">Bedrooms</label>
#                 <input type="number" class="form-control" name="bedrooms" required>
#             </div>
#             <div class="mb-3">
#                 <label class="form-label">Bathrooms</label>
#                 <input type="number" class="form-control" name="bathrooms" required>
#             </div>
#             <button type="submit" class="btn btn-primary w-100">Predict Price</button>
#         </form>

#         {% if price %}
#         <div class="alert alert-success mt-4 text-center">
#             <h4>Predicted Price: ₹ {{ price }}</h4>
#         </div>
#         {% endif %}
#     </div>
# </div>
# </body>
# </html>
# '''

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>House Price Prediction</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
        body {
            background-image: url("/static/charming-white-colonial-home-with-welcoming-front-porch.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;
        }

        .overlay {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 12px;
            max-width: 500px;
            margin: auto;
            margin-top: 80px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
    </style>
</head>

<body>
    <div class="overlay">
        <h2 class="text-center mb-4">🏠 AI House Price Prediction</h2>

        <form method="POST">
            <div class="mb-3">
                <label class="form-label">Area (sqft)</label>
                <input type="number" class="form-control" name="area" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Bedrooms</label>
                <input type="number" class="form-control" name="bedrooms" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Bathrooms</label>
                <input type="number" class="form-control" name="bathrooms" required>
            </div>

            <div class = "mb-3">
                <label class="form-label">State</label>
                <select class="form-select" id = "state" name="state" onchange="updateCities()" required>
                   <option value="">Select State</option>
                   <option value="Karnataka">Karnataka</option>
                   <option value="Uttar Pradesh">Uttar Pradesh</option>
                   <option value="Uttarakhand">Uttarakhand</option>
                   <option value="Kerala">Kerala</option>
                   <option value="Bihar">Bihar</option>
                </select>
            </div>

            <div class="mb-3">
                <label class="form-label">City</label>
                <select class="form-select" id="city" name="city" required>
                    <option value="">Select City</option>
                </select>
            </div>



            <button type="submit" class="btn btn-primary w-100">
                Predict Price
            </button>
        </form>

        {% if price %}
        <div class="alert alert-success mt-4 text-center">
            <h4>Predicted Price: ₹ {{ price }}</h4>
        </div>
        {% endif %}
    </div>

  
<script>
    const stateCityMap = {
        "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru"],
        "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh"],
        "Kerala": ["Kochi", "Trivandrum", "Kozhikode"],
        "Bihar": ["Patna", "Gaya", "Muzaffarpur"]
    };

    function updateCities() {
        const stateSelect = document.getElementById("state");
        const citySelect = document.getElementById("city");

        const selectedState = stateSelect.value;

        // Clear existing cities
        citySelect.innerHTML = '<option value="">Select City</option>';

        if (selectedState && stateCityMap[selectedState]) {
            stateCityMap[selectedState].forEach(city => {
                const option = document.createElement("option");
                option.value = city;
                option.text = city;
                citySelect.appendChild(option);
            });
        }
    }
</script>

</body>
</html>
'''


@app.route("/", methods=["GET", "POST"])
def predict():
    price = None
    if request.method == "POST":
        area = int(request.form["area"])
        bedrooms = int(request.form["bedrooms"])
        bathrooms = int(request.form["bathrooms"])
        # state= request.form["state"]
        city = request.form["city"]
        
        # state_value = STATE_ENCODING.get(state, 2)
        city_value = CITY_ENCODING.get(city, 2)
        

        prediction = model.predict([[area, bedrooms, bathrooms, city_value]])[0]
        price = f"{int(prediction):,}"

    return render_template_string(HTML, price=price)

if __name__ == "__main__":
    app.run(debug=True)
