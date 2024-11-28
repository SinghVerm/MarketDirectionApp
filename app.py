import streamlit as st
import pandas as pd
import pickle

# Load the trained model
with open('final_random_forest_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Title for the app
st.title("Netrunner: Market Direction Prediction App")

# Input feature explanations
st.subheader("Blackwall")


# Dropdown menus for each feature
previous_day_trend = st.selectbox(
    "Previous Day Trend:",
    ["", "Double Top", "Double Bottom", "Long", "No View", "Short"]
)
ma9 = st.selectbox(
    "MA9 (9-day Moving Average):",
    ["", "Long", "Short"]
)
day_trend = st.selectbox(
    "Day Trend:",
    ["", "Long", "Short", "Sideways"]
)
candle_30m = st.selectbox(
    "30-minute Candle:",
    ["", "Doji", "Green", "Green Hammer", "Inverted Hammer", "Red", "Red Hammer", "Shooting Star"]
)

# Hardcoded encoding logic
def encode_features(previous_day_trend, ma9, day_trend, candle_30m):
    # Encoding logic as per your description
    encoded = {
        "Previous_Day_Trend": (
            1 if previous_day_trend == "Double Top" else
            0 if previous_day_trend == "Double Bottom" else
            2 if previous_day_trend == "Long" else
            3 if previous_day_trend == "No View" else
            4 if previous_day_trend == "Short" else -1
        ),
        "MA9": (
            0 if ma9 == "Long" else
            1 if ma9 == "Short" else -1
        ),
        "Day_Trend": (
            0 if day_trend == "Long" else
            1 if day_trend == "Short" else
            2 if day_trend == "Sideways" else -1
        ),
        "30m_Candle": (
            0 if candle_30m == "Doji" else
            1 if candle_30m == "Green" else
            2 if candle_30m == "Green Hammer" else
            3 if candle_30m == "Inverted Hammer" else
            4 if candle_30m == "Red" else
            5 if candle_30m == "Red Hammer" else
            6 if candle_30m == "Shooting Star" else -1
        )
    }
    return encoded

# Encode the inputs
if st.button("Predict Market Direction"):
    if not previous_day_trend or not ma9 or not day_trend or not candle_30m:
        st.error("Please select values for all features!")
    else:
        encoded_input = encode_features(previous_day_trend, ma9, day_trend, candle_30m)
        
        # Create input DataFrame
        input_data = pd.DataFrame([encoded_input])

        # Make prediction
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]

        # Interpret prediction
        direction = "Long" if prediction == 0 else "Short"
        st.subheader(f"Predicted Market Direction: {direction}")
        st.write(f"Probability of Long: {probabilities[0]:.2f}")
        st.write(f"Probability of Short: {probabilities[1]:.2f}")
