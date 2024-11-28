import streamlit as st
import pandas as pd
import joblib

# Load the trained Random Forest model
model = joblib.load("Opening_PrevDay_PDH_30MCandle.pkl")

# Title of the app
st.title("Netrunner")

# Define dropdown options for each feature
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

# Collect user inputs for the features using dropdowns
st.header("Input Features")

previous_day_trend = st.selectbox(
    "Previous Day Trend:", list(previous_day_trend_options.keys())
)
opening_position = st.selectbox(
    "Opening Position:", list(opening_position_options.keys())
)
position_pdh = st.selectbox(
    "Position PDH:", list(position_pdh_options.keys())
)
candle_30m = st.selectbox(
    "30-minute Candle:", list(candle_options.keys())
)

# Convert the selected labels to the corresponding numeric values for the model
previous_day_trend_value = previous_day_trend_options[previous_day_trend]
opening_position_value = opening_position_options[opening_position]
position_pdh_value = position_pdh_options[position_pdh]
candle_30m_value = candle_options[candle_30m]

# Button to make prediction
if st.button("Predict Market Direction"):
    # Create a DataFrame for the input data
    input_data = pd.DataFrame({
        'Previous_Day_Trend': [previous_day_trend_value],
        'Opening_Position': [opening_position_value],
        'Position_PDH': [position_pdh_value],
        '30m_Candle': [candle_30m_value]
    })
    
    # Ensure feature order matches the trained model
    input_data = input_data[model.feature_names_in_]

    # Make prediction
    prediction = model.predict(input_data)[0]
    prediction_label = "Long" if prediction == 0 else "Short"

    # Display the result
    st.subheader(f"Predicted Market Direction: {prediction_label}")

    # Display predicted probabilities (optional)
    probabilities = model.predict_proba(input_data)[0]
    st.write(f"Probability of Long: {probabilities[0]:.2f}")
    st.write(f"Probability of Short: {probabilities[1]:.2f}")
