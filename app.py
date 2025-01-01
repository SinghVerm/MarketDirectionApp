import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model_data = joblib.load('xgb_model_full_data.pkl')  # Correct model name
model = model_data['model']  # Trained model
features = model.feature_names_in_  # Feature order in the model

# Dropdown options for each feature
previous_day_trend_options = {
    "Select an option": None,
    "Double Top": 1,
    "Double Bottom": 0,
    "Long": 2,
    "No View": 3,
    "Short": 4
}

opening_position_options = {
    "Select an option": None,
    "Above Resistance": 0,
    "Below Support": 1,
    "Middle": 2,
    "Resistance": 3,
    "Support": 4
}

thirty_min_candle_options = {
    "Select an option": None,
    "Doji": 0,
    "Green": 1,
    "Green Hammer": 2,
    "Inverted Hammer": 3,
    "Red": 4,
    "Red Hammer": 5,
    "Shooting Star": 6
}

ultimate_sr_options = {
    "Select an option": None,
    "No Touch": 0,
    "Resistance Above": 1,
    "Support Below": 2,
    "Touched Both Above": 3,
    "Touched Both Below": 4,
    "Touched Both In Resistance Zone": 5,
    "Touched Both In Support Zone": 6,
    "Touched Both Middle": 7,
    "Touched Resistance Below": 9,
    "Touched Support Above": 10
}

stoch_options = {
    "Select an option": None,
    "Above": 0,
    "Below": 1,
    "Overbought": 2,
    
}

np_options = {
    "Select an option": None,
    "Above": 0,
    "Below": 1
}

# Title
st.title("BlackWall")

# User Inputs
previous_day_trend = st.selectbox("Previous Day Trend", options=list(previous_day_trend_options.keys()))
opening_position = st.selectbox("Opening Position", options=list(opening_position_options.keys()))
thirty_min_candle = st.selectbox("30m Candle", options=list(thirty_min_candle_options.keys()))
ultimate_sr = st.selectbox("Ultimate S/R", options=list(ultimate_sr_options.keys()))
stoch = st.selectbox("Stoch", options=list(stoch_options.keys()))
np_value = st.selectbox("NP", options=list(np_options.keys()))

# Check for missing values
if None in [
    previous_day_trend_options[previous_day_trend],
    opening_position_options[opening_position],
    thirty_min_candle_options[thirty_min_candle],
    ultimate_sr_options[ultimate_sr],
    stoch_options[stoch],
    np_options[np_value]
]:
    st.warning("Please select a value for all features before making a prediction.")
else:
    # Encode user inputs into the correct order
    input_features = pd.DataFrame([[
        previous_day_trend_options[previous_day_trend],
        opening_position_options[opening_position],
        thirty_min_candle_options[thirty_min_candle],
        ultimate_sr_options[ultimate_sr],
        stoch_options[stoch],
        np_options[np_value]
    ]], columns=[
        "Previous_Day_Trend", 
        "Opening_Position", 
        "30m_Candle", 
        "Ultimate S/R", 
        "Stoch",
        "NP"
    ])

    # Ensure feature order matches the trained model
    input_features = input_features[features]

    # Predict market direction
    prediction = model.predict(input_features)[0]
    prediction_label = "Long" if prediction == 0 else "Short"

    # Display the predicted market direction
    st.subheader(f"Probable Direction: {prediction_label}")

    # Display probabilities for Long and Short
    probabilities = model.predict_proba(input_features)[0]
    st.write(f"Probability of Long: {probabilities[0] * 100:.2f}%")
    st.write(f"Probability of Short: {probabilities[1] * 100:.2f}%")
