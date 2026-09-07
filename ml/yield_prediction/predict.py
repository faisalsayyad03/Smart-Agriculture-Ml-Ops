# Make the predictions

# Import necessary libraries
import pandas as pd
import joblib
from pathlib import Path

# Get project root
project_root = Path(__file__).resolve().parents[2]

# Model path
model_path = project_root / "backend" / "app" / "models" / "random_forest_model.pkl"

# Load the trained model
model = joblib.load(model_path)

# New data for prediction
new_data = pd.DataFrame({
    "Crop Type": ["Rice"],
    "Soil Type": ["Clay"],
    "Fertilizer Used": ["Yes"],
    "Irrigation Type": ["Drip"],
    "Field Size (hectares)": [2.5],
    "Planting_Year": [2023],
    "Planting_Month": [5],
    "Planting_Day": [15],
    "Planting_DayOfYear": [135],
    "Planting_Quarter": [2]
})

# Make prediction
prediction = model.predict(new_data)

# Print prediction
print(f"Predicted Yield: {prediction[0]}")