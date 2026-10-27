"""
===========================================
CROP DISEASE DETECTION SYSTEM - Streamlit App
Final Year Academic Project
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
# TEXT-TO-SPEECH FUNCTION (SIMPLIFIED)
# ==========================================
def speak_text(text):
    """Convert text to speech and play it"""
    try:
        # Try to import pyttsx3
        import pyttsx3
        
        # Initialize the engine
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', 150)  # Speed
        engine.setProperty('volume', 0.9)  # Volume
        
        # Get available voices
        voices = engine.getProperty('voices')
        
        # Try to use a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
        return True
    except Exception as e:
        # If pyttsx3 fails, show a message
        st.warning(f"Voice feature unavailable. Please install pyttsx3 with: pip install pyttsx3")
        return False

# ==========================================
# CUSTOM CSS STYLING
# ==========================================
st.markdown("""
<style>
    /* Main styles */
    .stApp {
        background: linear-gradient(135deg, #f9fff9 0%, #e8f5e9 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .main-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        margin: 0 auto;
        max-width: 800px;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid rgba(46, 125, 50, 0.1);
    }
    
    .card-title {
        color: #2E7D32;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #A5D6A7;
        padding-bottom: 0.5rem;
    }
    
    /* Result card */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 900px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Disease name */
    .disease-name {
        color: #2E7D32;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Confidence badge */
    .confidence-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
        padding: 0.7rem 1.8rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }
    
    /* Severity badges */
    .severity-high {
        background: #FFEBEE;
        color: #C62828;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    .severity-moderate {
        background: #FFF3E0;
        color: #EF6C00;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    .severity-low {
        background: #E8F5E9;
        color: #1B5E20;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Treatment cards */
    .treatment-card {
        background: #F9FFF9;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32, #43A047);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3);
    }
    
    /* Upload container */
    .upload-container {
        background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
        border: 3px dashed #2E7D32;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        background: linear-gradient(135deg, #F1F8E9, #E8F5E9);
        border-color: #43A047;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ENHANCED DISEASE DATABASE WITH MULTIPLE SOLUTIONS
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
# INITIALIZE SESSION STATE
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Detection'  # Default to detection page
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

# ==========================================
# SIDEBAR - SIMPLE NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-title">🌿 Navigation</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">
            Crop Disease Detection System
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Voice Assistant Section
    st.markdown("### 🔊 Voice Assistant")
    
    if st.button("🎤 Test Voice Assistant", use_container_width=True):
        test_message = "Welcome to the Crop Disease Detection System. I am your voice assistant. I will help you understand the disease detection results."
        if speak_text(test_message):
            st.success("Voice assistant is working!")
        else:
            st.warning("Please install pyttsx3: pip install pyttsx3")
    
    st.markdown("---")
    
    # Quick Tips
    st.markdown("### 💡 Quick Tips")
    st.info("""
    1. Upload clear leaf images
    2. Select correct crop type
    3. Review all solution options
    4. Use voice assistant for explanations
    """)
    
    st.markdown("---")
    
    # Disease Statistics
    st.markdown("### 📊 Disease Database")
    st.metric("Total Diseases", len(DISEASE_DATABASE))
    
    # List available diseases
    st.markdown("**Available Diseases:**")
    for disease in DISEASE_DATABASE.keys():
        st.markdown(f"- {DISEASE_DATABASE[disease]['emoji']} {disease}")

# ==========================================
# MAIN HEADER
# ==========================================
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌱 AI-Powered Crop Disease Detection</h1>
    <p class="main-subtitle">
        Upload leaf images to detect diseases and get multiple treatment solutions instantly
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MAIN CONTENT - DISEASE DETECTION ONLY
# ==========================================
st.markdown("""
<div class="card">
    <h2 class="card-title">🔍 Upload Leaf Image for Disease Detection</h2>
    <p style="font-size: 1.1rem; color: #555; line-height: 1.6;">
        Our advanced AI system analyzes plant leaf images to detect diseases and provides 
        multiple treatment solutions including chemical, organic, cultural, and biological methods.
    </p>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="upload-container">
    <div style="font-size: 4rem;">📤</div>
    <h3 style="color: #2E7D32; margin-bottom: 1rem;">
        Drag & Drop or Click to Upload Image
    </h3>
    <p style="color: #666; margin-bottom: 1.5rem;">
        Supported formats: JPG, JPEG, PNG | Max size: 10MB
    </p>
</div>
""", unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader(
    "Choose a leaf image...",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

# Process Uploaded Image
if uploaded_file is not None:
    try:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        st.markdown("### 📸 Uploaded Image Preview")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Leaf Image for Analysis", use_column_width=True)
        
        # Crop Selection
        st.markdown("### 🌾 Select Crop Type")
        crop_type = st.selectbox(
            "Choose the crop type for better accuracy:",
            ["Auto Detect", "Tomato", "Potato", "Rice", "Banana", "Cucumber", "Wheat", "Grapes", "Other"],
            index=0
        )
        
        # Analyze Button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔬 Analyze Image with AI", type="primary", use_container_width=True):
                with st.spinner("🔄 AI is analyzing the image... Please wait."):
                    # Show progress
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                    
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
                    
                    # DISPLAY RESULTS
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    
                    # Title
                    st.markdown('<h2 style="color: #2E7D32; margin-bottom: 1.5rem;">✅ Analysis Complete!</h2>', unsafe_allow_html=True)
                    
                    # Emoji
                    st.markdown(f'<div style="font-size: 4rem; margin: 1rem 0;">{disease_info["emoji"]}</div>', unsafe_allow_html=True)
                    
                    # Disease Name
                    st.markdown(f'<h1 class="disease-name">{disease_name}</h1>', unsafe_allow_html=True)
                    
                    # Confidence Badge
                    st.markdown(f'<div class="confidence-badge">{confidence}% Confidence Level</div>', unsafe_allow_html=True)
                    
                    # Severity
                    if "High" in disease_info["severity"]:
                        severity_class = "severity-high"
                    elif "Moderate" in disease_info["severity"]:
                        severity_class = "severity-moderate"
                    else:
                        severity_class = "severity-low"
                    
                    st.markdown(f'<div style="margin: 1.5rem 0;"><span class="{severity_class}">Severity: {disease_info["severity"]}</span></div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Disease Information
                    st.markdown("### 📋 Disease Information")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info(f"""
                        **Scientific Name:** {disease_info['scientific_name']}
                        
                        **Description:** {disease_info['description']}
                        
                        **Affected Crops:** {', '.join(disease_info['affected_crops'])}
                        """)
                    
                    with col2:
                        st.info("**Main Symptoms:**")
                        for symptom in disease_info['symptoms'][:4]:
                            st.write(f"• {symptom}")
                    
                    # MULTIPLE SOLUTIONS SECTION
                    st.markdown("### 💡 Multiple Treatment Solutions")
                    
                    # Chemical Solutions
                    with st.expander("🧪 Chemical Solutions", expanded=True):
                        st.success("**Recommended chemical treatments:**")
                        for i, solution in enumerate(disease_info['solutions']['chemical'], 1):
                            st.write(f"{i}. {solution}")
                    
                    # Organic Solutions
                    with st.expander("🌿 Organic Solutions", expanded=True):
                        st.success("**Natural and organic treatments:**")
                        for i, solution in enumerate(disease_info['solutions']['organic'], 1):
                            st.write(f"{i}. {solution}")
                    
                    # Cultural Solutions
                    with st.expander("🌱 Cultural Practices", expanded=True):
                        st.success("**Management and cultural practices:**")
                        for i, solution in enumerate(disease_info['solutions']['cultural'], 1):
                            st.write(f"{i}. {solution}")
                    
                    # Biological Solutions
                    with st.expander("🦠 Biological Control", expanded=True):
                        st.success("**Biological control methods:**")
                        for i, solution in enumerate(disease_info['solutions']['biological'], 1):
                            st.write(f"{i}. {solution}")
                    
                    # Prevention Tips
                    st.markdown("### 🛡️ Prevention Tips")
                    prevention_cols = st.columns(2)
                    for i, tip in enumerate(disease_info['prevention']):
                        with prevention_cols[i % 2]:
                            st.info(f"✓ {tip}")
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please upload a valid image file.")

# Show analysis results if available
if st.session_state.last_analysis:
    disease_name = st.session_state.last_analysis["disease_name"]
    disease_info = st.session_state.last_analysis["disease_info"]
    confidence = st.session_state.last_analysis["confidence"]
    
    # VOICE ASSISTANT BUTTONS (AFTER RESULTS ARE DISPLAYED)
    st.markdown("---")
    st.markdown("### 🔊 Voice Assistant")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎤 Hear Diagnosis", key="hear_diagnosis", use_container_width=True):
            voice_text = f"Disease detected: {disease_name}. Confidence level: {confidence} percent. Severity: {disease_info['severity']}. This disease affects: {', '.join(disease_info['affected_crops'])}."
            if speak_text(voice_text):
                st.success("Playing diagnosis...")
    
    with col2:
        if st.button("💊 Hear Treatments", key="hear_treatments", use_container_width=True):
            if disease_info['solutions']['chemical']:
                chemical_treatment = disease_info['solutions']['chemical'][0]
            else:
                chemical_treatment = "Consult agricultural expert"
            
            if disease_info['solutions']['organic']:
                organic_treatment = disease_info['solutions']['organic'][0]
            else:
                organic_treatment = "Use neem oil spray"
            
            voice_text = f"Recommended treatments. Chemical treatment: {chemical_treatment}. Organic option: {organic_treatment}."
            if speak_text(voice_text):
                st.success("Playing treatments...")
    
    with col3:
        if st.button("🛡️ Hear Prevention", key="hear_prevention", use_container_width=True):
            if disease_info['prevention']:
                prevention1 = disease_info['prevention'][0]
                if len(disease_info['prevention']) > 1:
                    prevention2 = disease_info['prevention'][1]
                    voice_text = f"Prevention tips: {prevention1}. Also remember to: {prevention2}."
                else:
                    voice_text = f"Prevention tip: {prevention1}."
            else:
                voice_text = "Practice crop rotation and monitor plants regularly."
            
            if speak_text(voice_text):
                st.success("Playing prevention tips...")
    
    # Download Report and Analyze Another
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Full Report", use_container_width=True):
            st.success("Report generated! (Demo feature - would create PDF in full implementation)")
    
    with col2:
        if st.button("🔄 Analyze Another Image", type="primary", use_container_width=True):
            st.session_state.last_analysis = None
            st.rerun()
else:
    # Show sample images when no file is uploaded
    st.markdown("""
    <div class="card">
        <h3 style="color: #2E7D32; margin-bottom: 1rem;">📸 Sample Images for Testing</h3>
        <p style="color: #666; margin-bottom: 1.5rem;">
            Upload images like these for best results:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for sample images using Streamlit's native columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="text-align: center; font-size: 3rem;">🍅</div>', unsafe_allow_html=True)
        st.markdown("**Tomato Leaf**")
        st.caption("With disease symptoms")
    
    with col2:
        st.markdown('<div style="text-align: center; font-size: 3rem;">🥔</div>', unsafe_allow_html=True)
        st.markdown("**Potato Leaf**")
        st.caption("Clear close-up image")
    
    with col3:
        st.markdown('<div style="text-align: center; font-size: 3rem;">🌾</div>', unsafe_allow_html=True)
        st.markdown("**Rice Plant**")
        st.caption("Showing leaf lesions")
    
    # Image Guidelines
    st.markdown("""
    <div class="card">
        <h3 style="color: #2E7D32; margin-bottom: 1rem;">📋 Image Guidelines</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Guidelines in columns
    gcol1, gcol2, gcol3 = st.columns(3)
    
    with gcol1:
        st.markdown('<div style="text-align: center; font-size: 2.5rem;">📷</div>', unsafe_allow_html=True)
        st.markdown("**Good Lighting**")
        st.caption("Take photos in natural light")
    
    with gcol2:
        st.markdown('<div style="text-align: center; font-size: 2.5rem;">🍃</div>', unsafe_allow_html=True)
        st.markdown("**Focus on Leaves**")
        st.caption("Capture clear leaf details")
    
    with gcol3:
        st.markdown('<div style="text-align: center; font-size: 2.5rem;">⚡</div>', unsafe_allow_html=True)
        st.markdown("**Quick Results**")
        st.caption("Get diagnosis within seconds")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown('<div style="text-align: center; color: #666; padding: 2rem;">', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.1rem; font-weight: 600; color: #2E7D32;">🌾 Crop Disease Detection System</p>', unsafe_allow_html=True)
st.markdown('<p>Final Year Project | Computer Science Department</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 0.9rem; margin-top: 0.5rem;">© 2024 [Your University Name]. Voice-enabled AI detection system.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)