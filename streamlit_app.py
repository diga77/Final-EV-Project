import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import os
from openai import OpenAI
import json
from AIapi import EVAIAssistant
from dotenv import load_dotenv

load_dotenv()


# PAGE CONFIGURATION
st.set_page_config(
    page_title="EV Range Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "AI-powered Electric Vehicle Range Prediction System"}
)

# Professional Enhanced UI Styling
st.markdown("""
<style>
    :root {
        --primary-color: #1a73e8;
        --secondary-color: #34a853;
        --accent-color: #fbbc04;
        --dark-bg: #0f1419;
        --light-text: #ffffff;
    }
    
    .main {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        color: #ffffff;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #1a73e8 0%, #0f5cc0 100%);
        color: white;
        border-radius: 6px;
        padding: 10px 24px;
        border: none;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0f5cc0 0%, #0847a6 100%);
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.4);
        transform: translateY(-2px);
    }
    
    .result-box {
        border-left: 5px solid #34a853;
        background: linear-gradient(90deg, rgba(52, 168, 83, 0.1) 0%, rgba(52, 168, 83, 0.05) 100%);
        color: #34a853;
        padding: 16px;
        border-radius: 8px;
        margin-top: 16px;
        font-size: 18px;
        font-weight: 600;
    }
    
    .info-box {
        border-left: 5px solid #1a73e8;
        background: linear-gradient(90deg, rgba(26, 115, 232, 0.1) 0%, rgba(26, 115, 232, 0.05) 100%);
        color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        margin-top: 12px;
    }
    
    .ai-insight-box {
        border-left: 5px solid #fbbc04;
        background: linear-gradient(90deg, rgba(251, 188, 4, 0.1) 0%, rgba(251, 188, 4, 0.05) 100%);
        color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        margin-top: 12px;
    }
    
    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 16px;
        color: #1a73e8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .subsection-title {
        font-size: 16px;
        font-weight: 600;
        color: #34a853;
        margin-top: 12px;
    }
    
    .stSelectbox, .stNumberInput, .stTextInput {
        margin-bottom: 12px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(26, 115, 232, 0.15) 0%, rgba(52, 168, 83, 0.15) 100%);
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
    }
    
    .header-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(90deg, #1a73e8 0%, #34a853 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# INITIALIZE AI CLIENT
@st.cache_resource
def get_ai_client():
    api_key = os.getenv("HF_TOK")
    if not api_key:
        raise ValueError("HuggingFace API key not found. Please set HF_TOKEN in environment variables.")
    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key,
    )

# GET AI INSIGHTS
@st.cache_data
def get_ai_insights(vehicle_info, predicted_range):
    """Get AI-powered insights about the vehicle and range"""
    try:
        client = get_ai_client()
        prompt = f"""You are an expert electric vehicle consultant. Provide a brief, professional insight about this vehicle's range prediction.

Vehicle Details:
- Make: {vehicle_info.get('Make', 'Unknown')}
- Model: {vehicle_info.get('Model', 'Unknown')}
- Year: {vehicle_info.get('Model Year', 'Unknown')}
- Type: {vehicle_info.get('Electric Vehicle Type', 'Unknown')}
- Price: ${vehicle_info.get('Base MSRP', 0):,.0f}
- Predicted Range: {predicted_range:.1f} miles

Provide a 2-3 sentence professional insight about:
1. Whether this range is competitive for this vehicle class
2. Real-world usage recommendations
Keep it concise and user-friendly."""

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2-Exp:novita",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI insights unavailable: {str(e)[:50]}..."

# LOAD MODEL
model_path = Path("ev_range_model.joblib")

if not model_path.exists():
    st.error("❌ Model file not found. Please train the model first.")
    st.stop()

model = joblib.load(model_path)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# HEADER SECTION
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="header-title">⚡ EV Range Predictor</div>', unsafe_allow_html=True)
    st.write("**Advanced AI-Powered Electric Vehicle Range Estimation System**")
with col2:
    st.metric("Model Status", "✅ Ready", delta="Active")

st.markdown("---")

# SIDEBAR INFORMATION
with st.sidebar:
    st.markdown("### 📊 About This Tool")
    st.info("""
    This professional application uses machine learning to predict electric vehicle driving ranges based on:
    - Vehicle specifications
    - Model year and pricing
    - Vehicle type (BEV/PHEV)
    - Geographic location
    """)
    
    st.markdown("### ⚙️ Model Information")
    st.write("**Model Type:** Gradient Boosting Regressor")
    st.write("**Task:** Range Prediction (Miles)")
    st.write("**Status:** Trained and Deployed")

# PRESET EXAMPLES
presets = {
    "Select Example (Optional)": {},
    "🚗 Tesla Model 3 (2022)": {
        "Make": "Tesla", "Model": "Model 3", "Model Year": 2022,
        "Electric Vehicle Type": "BEV", "Base MSRP": 46990, "State": "CA"
    },
    "🚙 Tata Nexon EV (2021)": {
        "Make": "Tata", "Model": "Nexon EV", "Model Year": 2021,
        "Electric Vehicle Type": "BEV", "Base MSRP": 18500, "State": "MH"
    },
    "🏎️ Hyundai Kona Electric (2023)": {
        "Make": "Hyundai", "Model": "Kona Electric", "Model Year": 2023,
        "Electric Vehicle Type": "BEV", "Base MSRP": 37400, "State": "WA"
    },
    "🔋 MG ZS EV (2022)": {
        "Make": "MG", "Model": "ZS EV", "Model Year": 2022,
        "Electric Vehicle Type": "BEV", "Base MSRP": 26900, "State": "DL"
    },
    "⚡ Nissan Leaf (2020)": {
        "Make": "Nissan", "Model": "Leaf", "Model Year": 2020,
        "Electric Vehicle Type": "BEV", "Base MSRP": 31999, "State": "NY"
    }
}

st.markdown('<div class="section-title">🎯 Vehicle Specifications</div>', unsafe_allow_html=True)

preset_choice = st.selectbox("Choose Preset Example or Enter Custom Details", list(presets.keys()))
preset = presets[preset_choice] if preset_choice != "Select Example (Optional)" else {}

# INPUT COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="subsection-title">Basic Information</div>', unsafe_allow_html=True)
    make = st.text_input("Manufacturer", value=preset.get("Make", ""), placeholder="e.g., Tesla")
    year = st.number_input("Model Year", min_value=1995, max_value=2035,
                           value=preset.get("Model Year", 2023))

with col2:
    st.markdown('<div class="subsection-title">Model Details</div>', unsafe_allow_html=True)
    model_name = st.text_input("Model Name", value=preset.get("Model", ""), placeholder="e.g., Model 3")
    ev_type = st.selectbox("Vehicle Type", ["BEV", "PHEV"],
                           index=["BEV", "PHEV"].index(preset.get("Electric Vehicle Type", "BEV")))

with col3:
    st.markdown('<div class="subsection-title">Pricing & Location</div>', unsafe_allow_html=True)
    msrp = st.number_input("Base MSRP ($)", min_value=1000, max_value=200000,
                           value=preset.get("Base MSRP", 45000), step=1000)
    state = st.text_input("State/Region", value=preset.get("State", ""), placeholder="e.g., CA")

# PREDICTION SECTION
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-title">🚀 Prediction Engine</div>', unsafe_allow_html=True)

with col2:
    predict_button = st.button("Predict Range", use_container_width=True)

if predict_button:
    # Validation
    if not all([make, model_name, state]):
        st.error("⚠️ Please fill in all required fields: Make, Model, and State")
    else:
        with st.spinner("⏳ Analyzing vehicle data and generating prediction..."):
            # Create input dataframe
            input_df = pd.DataFrame([{
                "Model Year": year,
                "Base MSRP": msrp,
                "Make": make,
                "Model": model_name,
                "Electric Vehicle Type": ev_type,
                "State": state
            }])

            # Make prediction
            predicted_range = model.predict(input_df)[0]
            
            # Display results
            st.markdown('<div class="result-box">⚡ ESTIMATED DRIVING RANGE: ' + 
                       f'{predicted_range:.1f} MILES</div>', unsafe_allow_html=True)
            
            # Display vehicle summary
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            with summary_col1:
                st.metric("Make", make)
            with summary_col2:
                st.metric("Model Year", year)
            with summary_col3:
                st.metric("Vehicle Type", ev_type)
            with summary_col4:
                st.metric("Base Price", f"${msrp:,.0f}")
            
            # AI INSIGHTS
            st.markdown('<div class="section-title">💡 AI Insights</div>', unsafe_allow_html=True)
            
            vehicle_info = {
                "Make": make,
                "Model": model_name,
                "Model Year": year,
                "Electric Vehicle Type": ev_type,
                "Base MSRP": msrp,
                "State": state
            }
            
            ai_insight = get_ai_insights(vehicle_info, predicted_range)
            st.markdown(f'<div class="ai-insight-box">{ai_insight}</div>', 
                       unsafe_allow_html=True)
            
            # RANGE ANALYSIS
            st.markdown('<div class="section-title">📈 Range Analysis</div>', unsafe_allow_html=True)
            
            analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
            
            with analysis_col1:
                st.markdown("**Daily Commute Capability**")
                daily_miles = predicted_range / 2
                st.write(f"Typical days on single charge: {daily_miles:.0f} miles")
            
            with analysis_col2:
                st.markdown("**Weekly Range**")
                weekly_miles = predicted_range * 5
                st.write(f"Weekly driving potential: {weekly_miles:.0f} miles")
            
            with analysis_col3:
                st.markdown("**Cost per Mile**")
                cost_per_mile = msrp / (predicted_range * 50)
                st.write(f"Infrastructure cost: ${cost_per_mile:.2f}/mile")
            
            # IMPORTANT NOTES
            st.markdown('<div class="section-title">📝 Important Considerations</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
            <b>⚠️ Range Variance Factors:</b>
            
            The estimated range can vary by ±15-25% based on:
            • **Temperature:** Cold weather reduces range by 20-40%
            • **Driving Style:** Aggressive acceleration decreases efficiency
            • **Terrain:** Highways are more efficient than city driving
            • **Accessories:** Heating, cooling, and lights impact range
            • **Battery Age:** Degradation occurs over charging cycles
            • **Road Conditions:** Traffic, wind, and elevation affect consumption
            
            <b>💡 Recommendations:</b>
            • Plan long trips with charging stations in mind
            • Precondition battery before departure in cold weather
            • Monitor battery health regularly
            • Use eco-driving modes for maximum range
            </div>
            """, unsafe_allow_html=True)

# FOOTER
st.markdown("---")
# -------------------- Chat Assistant --------------------
st.markdown('<div class="section-title">💬 Chat with EV Assistant</div>', unsafe_allow_html=True)
with st.expander("Ask the AI Assistant a question about EVs, charging, or this prediction", expanded=False):
    # Chat input and send
    user_question = st.text_input("Your question", key="chat_input", placeholder="E.g., How far can I drive in cold weather with this vehicle?")
    send = st.button("Send", key="send_chat")

    if send and user_question:
        assistant = EVAIAssistant()
        with st.spinner("Getting answer from AI..."):
            try:
                answer = assistant.answer_ev_question(user_question)
            except Exception as e:
                answer = f"AI error: {str(e)[:200]}"

        # Append to chat history and display
        st.session_state['chat_history'].append(("You", user_question))
        st.session_state['chat_history'].append(("Assistant", answer))

    # Display chat history
    if st.session_state['chat_history']:
        for role, msg in st.session_state['chat_history']:
            if role == 'You':
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Assistant:** {msg}")

st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">
    <p>For accurate range estimates, refer to manufacturer specifications | Data may vary by region</p>
</div>
""", unsafe_allow_html=True)
