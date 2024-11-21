import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model_path = "Ultimate5_updated.pkl"  # Ensure this file is in your working directory
model = joblib.load(model_path)

# Dropdown options based on your manual encoding
previous_day_trend_options = {
    "Double Bottom": 0,
    "Double Top": 1,
    "Long": 2,
    "No View": 3,
    "Short": 4
}

opening_position_options = {
    "Above Resistance": 0,
    "Below Support": 1,
    "Middle": 2,
    "Resistance": 3,
    "Support": 4
}

zone_touch_30m_options = {
    "No Touch": 0,
    "Touched Both Above": 1,
    "Touched Both Below": 2,
    "Touched Both In Resistance Zone": 3,
    "Touched Both In Support Zone": 4,
    "Touched Both Middle": 5,
    "Touched Resistance Above": 6,
    "Touched Resistance Below": 7,
    "Touched Support Above": 8,
    "Touched Support Below": 9
}

position_pdh_options = {
    "Above": 0,
    "Below": 1,
    "No Touch": 2
}

candle_options = {
    "Doji": 0,
    "Green": 1,
    "Green Hammer": 2,
    "Inverted Hammer": 3,
    "Red": 4,
    "Red Hammer": 5,
    "Shooting Star": 6
}

# Title and dropdown inputs
st.title("Dexter")

# Input dropdowns for the 5 parameters
previous_day_trend = st.selectbox(
    "Previous Day Trend:",
    options=list(previous_day_trend_options.keys())
)
opening_position = st.selectbox(
    "Opening Position:",
    options=list(opening_position_options.keys())
)
zone_touch_30m = st.selectbox(
    "30M Zone Touch:",
    options=list(zone_touch_30m_options.keys())
)
position_pdh = st.selectbox(
    "PDH:",
    options=list(position_pdh_options.keys())
)
candle = st.selectbox(
    "30MCandle:",
    options=list(candle_options.keys())
)

# Encode user inputs
user_input = pd.DataFrame([{
    "Previous_Day_Trend": previous_day_trend_options[previous_day_trend],
    "30m_Zone_Touch": zone_touch_30m_options[zone_touch_30m],
    "Opening_Position": opening_position_options[opening_position],
    "Position_PDH": position_pdh_options[position_pdh],
    "30m_Candle": candle_options[candle]
}])

# Predict and display result
if st.button("Predict Market Direction"):
    prediction = model.predict(user_input)[0]
    probabilities = model.predict_proba(user_input)[0]
    direction = "Long" if prediction == 0 else "Short"
    confidence = probabilities[prediction] * 100

    st.write(f"Predicted Market Direction: **{direction}**")
    st.write(f"Model Confidence: **{confidence:.2f}%**")
