import streamlit as st
import joblib
import pandas as pd

# Load the saved model
model_path = "ultimate_6_model.pkl"  # Ensure the path matches the saved model
rf_model = joblib.load(model_path)

# Load the dataset to get the exact options for each parameter
data_path = "DataAll.xlsx"  # Path to your original dataset
data = pd.read_excel(data_path)

# Extract unique values for each parameter from the dataset
parameters = {
    "Previous_Day_Trend": data["Previous_Day_Trend"].unique().tolist(),
    "Opening_Position": data["Opening_Position"].unique().tolist(),
    "2hr_Zone_Touch": data["2hr_Zone_Touch"].unique().tolist(),
    "30m_Zone_Touch": data["30m_Zone_Touch"].unique().tolist(),
    "Position_PDH": data["Position_PDH"].unique().tolist(),
    "30m_Candle": data["30m_Candle"].unique().tolist()
}

# Streamlit App
st.title("Market Direction Prediction App")
st.markdown("This app predicts the market direction based on the parameters you select.")

# Create dropdowns for each parameter
user_input = {}
for parameter, values in parameters.items():
    user_input[parameter] = st.selectbox(f"Select {parameter}:", values)

# Button to predict
if st.button("Predict Market Direction"):
    # Convert input to DataFrame and encode
    input_data = pd.DataFrame([user_input])
    
    # Encode user inputs based on dataset
    encoding_map = {col: {val: i for i, val in enumerate(parameters[col])} for col in parameters.keys()}
    input_data_encoded = input_data.replace(encoding_map)
    
    # Predict using the model
    prediction = rf_model.predict(input_data_encoded)[0]
    prediction_label = "Long" if prediction == 1 else "Short"
    
    # Display prediction
    st.success(f"The predicted market direction is: **{prediction_label}**")
