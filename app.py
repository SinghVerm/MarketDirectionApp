import streamlit as st
import joblib
import pandas as pd

# Load the saved model
model_path = "Ultimate_6_model.pkl"  # Ensure the path matches the saved model
rf_model = joblib.load(model_path)

# Define the hardcoded encodings based on provided formulas
encoding_map = {
    "Previous_Day_Trend": {
        0: "Double Top",
        1: "Double Bottom",
        2: "Long",
        3: "No View",
        4: "Short"
    },
    "Opening_Position": {
        0: "Above Resistance",
        1: "Below Support",
        2: "Middle",
        3: "Resistance",
        4: "Support"
    },
    "2hr_Zone_Touch": {
        0: "No Touch",
        1: "Resistance H Above",
        2: "Resistance H Below",
        3: "Resistance H In Zone",
        4: "Resistance L Above",
        5: "Resistance L Below",
        6: "Resistance L In Zone",
        7: "Support H",
        8: "Support H Above",
        9: "Support H In Zone",
        10: "Support L",
        11: "Support L Above",
        12: "Support L Below",
        13: "Support L In Zone"
    },
    "30m_Zone_Touch": {
        0: "No Touch",
        1: "Touched Both",
        2: "Touched Both Above",
        3: "Touched Both Below",
        4: "Touched Both In Resistance Zone",
        5: "Touched Both In Support Zone",
        6: "Touched Both Middle",
        7: "Touched Resistance Above",
        8: "Touched Resistance Below",
        9: "Touched Support Above",
        10: "Touched Support Below"
    },
    "Position_PDH": {
        0: "Above",
        1: "Below",
        2: "No Touch"
    },
    "30m_Candle": {
        0: "Doji",
        1: "Green",
        2: "Green Hammer",
        3: "Inverted Hammer",
        4: "Red",
        5: "Red Hammer",
        6: "Shooting Star",
        7: "Strong Green",
        8: "Strong Red"
    }
}

# Reverse encoding map for predictions
decoding_map = {col: {v: k for k, v in mapping.items()} for col, mapping in encoding_map.items()}

# Streamlit App
st.title("Market Direction Prediction App")
st.markdown("This app predicts the market direction based on the parameters you select.")

# Create dropdowns for each parameter with user-friendly text
user_input = {}
for parameter, mapping in encoding_map.items():
    user_input[parameter] = st.selectbox(f"Select {parameter}:", list(mapping.values()))

# Button to predict
if st.button("Predict Market Direction"):
    # Convert user inputs (text) to encoded numerical values
    input_data = pd.DataFrame([{param: decoding_map[param][value] for param, value in user_input.items()}])
    
    # Predict using the model
    prediction = rf_model.predict(input_data)[0]
    prediction_label = "Long" if prediction == 0 else "Short"  # Adjust based on `Market_Direction` encoding
    
    # Display prediction
    st.success(f"The predicted market direction is: **{prediction_label}**")
