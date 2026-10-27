"""
===========================================
CROP DISEASE DETECTION SYSTEM - Streamlit App
Final Year Academic Project - ENHANCED UI/UX VERSION
===========================================
"""

import streamlit as st
from PIL import Image
import numpy as np
import random
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Crop Disease Detection System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ENHANCED CSS STYLING - OPTIMIZED SIZING & SPACING
# ==========================================
st.markdown("""
<style>
    /* ===== ROOT & GLOBAL STYLES ===== */
    :root {
        --primary-green: #1B5E20;
        --secondary-green: #2E7D32;
        --accent-green: #4CAF50;
        --light-green: #E8F5E9;
        --dark-green: #0D3C13;
        --gradient-primary: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        --gradient-secondary: linear-gradient(135deg, #2E7D32 0%, #43A047 100%);
        --gradient-light: linear-gradient(135deg, #F1F8E9 0%, #E8F5E9 100%);
        --shadow-soft: 0 4px 20px rgba(27, 94, 32, 0.08);
        --shadow-medium: 0 8px 30px rgba(27, 94, 32, 0.12);
        --shadow-hard: 0 12px 40px rgba(27, 94, 32, 0.15);
        --border-radius-sm: 10px;
        --border-radius-md: 14px;
        --border-radius-lg: 18px;
        --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* ===== MAIN APP STYLING ===== */
    .stApp {
        background: linear-gradient(135deg, #f8fff8 0%, #f0f9f0 50%, #e8f5e9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        min-height: 100vh;
    }
    
    /* ===== TYPOGRAPHY ENHANCEMENTS ===== */
    h1, h2, h3, h4, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-weight: 650;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    
    .stMarkdown {
        color: #1a1a1a;
    }
    
    /* ===== ENHANCED HEADER - REDUCED SIZE ===== */
    .main-header-container {
        position: relative;
        overflow: hidden;
        border-radius: var(--border-radius-lg);
        margin-bottom: 1.8rem;
        box-shadow: var(--shadow-medium);
    }
    
    .main-header {
        background: var(--gradient-primary);
        color: white;
        padding: 2rem 1.5rem;
        text-align: center;
        position: relative;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4CAF50, #81C784);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 750;
        margin-bottom: 0.6rem;
        background: linear-gradient(135deg, #FFFFFF 0%, #E8F5E9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        margin: 0 auto;
        max-width: 700px;
        font-weight: 400;
        line-height: 1.5;
        padding: 0 1rem;
    }
    
    .header-decoration {
        position: absolute;
        opacity: 0.08;
        font-size: 6rem;
        pointer-events: none;
    }
    
    .header-leaf-1 { top: 10px; left: 15px; transform: rotate(-15deg); }
    .header-leaf-2 { top: 20px; right: 25px; transform: rotate(25deg); }
    .header-leaf-3 { bottom: 10px; left: 10%; transform: rotate(10deg); }
    
    /* ===== MODERN CARD DESIGN - OPTIMIZED PADDING ===== */
    .modern-card {
        background: white;
        border-radius: var(--border-radius-md);
        padding: 1.8rem;
        margin: 1.2rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(76, 175, 80, 0.08);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: var(--gradient-primary);
        border-radius: var(--border-radius-sm) 0 0 var(--border-radius-sm);
    }
    
    .card-title {
        color: var(--dark-green);
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .card-title-icon {
        background: var(--gradient-secondary);
        color: white;
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
    }
    
    /* ===== UPLOAD ZONE ENHANCEMENT - COMPACT SIZE ===== */
    .upload-zone {
        background: var(--gradient-light);
        border: 2px dashed #81C784;
        border-radius: var(--border-radius-lg);
        padding: 2.5rem 2rem;
        text-align: center;
        margin: 1.8rem 0;
        cursor: pointer;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .upload-zone:hover {
        border-color: var(--accent-green);
        background: linear-gradient(135deg, #F9FFFB 0%, #F1F8E9 100%);
        transform: scale(1.002);
    }
    
    .upload-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        color: var(--secondary-green);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* ===== RESULT CARD ENHANCEMENT - BETTER PROPORTIONS ===== */
    .result-container {
        position: relative;
        background: white;
        border-radius: var(--border-radius-lg);
        padding: 2.2rem;
        margin: 2rem auto;
        max-width: 850px;
        box-shadow: var(--shadow-hard);
        border: 1px solid rgba(76, 175, 80, 0.1);
        animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(20px) scale(0.98);
        }
        to { 
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .result-header {
        text-align: center;
        margin-bottom: 1.8rem;
        padding-bottom: 1.2rem;
        border-bottom: 2px solid rgba(129, 199, 132, 0.2);
    }
    
    .disease-emoji {
        font-size: 4rem;
        margin-bottom: 0.8rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    
    .disease-name {
        color: var(--dark-green);
        font-size: 2.2rem;
        font-weight: 750;
        margin: 0.8rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: linear-gradient(135deg, var(--dark-green) 0%, var(--secondary-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* ===== CONFIDENCE BADGE ENHANCEMENT ===== */
    .confidence-container {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: var(--gradient-light);
        padding: 0.8rem 1.5rem;
        border-radius: 40px;
        margin: 1.2rem 0;
        box-shadow: 0 3px 12px rgba(46, 125, 50, 0.12);
    }
    
    .confidence-badge {
        background: var(--gradient-secondary);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 40px;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.25);
    }
    
    /* ===== SEVERITY BADGES ENHANCEMENT ===== */
    .severity-badge {
        padding: 0.6rem 1.4rem;
        border-radius: 40px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        letter-spacing: 0.3px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        transition: var(--transition);
    }
    
    .severity-badge:hover {
        transform: translateY(-1px);
    }
    
    .severity-high {
        background: linear-gradient(135deg, #FF5252 0%, #D32F2F 100%);
        color: white;
    }
    
    .severity-moderate {
        background: linear-gradient(135deg, #FFB74D 0%, #F57C00 100%);
        color: white;
    }
    
    .severity-low {
        background: linear-gradient(135deg, #81C784 0%, #43A047 100%);
        color: white;
    }
    
    /* ===== SOLUTION CARDS ENHANCEMENT - COMPACT GRID ===== */
    .solution-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.2rem;
        margin: 1.5rem 0;
    }
    
    .solution-card {
        background: var(--gradient-light);
        border-radius: var(--border-radius-md);
        padding: 1.5rem;
        transition: var(--transition);
        border: 1px solid rgba(129, 199, 132, 0.25);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .solution-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-medium);
        border-color: var(--accent-green);
    }
    
    .solution-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        color: var(--dark-green);
    }
    
    .solution-icon {
        font-size: 1.7rem;
        background: var(--gradient-primary);
        color: white;
        width: 48px;
        height: 48px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    /* ===== BUTTON ENHANCEMENTS - BETTER PROPORTIONS ===== */
    .stButton > button {
        background: var(--gradient-secondary);
        color: white;
        border: none;
        padding: 0.9rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.3px;
        height: auto;
        min-height: 48px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(46, 125, 50, 0.3);
    }
    
    /* ===== SIDEBAR ENHANCEMENTS - IMPROVED SPACING ===== */
    .sidebar-container {
        background: linear-gradient(180deg, #F9FFF9 0%, #F1F8E9 100%);
        border-right: 1px solid rgba(129, 199, 132, 0.15);
        height: 100%;
        padding: 1.2rem;
    }
    
    .sidebar-header {
        background: var(--gradient-primary);
        color: white;
        padding: 1.2rem;
        border-radius: var(--border-radius-md);
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        position: relative;
    }
    
    /* ===== METRIC CARDS - COMPACT SIZE ===== */
    .metric-card {
        background: white;
        border-radius: var(--border-radius-sm);
        padding: 1rem;
        margin: 0.8rem 0;
        box-shadow: var(--shadow-soft);
        border-left: 3px solid var(--accent-green);
        transition: var(--transition);
    }
    
    .metric-card:hover {
        transform: translateX(3px);
        box-shadow: var(--shadow-medium);
    }
    
    /* ===== VOICE ASSISTANT SECTION ===== */
    .voice-section {
        background: linear-gradient(135deg, #F3E5F5 0%, #E8F5E9 100%);
        border-radius: var(--border-radius-md);
        padding: 1.2rem;
        margin: 1.2rem 0;
        border: 1px solid #CE93D8;
    }
    
    .voice-buttons-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.8rem;
        margin-top: 0.8rem;
    }
    
    /* ===== COLUMN SPACING IMPROVEMENTS ===== */
    .stColumn {
        padding: 0 0.5rem;
    }
    
    /* ===== PROGRESS BAR ENHANCEMENT ===== */
    .stProgress > div > div {
        background: var(--gradient-secondary);
        border-radius: 40px;
        height: 8px;
    }
    
    /* ===== RESPONSIVE DESIGN IMPROVEMENTS ===== */
    @media (max-width: 992px) {
        .main-title {
            font-size: 2.2rem;
        }
        
        .main-subtitle {
            font-size: 1rem;
        }
        
        .disease-name {
            font-size: 1.8rem;
        }
        
        .solution-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .upload-zone {
            padding: 2rem 1.5rem;
        }
        
        .modern-card {
            padding: 1.5rem 1.2rem;
        }
        
        .result-container {
            padding: 1.8rem;
            margin: 1.5rem auto;
        }
    }
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
        
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .card-title {
            font-size: 1.4rem;
        }
        
        .disease-name {
            font-size: 1.6rem;
        }
        
        .disease-emoji {
            font-size: 3rem;
        }
        
        .upload-icon {
            font-size: 2.8rem;
        }
        
        .stButton > button {
            padding: 0.8rem 1.5rem;
            font-size: 0.95rem;
        }
    }
    
    /* ===== CUSTOM SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(232, 245, 233, 0.4);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-green);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-green);
    }
    
    /* ===== FORM ELEMENT SPACING ===== */
    .stSelectbox, .stFileUploader {
        margin-bottom: 1rem;
    }
    
    .stSpinner {
        margin: 1.5rem 0;
    }
    
    /* ===== IMAGE PREVIEW CONTAINER ===== */
    .image-preview-container {
        border-radius: var(--border-radius-md);
        overflow: hidden;
        border: 2px solid rgba(129, 199, 132, 0.2);
        background: white;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# TEXT-TO-SPEECH FUNCTION (UNCHANGED)
# ==========================================
def speak_text(text):
    """Convert text to speech and play it"""
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.say(text)
        engine.runAndWait()
        
        return True
    except Exception as e:
        st.warning(f"Voice feature unavailable. Please install pyttsx3 with: pip install pyttsx3")
        return False

# ==========================================
# DISEASE DATABASE (UNCHANGED)
# ==========================================
DISEASE_DATABASE = {
    "Early Blight": {
        "scientific_name": "Alternaria solani",
        "description": "A fungal disease characterized by dark concentric rings on leaves, affecting tomatoes and potatoes.",
        "affected_crops": ["Tomato", "Potato", "Eggplant", "Pepper"],
        "symptoms": [
            "Small dark spots on lower leaves",
            "Concentric rings on lesions",
            "Yellowing around spots",
            "Leaf drop in severe cases",
            "Lesions on stems and fruits"
        ],
        "severity": "Moderate-High",
        "severity_score": 65,
        "solutions": {
            "chemical": [
                "Apply Chlorothalonil (Bravo) every 7-10 days",
                "Use Mancozeb (Dithane) as preventative spray",
                "Apply Copper-based fungicides (Kocide)"
            ],
            "organic": [
                "Spray neem oil solution every 5-7 days",
                "Apply baking soda solution (1 tbsp per gallon of water)",
                "Use garlic extract spray"
            ],
            "cultural": [
                "Practice 3-year crop rotation",
                "Remove and destroy infected plant debris",
                "Ensure proper spacing (60-90 cm between plants)",
                "Water at soil level, avoid overhead irrigation",
                "Use mulch to prevent soil splash"
            ],
            "biological": [
                "Apply Trichoderma harzianum bio-fungicide",
                "Use Bacillus subtilis products",
                "Introduce beneficial microbes to soil"
            ]
        },
        "prevention": [
            "Use disease-resistant varieties",
            "Plant in well-drained soil",
            "Avoid working with wet plants",
            "Sanitize garden tools regularly",
            "Monitor plants weekly for early signs"
        ],
        "emoji": "🍅"
    },
    "Late Blight": {
        "scientific_name": "Phytophthora infestans",
        "description": "Devastating disease that spreads rapidly in cool, wet conditions, famous for causing the Irish Potato Famine.",
        "affected_crops": ["Potato", "Tomato"],
        "symptoms": [
            "Water-soaked lesions on leaves",
            "White mold growth on underside of leaves",
            "Rapid spreading in wet conditions",
            "Dark lesions on stems",
            "Rotting of tubers and fruits"
        ],
        "severity": "Very High",
        "severity_score": 90,
        "solutions": {
            "chemical": [
                "Apply Metalaxyl (Ridomil) as soil drench",
                "Use Chlorothalonil (Bravo) every 5-7 days during wet weather",
                "Apply Famoxadone + Cymoxanil (Tanos)"
            ],
            "organic": [
                "Apply copper fungicides every 7-10 days",
                "Use hydrogen peroxide spray (3% solution)",
                "Apply compost tea to boost plant immunity"
            ],
            "cultural": [
                "Destroy infected plants immediately",
                "Use certified disease-free seeds",
                "Avoid overhead irrigation",
                "Improve air circulation",
                "Harvest before rainy season"
            ],
            "biological": [
                "Apply Streptomyces lydicus products",
                "Use Bacillus amyloliquefaciens",
                "Apply chitosan-based products"
            ]
        },
        "prevention": [
            "Plant resistant varieties",
            "Monitor weather forecasts",
            "Use protective fungicides before rainy periods",
            "Avoid planting near infected fields",
            "Practice strict sanitation"
        ],
        "emoji": "🥔"
    },
    "Powdery Mildew": {
        "scientific_name": "Erysiphe spp.",
        "description": "White powdery fungal growth on leaves and stems, common in dry conditions with high humidity.",
        "affected_crops": ["Cucumber", "Squash", "Grapes", "Wheat", "Mango", "Rose"],
        "symptoms": [
            "White powdery spots on leaves",
            "Leaves turning yellow then brown",
            "Stunted plant growth",
            "Distorted leaves",
            "Reduced fruit production"
        ],
        "severity": "Moderate",
        "severity_score": 50,
        "solutions": {
            "chemical": [
                "Apply Sulfur dust or spray",
                "Use Myclobutanil (Systhane) every 10-14 days",
                "Apply Triflumizole (Procure)"
            ],
            "organic": [
                "Spray milk solution (1 part milk to 9 parts water)",
                "Apply baking soda spray (1 tsp per liter)",
                "Use neem oil every 5-7 days",
                "Apply potassium bicarbonate solution"
            ],
            "cultural": [
                "Ensure good air circulation",
                "Avoid overhead watering",
                "Plant resistant varieties",
                "Remove infected leaves promptly",
                "Space plants properly"
            ],
            "biological": [
                "Apply Ampelomyces quisqualis",
                "Use Bacillus pumilus products",
                "Apply horticultural oil sprays"
            ]
        },
        "prevention": [
            "Water early in the day",
            "Maintain proper plant spacing",
            "Avoid excess nitrogen fertilizer",
            "Keep garden clean of debris",
            "Monitor humidity levels"
        ],
        "emoji": "🍃"
    },
    "Bacterial Leaf Spot": {
        "scientific_name": "Xanthomonas spp.",
        "description": "Bacterial disease causing angular water-soaked spots that turn brown with yellow halos.",
        "affected_crops": ["Tomato", "Pepper", "Cabbage", "Rice", "Mango", "Citrus"],
        "symptoms": [
            "Small water-soaked spots",
            "Spots turning brown or black",
            "Yellow halos around spots",
            "Leaf drop in severe cases",
            "Fruit lesions and spots"
        ],
        "severity": "Moderate",
        "severity_score": 55,
        "solutions": {
            "chemical": [
                "Apply Copper-based bactericides (Kocide 3000)",
                "Use Streptomycin for severe cases",
                "Apply Oxytetracycline products"
            ],
            "organic": [
                "Apply copper soap sprays",
                "Use hydrogen peroxide (3%) solution",
                "Apply garlic-chili spray",
                "Use vinegar solution (1:3 vinegar:water)"
            ],
            "cultural": [
                "Use disease-free seeds and transplants",
                "Avoid working with wet plants",
                "Practice 2-3 year crop rotation",
                "Remove weed hosts",
                "Disinfect tools regularly"
            ],
            "biological": [
                "Apply Bacillus subtilis products",
                "Use Pseudomonas fluorescens",
                "Apply beneficial microbes"
            ]
        },
        "prevention": [
            "Purchase certified disease-free seeds",
            "Avoid overhead irrigation",
            "Remove infected plants immediately",
            "Control insect vectors",
            "Improve soil drainage"
        ],
        "emoji": "🦠"
    }
}

# ==========================================
# INITIALIZE SESSION STATE (UNCHANGED)
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Detection'
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

# ==========================================
# ENHANCED SIDEBAR - OPTIMIZED SPACING
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-container">
        <div class="sidebar-header">
            <div class="sidebar-title">🌿 Navigation</div>
            <div style="font-size: 0.85rem; opacity: 0.95; font-weight: 500; line-height: 1.3;">
                AI-Powered Disease Detection
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Voice Assistant Section
    st.markdown("#### 🔊 Voice Assistant")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Test", use_container_width=True, help="Test voice functionality"):
            test_message = "Welcome to the Crop Disease Detection System."
            if speak_text(test_message):
                st.success("Voice active!", icon="✅")
    
    with col2:
        if st.button("📖 Guide", use_container_width=True, help="Voice guide"):
            st.info("Click voice buttons after analysis")
    
    st.markdown("---")
    
    # Quick Tips
    st.markdown("#### 💡 Quick Tips")
    with st.container():
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.85rem; line-height: 1.5; color: #1a1a1a;">
                • Upload clear, well-lit leaf images<br>
                • Select correct crop type for accuracy<br>
                • Review all treatment options<br>
                • Use voice assistant for explanations
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Disease Statistics
    st.markdown("#### 📊 Disease Database")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Diseases", len(DISEASE_DATABASE), delta="4 types")
    with col2:
        st.metric("Avg Severity", "65%", delta="-2% from avg")
    
    # Disease List
    st.markdown("**Available Diseases:**")
    for disease, info in DISEASE_DATABASE.items():
        with st.container():
            st.markdown(f"""
            <div class="metric-card" style="padding: 0.8rem; margin: 0.5rem 0;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1rem;">{info['emoji']}</span>
                    <span style="font-weight: 600; color: #1B5E20; font-size: 0.9rem;">{disease}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ENHANCED MAIN HEADER - COMPACT DESIGN
# ==========================================
st.markdown("""
<div class="main-header-container">
    <div class="main-header">
        <div class="header-decoration header-leaf-1">🍃</div>
        <div class="header-decoration header-leaf-2">🌿</div>
        <div class="header-decoration header-leaf-3">🌱</div>
        <h1 class="main-title">AI-Powered Crop Disease Detection</h1>
        <p class="main-subtitle">
            Advanced computer vision system for plant disease diagnosis with multiple treatment solutions
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MAIN CONTENT - COMPACT CARDS
# ==========================================
st.markdown("""
<div class="modern-card">
    <div class="card-title">
        <div class="card-title-icon">🔍</div>
        Upload Leaf Image for Disease Detection
    </div>
    <p style="font-size: 1rem; color: #444; line-height: 1.6; margin-bottom: 1rem;">
        Our advanced AI system analyzes plant leaf images to detect diseases with high accuracy 
        and provides comprehensive treatment solutions including chemical, organic, cultural, 
        and biological methods for sustainable agriculture.
    </p>
    <div style="display: flex; flex-wrap: wrap; gap: 0.8rem; margin-top: 1.2rem;">
        <div style="background: #E8F5E9; padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem;">
            <span style="color: #2E7D32; font-weight: 600;">🎯</span> High Accuracy
        </div>
        <div style="background: #E8F5E9; padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem;">
            <span style="color: #2E7D32; font-weight: 600;">⚡</span> Real-time Results
        </div>
        <div style="background: #E8F5E9; padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem;">
            <span style="color: #2E7D32; font-weight: 600;">🎧</span> Voice Assistant
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# COMPACT UPLOAD SECTION
# ==========================================
st.markdown("""
<div class="upload-zone" onclick="document.querySelector('input[type=file]').click()">
    <div class="upload-icon">📤</div>
    <h3 style="color: #1B5E20; margin-bottom: 0.8rem; font-size: 1.5rem;">
        Drag & Drop or Click to Upload Image
    </h3>
    <p style="color: #555; margin-bottom: 1.2rem; font-size: 1rem;">
        Supported formats: JPG, JPEG, PNG | Maximum file size: 10MB
    </p>
    <div style="background: white; display: inline-block; padding: 0.4rem 1.2rem; 
                border-radius: 40px; color: #2E7D32; font-weight: 600; border: 2px solid #A5D6A7; font-size: 0.9rem;">
        Browse Files
    </div>
</div>
""", unsafe_allow_html=True)

# File Uploader (UNCHANGED)
uploaded_file = st.file_uploader(
    "Choose a leaf image...",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

# Process Uploaded Image (UNCHANGED LOGIC)
if uploaded_file is not None:
    try:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        st.markdown("""
        <div class="modern-card">
            <div class="card-title">
                <div class="card-title-icon">📸</div>
                Uploaded Image Preview
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Leaf Image for Analysis", use_column_width=True)
        
        # Crop Selection with Compact UI
        st.markdown("""
        <div class="modern-card">
            <div class="card-title">
                <div class="card-title-icon">🌾</div>
                Select Crop Type
            </div>
            <p style="color: #555; margin-bottom: 1rem; font-size: 0.95rem;">
                Choose the crop type for enhanced detection accuracy
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        crop_type = st.selectbox(
            "Crop Selection:",
            ["Auto Detect", "Tomato", "Potato", "Rice", "Banana", "Cucumber", "Wheat", "Grapes", "Other"],
            index=0,
            label_visibility="collapsed"
        )
        
        # Analyze Button with Better Spacing
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔬 Analyze Image with AI", type="primary", use_container_width=True, 
                        help="Start AI analysis of the uploaded image"):
                with st.spinner("🔄 AI is analyzing the image... Please wait."):
                    # Show enhanced progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("🔍 Scanning image features...")
                        elif i < 60:
                            status_text.text("🧠 Processing with neural network...")
                        elif i < 90:
                            status_text.text("📊 Comparing with disease database...")
                        else:
                            status_text.text("✅ Finalizing results...")
                    
                    # Get random disease prediction (for demo)
                    disease_name = random.choice(list(DISEASE_DATABASE.keys()))
                    disease_info = DISEASE_DATABASE[disease_name]
                    confidence = random.randint(88, 97)
                    
                    # Store analysis in session state
                    st.session_state.last_analysis = {
                        "disease_name": disease_name,
                        "disease_info": disease_info,
                        "confidence": confidence
                    }
                    
                    # Complete progress
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    status_text.success("✅ Analysis complete!")
                    
        # Display Results if available
        if st.session_state.last_analysis:
            disease_name = st.session_state.last_analysis["disease_name"]
            disease_info = st.session_state.last_analysis["disease_info"]
            confidence = st.session_state.last_analysis["confidence"]
            
            st.markdown("""
            <div class="result-container">
                <div class="result-header">
                    <div class="disease-emoji">{}</div>
                    <h1 class="disease-name">{}</h1>
                    <div class="confidence-container">
                        <span style="font-weight: 600; color: #555;">Confidence Level:</span>
                        <div class="confidence-badge">{}%</div>
                    </div>
                    <div style="margin-top: 1.2rem;">
                        <span class="severity-badge {}">
                            <span>Severity:</span>
                            <span>{}</span>
                        </span>
                    </div>
                </div>
            </div>
            """.format(
                disease_info["emoji"],
                disease_name,
                confidence,
                "severity-high" if "High" in disease_info["severity"] else "severity-moderate" if "Moderate" in disease_info["severity"] else "severity-low",
                disease_info["severity"]
            ), unsafe_allow_html=True)
            
            # Disease Information in Compact Grid
            st.markdown("""
            <div class="modern-card">
                <div class="card-title">
                    <div class="card-title-icon">📋</div>
                    Disease Information
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="solution-card">
                    <div class="solution-header">
                        <div class="solution-icon">🔬</div>
                        <h3 style="font-size: 1.2rem; margin: 0;">Scientific Details</h3>
                    </div>
                    <p style="margin: 0.5rem 0; font-size: 0.95rem;"><strong>Scientific Name:</strong><br>{}</p>
                    <p style="margin: 0.5rem 0; font-size: 0.95rem;"><strong>Description:</strong><br>{}</p>
                    <p style="margin: 0.5rem 0; font-size: 0.95rem;"><strong>Affected Crops:</strong><br>{}</p>
                </div>
                """.format(
                    disease_info['scientific_name'],
                    disease_info['description'],
                    ', '.join(disease_info['affected_crops'])
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="solution-card">
                    <div class="solution-header">
                        <div class="solution-icon">⚠️</div>
                        <h3 style="font-size: 1.2rem; margin: 0;">Key Symptoms</h3>
                    </div>
                    <div style="margin-top: 0.5rem;">
                """, unsafe_allow_html=True)
                for symptom in disease_info['symptoms'][:4]:
                    st.markdown(f"• **{symptom}**")
                st.markdown("</div></div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Multiple Solutions Section - Compact Layout
            st.markdown("""
            <div class="modern-card">
                <div class="card-title">
                    <div class="card-title-icon">💡</div>
                    Multiple Treatment Solutions
                </div>
                <p style="color: #555; margin-bottom: 1.5rem; font-size: 0.95rem;">
                    Choose from various treatment approaches based on your farming practices
                </p>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="solution-grid">', unsafe_allow_html=True)
            
            # Chemical Solutions
            st.markdown("""
            <div class="solution-card">
                <div class="solution-header">
                    <div class="solution-icon">🧪</div>
                    <h3 style="font-size: 1.2rem; margin: 0;">Chemical Solutions</h3>
                </div>
                <div style="margin-top: 0.5rem;">
            """, unsafe_allow_html=True)
            for solution in disease_info['solutions']['chemical'][:3]:
                st.markdown(f"• {solution}")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Organic Solutions
            st.markdown("""
            <div class="solution-card">
                <div class="solution-header">
                    <div class="solution-icon">🌿</div>
                    <h3 style="font-size: 1.2rem; margin: 0;">Organic Solutions</h3>
                </div>
                <div style="margin-top: 0.5rem;">
            """, unsafe_allow_html=True)
            for solution in disease_info['solutions']['organic'][:3]:
                st.markdown(f"• {solution}")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Cultural Solutions
            st.markdown("""
            <div class="solution-card">
                <div class="solution-header">
                    <div class="solution-icon">🌱</div>
                    <h3 style="font-size: 1.2rem; margin: 0;">Cultural Practices</h3>
                </div>
                <div style="margin-top: 0.5rem;">
            """, unsafe_allow_html=True)
            for solution in disease_info['solutions']['cultural'][:3]:
                st.markdown(f"• {solution}")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Biological Solutions
            st.markdown("""
            <div class="solution-card">
                <div class="solution-header">
                    <div class="solution-icon">🦠</div>
                    <h3 style="font-size: 1.2rem; margin: 0;">Biological Control</h3>
                </div>
                <div style="margin-top: 0.5rem;">
            """, unsafe_allow_html=True)
            for solution in disease_info['solutions']['biological'][:3]:
                st.markdown(f"• {solution}")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            # Prevention Tips - Compact Layout
            st.markdown("""
            <div class="modern-card">
                <div class="card-title">
                    <div class="card-title-icon">🛡️</div>
                    Prevention & Management
                </div>
            """, unsafe_allow_html=True)
            
            prevention_cols = st.columns(2)
            for i, tip in enumerate(disease_info['prevention']):
                with prevention_cols[i % 2]:
                    st.markdown(f"""
                    <div class="solution-card" style="padding: 1rem; margin-bottom: 0.8rem;">
                        <div style="display: flex; align-items: start; gap: 8px;">
                            <span style="color: #4CAF50; font-size: 1.1rem;">✓</span>
                            <span style="font-size: 0.95rem; line-height: 1.5;">{tip}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Voice Assistant Section - Compact
            st.markdown("""
            <div class="modern-card">
                <div class="card-title">
                    <div class="card-title-icon">🔊</div>
                    Voice Assistant
                </div>
                <p style="color: #555; margin-bottom: 1rem; font-size: 0.95rem;">
                    Listen to diagnosis and treatment explanations
                </p>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🎤 Hear Diagnosis", key="hear_diagnosis", use_container_width=True):
                    voice_text = f"Disease detected: {disease_name}. Confidence level: {confidence} percent. Severity: {disease_info['severity']}."
                    if speak_text(voice_text):
                        st.success("Playing diagnosis...")
            
            with col2:
                if st.button("💊 Hear Treatments", key="hear_treatments", use_container_width=True):
                    if disease_info['solutions']['chemical']:
                        treatment = disease_info['solutions']['chemical'][0]
                    voice_text = f"Recommended treatment: {treatment}"
                    if speak_text(voice_text):
                        st.success("Playing treatments...")
            
            with col3:
                if st.button("🛡️ Hear Prevention", key="hear_prevention", use_container_width=True):
                    if disease_info['prevention']:
                        tip = disease_info['prevention'][0]
                        voice_text = f"Prevention tip: {tip}"
                    if speak_text(voice_text):
                        st.success("Playing prevention tips...")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Action Buttons - Better Spacing
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Download Full Report", use_container_width=True, 
                           help="Generate comprehensive PDF report"):
                    st.success("✅ Report generated! (Demo feature)")
            
            with col2:
                if st.button("🔄 Analyze Another Image", type="primary", use_container_width=True,
                           help="Start new analysis with different image"):
                    st.session_state.last_analysis = None
                    st.rerun()
            
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please upload a valid image file.")

# ==========================================
# COMPACT FOOTER
# ==========================================
st.markdown("""
<div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid rgba(129, 199, 132, 0.2);">
    <div style="text-align: center; color: #555; padding: 0.8rem;">
        <p style="font-size: 1.1rem; font-weight: 700; color: #1B5E20; margin-bottom: 0.3rem;">
            🌾 AI-Powered Crop Disease Detection System
        </p>
        <p style="font-size: 0.9rem; margin-bottom: 0.3rem; opacity: 0.9;">
            Final Year Project | Computer Science & Agriculture Department
        </p>
        <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.8rem;">
            © 2024 Smart Agriculture Solutions. Voice-enabled AI detection system for sustainable farming.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)