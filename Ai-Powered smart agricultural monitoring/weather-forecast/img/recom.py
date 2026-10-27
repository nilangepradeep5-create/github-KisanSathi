import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
from PIL import Image
import requests
import time

# Page config
st.set_page_config(page_title="🌱 Smart Crop Recommendation System", layout="wide", page_icon="🌾")

# Custom CSS with larger fonts and background
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-green: #2E7D32;
        --secondary-green: #4CAF50;
        --light-green: #A5D6A7;
        --dark-green: #1B5E20;
        --accent-gold: #FFB300;
    }

    /* Background Image */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.98)),
                    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
    }

    /* Header Styling with LARGER FONTS */
    .main-header {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.95), rgba(76, 175, 80, 0.95));
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(46, 125, 50, 0.3);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }
    .main-subtitle {
        font-size: 1.6rem !important;
        opacity: 0.95;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* Card Styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border: 2px solid rgba(46, 125, 50, 0.2);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(46, 125, 50, 0.2);
    }

    /* Input Container */
    .input-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 2px solid rgba(46, 125, 50, 0.2);
    }
    
    .input-title {
        font-size: 1.8rem !important;
        color: var(--primary-green) !important;
        margin-bottom: 1.5rem !important;
        font-weight: 700 !important;
        text-align: center;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-green), var(--secondary-green));
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 40px;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(46, 125, 50, 0.4);
    }

    /* Result Cards */
    .result-card {
        background: linear-gradient(135deg, rgba(232, 245, 232, 0.98), rgba(200, 230, 201, 0.98));
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(46, 125, 50, 0.15);
        border-left: 6px solid var(--primary-green);
    }

    /* Crop Badge */
    .crop-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent-gold), #FFCA28);
        color: var(--dark-green);
        padding: 1rem 2rem;
        border-radius: 40px;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        box-shadow: 0 5px 15px rgba(255, 179, 0, 0.3);
        margin: 0.5rem;
        border: 2px solid white;
        text-transform: uppercase;
    }

    /* Labels */
    label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: var(--dark-green) !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.95), rgba(27, 94, 32, 0.95));
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 8px 20px rgba(46, 125, 50, 0.2);
    }
    
    .footer h3 {
        font-size: 1.8rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    .footer p {
        font-size: 1.1rem !important;
        opacity: 0.9;
        margin-bottom: 0.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Create simplified dataset with only required parameters
np.random.seed(42)
n_samples = 300

data = {
    'N': np.random.uniform(0, 200, n_samples).round(1),
    'P': np.random.uniform(0, 150, n_samples).round(1),
    'K': np.random.uniform(0, 250, n_samples).round(1),
    'rainfall': np.random.uniform(100, 400, n_samples).round(1),
    'humidity': np.random.uniform(20, 95, n_samples).round(1),
    'temperature': np.random.uniform(10, 40, n_samples).round(1),  # Added temperature
}

df = pd.DataFrame(data)

# Assign crops based on simplified conditions
def assign_crop_simple(row):
    n, p, k = row['N'], row['P'], row['K']
    rainfall = row['rainfall']
    humidity = row['humidity']
    temperature = row['temperature']  # Added temperature
    
    # Rice - needs high rainfall, humidity, and warm temperature
    if rainfall > 300 and humidity > 80 and n > 100 and temperature > 20:
        return 'rice'
    
    # Wheat - moderate conditions, cooler temperature
    elif 200 < rainfall < 300 and 50 < humidity < 80 and p > 40 and 15 < temperature < 25:
        return 'wheat'
    
    # Maize - good rainfall, potassium, and warm temperature
    elif rainfall > 250 and humidity > 60 and k > 100 and temperature > 18:
        return 'maize'
    
    # Cotton - lower humidity needs, warm temperature
    elif rainfall < 250 and humidity < 60 and n > 80 and temperature > 22:
        return 'cotton'
    
    # Sugarcane - high rainfall, warm temperature
    elif rainfall > 350 and humidity > 75 and temperature > 20:
        return 'sugarcane'
    
    # Fruits based on conditions - warm temperatures
    elif humidity > 70 and rainfall > 200 and temperature > 18:
        return np.random.choice(['banana', 'papaya', 'pineapple', 'mango', 'coconut'])
    
    # Vegetables - moderate conditions, moderate temperature
    elif 150 < rainfall < 300 and 50 < humidity < 80 and 15 < temperature < 30:
        return np.random.choice(['tomato', 'potato', 'cucumber', 'onion'])
    
    # Legumes - lower nitrogen needs, moderate temperature
    elif n < 80 and p > 30 and 15 < temperature < 30:
        return np.random.choice(['mungbean', 'chickpea', 'kidneybeans', 'lentil'])
    
    # Coffee - specific humidity, rainfall, and temperature
    elif 150 < rainfall < 300 and 70 < humidity < 90 and 18 < temperature < 25:
        return 'coffee'
    
    # Jute - high rainfall, warm temperature
    elif rainfall > 300 and temperature > 22:
        return 'jute'
    
    # Watermelon - hot and humid
    elif humidity > 70 and rainfall > 200 and temperature > 25:
        return 'watermelon'
    
    else:
        # Default based on primary nutrients and temperature
        if temperature > 25:
            if n > p and n > k:
                return 'cotton'
            elif p > n and p > k:
                return 'potato'
            else:
                return 'banana'
        else:
            if n > p and n > k:
                return 'wheat'
            elif p > n and p > k:
                return 'potato'
            else:
                return 'mungbean'

df['label'] = df.apply(assign_crop_simple, axis=1)

# Train model with only required features
feature_cols = ['N', 'P', 'K', 'rainfall', 'humidity', 'temperature']  # Added temperature

X = df[feature_cols]
y = df['label']

model = RandomForestClassifier(
    n_estimators=200, 
    random_state=42, 
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2
)
model.fit(X, y)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌱 CROP RECOMMENDATION SYSTEM</h1>
    <p class="main-subtitle">AI-powered recommendations based on Soil Nutrients, Climate & Weather Conditions</p>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<h1 class="input-title">📊 ENTER PARAMETERS</h1>', unsafe_allow_html=True)

# Create columns for input
col1, col2 = st.columns(2)

with col1:
    st.markdown('### 🌿 SOIL NUTRIENTS')
    N = st.slider("**NITROGEN (N) in kg/ha**", 0.0, 200.0, 80.0, 1.0, 
                 help="Essential for leaf growth and plant development")
    P = st.slider("**PHOSPHORUS (P) in kg/ha**", 0.0, 150.0, 45.0, 1.0,
                 help="Important for root development and flowering")
    K = st.slider("**POTASSIUM (K) in kg/ha**", 0.0, 250.0, 120.0, 1.0,
                 help="Essential for fruit quality and disease resistance")

with col2:
    st.markdown('### 🌧️ CLIMATE FACTORS')
    rainfall = st.slider("**ANNUAL RAINFALL in mm**", 100.0, 400.0, 250.0, 10.0,
                       help="Total annual rainfall in millimeters")
    humidity = st.slider("**AVERAGE HUMIDITY in %**", 20.0, 95.0, 65.0, 1.0,
                        help="Average relative humidity percentage")
    temperature = st.slider("**AVERAGE TEMPERATURE in °C**", 10.0, 40.0, 25.0, 0.5,  # Added temperature slider
                          help="Average annual temperature in Celsius")

st.markdown('</div>', unsafe_allow_html=True)

# Center the button
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_clicked = st.button("🚀 GET CROP RECOMMENDATIONS", type="primary", use_container_width=True)

if analyze_clicked:
    # Prepare input data
    input_data = np.array([[
        N, P, K, rainfall, humidity, temperature  # Added temperature
    ]])
    
    # Get predictions
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    # Top recommendations
    prob_df = pd.DataFrame({
        'Crop': model.classes_,
        'Probability': probabilities
    }).sort_values('Probability', ascending=False).head(8)
    
    # Display results
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Top recommendation - centered without image
    st.markdown(f"""
    <div style='text-align: center;'>
        <h1 style='color: var(--primary-green); margin-bottom: 1rem; font-size: 2.2rem;'>🎯 BEST CROP FOR YOUR SOIL</h1>
        <div class="crop-badge">{prediction.title()}</div>
        <p style='font-size: 1.4rem; color: var(--dark-green); margin-top: 1rem;'>
            Confidence: <strong style='font-size: 1.8rem;'>{prob_df[prob_df["Crop"] == prediction]["Probability"].iloc[0]:.1%}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <h3>🌾 Smart Agriculture System</h3>
    <p>25+ Crops • 6 Key Parameters • AI-Powered Recommendations</p>  <!-- Updated to 6 parameters -->
    <p style='font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;'>
        💡 Based on N, P, K nutrients, rainfall, humidity, and temperature data  <!-- Added temperature -->
    </p>
</div>
""", unsafe_allow_html=True)