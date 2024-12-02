import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load('xgb_full_model.pkl')

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

thirty_pdh_options = {
    "Select an option": None,
    "Above": 0,
    "Below": 1,
    "No Touch": 2
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

# Title
st.title("Blackwall")

# User Inputs
st.header("Input Features")
previous_day_trend = st.selectbox("Previous Day Trend", options=list(previous_day_trend_options.keys()))
opening_position = st.selectbox("Opening Position", options=list(opening_position_options.keys()))
thirty_pdh = st.selectbox("30 PDH", options=list(thirty_pdh_options.keys()))
thirty_min_candle = st.selectbox("30m Candle", options=list(thirty_min_candle_options.keys()))
ultimate_sr = st.selectbox("Ultimate S/R", options=list(ultimate_sr_options.keys()))

# Check for missing values
if None in [
    previous_day_trend_options[previous_day_trend],
    opening_position_options[opening_position],
    thirty_pdh_options[thirty_pdh],
    thirty_min_candle_options[thirty_min_candle],
    ultimate_sr_options[ultimate_sr],
]:
    st.warning("Please select a value for all features before making a prediction.")
else:
    # Encode user inputs
    input_features = np.array([
        previous_day_trend_options[previous_day_trend],
        opening_position_options[opening_position],
        thirty_pdh_options[thirty_pdh],
        thirty_min_candle_options[thirty_min_candle],
        ultimate_sr_options[ultimate_sr]
    ]).reshape(1, -1)

    # Predict button
    if st.button("Predict"):
        prediction = model.predict(input_features)
        prediction_label = "Long" if prediction[0] == 0 else "Short"
        st.write(f"**Prediction:** {prediction_label}")
