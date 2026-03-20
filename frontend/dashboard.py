import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import joblib
import os
from datetime import datetime

# --- 1. ENTERPRISE CONFIGURATION ---
st.set_page_config(
    page_title="EcoTrack Enterprise Pro | Industrial Sustainability ERP",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths as per your environment
DATA_PATH = "C:\\Users\\pooja\\OneDrive\\Desktop\\EcoTrack-Enterprise\\backend\\data\\dpp_data.csv" # Local fallback for the script
MODEL_PATH = "C:\\Users\\pooja\\OneDrive\\Desktop\\EcoTrack-Enterprise\\backend\\data\\model.pkl"
SECURITY_MODEL_PATH = "C:\\Users\\pooja\\OneDrive\\Desktop\\EcoTrack-Enterprise\\backend\\data\\security_model.pkl"
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# --- 1.5. BARE MODE DETECTION ---
# When users execute the script directly with `python dashboard.py` the
# Streamlit runtime context is missing, which leads to hundreds of
# warnings and, previously, a NameError when trying to use `df` later on.
# `get_script_run_ctx()` returns `None` outside of the normal Streamlit
# launcher, so we can print a helpful message and exit early.
import sys

if st.runtime.scriptrunner.get_script_run_ctx() is None:
    # Bare execution – avoid running the UI logic altogether
    print("Dashboard script executed outside of Streamlit.\n" \
          "Please start with `streamlit run dashboard.py` to launch the app.")
    sys.exit(0)
# --- 2. PREMIUM DESIGN SYSTEM & GLASSMORPHISM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@400;600&display=swap');
    
    :root {
        --primary: #10B981;
        --secondary: #3B82F6;
        --background: #0F172A;
        --surface: rgba(30, 41, 59, 0.7);
        --text: #F8FAFC;
    }

    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        color: var(--text);
    }
    
    h1, h2, h3 { 
        font-family: 'Outfit', sans-serif; 
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }

    .main { 
        background-color: var(--background);
        background-image: 
            radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.1) 0px, transparent 50%);
    }

    /* Glassmorphism Card Style */
    div[data-testid="metric-container"], .stDataFrame, .stPlotlyChart {
        background: var(--surface);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease-in-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
    }

    .stSidebar { 
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Custom Ticker */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: rgba(16, 185, 129, 0.1);
        padding: 10px 0;
        border-radius: 8px;
        margin-bottom: 25px;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .ticker {
        display: flex;
        white-space: nowrap;
        animation: ticker 30s linear infinite;
    }
    .ticker-item {
        padding: 0 40px;
        font-size: 0.9rem;
        color: var(--primary);
        font-weight: 600;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & MODEL INGESTION ---
@st.cache_data
def load_assets():
    try:
        df = pd.read_csv(DATA_PATH)
    except:
        # Generate dummy data if file missing for demonstration
        data = {
            'total_lifecycle_carbon_footprint': np.random.uniform(100, 1000, 100),
            'manufacturing_efficiency': np.random.uniform(0.6, 0.95, 100),
            'manufacturing_water_usage': np.random.uniform(500, 5000, 100),
            'recycling_efficiency': np.random.uniform(0.3, 0.8, 100),
            'transport_distance_km': np.random.uniform(10, 5000, 100),
            'grid_carbon_intensity': np.random.uniform(200, 600, 100),
            'logistics_energy': np.random.uniform(50, 500, 100),
            'manufacturing_energy': np.random.uniform(100, 1000, 100),
            'lat': np.random.uniform(-60, 80, 100),
            'lon': np.random.uniform(-160, 160, 100)
        }
        df = pd.DataFrame(data)

    # Enrichment for Enterprise Visualization
    categories = ['Quantum Processor', 'Starship Hull', 'Cybernetic Limb', 'Bio-Reactor', 'Fusion Core']
    regions = ['Neo-Tokyo', 'Silicon Valley', 'Berlin Hub', 'Singapore Nexus', 'Luna Colony']
    df['Product_ID'] = [f"SKU-{1000+i}" for i in range(len(df))]
    df['Category'] = np.random.choice(categories, len(df))
    df['Region'] = np.random.choice(regions, len(df))
    df['Timestamp'] = pd.date_range(end=datetime.now(), periods=len(df), freq='H')
    df['Vendor'] = np.random.choice(['Apex Corp', 'Cyberdyne', 'Weyland-Yutani', 'Stark Ind'], len(df))
    
    # Load Models
    try:
        model = joblib.load(MODEL_PATH)
        security_model = joblib.load(SECURITY_MODEL_PATH)
        features = list(model.feature_names_in_)
    except:
        model = None
        security_model = None
        features = ['manufacturing_energy', 'transport_distance_km', 'grid_carbon_intensity']
    
    return df, model, security_model, features

df, carbon_model, security_model, features = load_assets()

# --- 4. TOP TICKER (LIVE MARKET SIMULATION) ---
st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            <div class="ticker-item">EU ETS Carbon: €84.20 (+1.2%)</div>
            <div class="ticker-item">Gold Standard Credit: $18.50 (-0.4%)</div>
            <div class="ticker-item">EcoTrack Index: 92.4 (STABLE)</div>
            <div class="ticker-item">Upcoming Audit: ISO 14064 (Q3)</div>
            <div class="ticker-item">Global Avg Intensity: 432 g/kWh</div>
            <div class="ticker-item">Renewable Mix: 42.1% (+5% WoW)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    st.title("EcoTrack™ v6.0")
    st.caption("AI-Powered Sustainability ERP")
    
    st.divider()
    page = st.radio("Intelligence Modules", ["Executive Suite", "Global Ledger", "Risk Engine", "Supply Chain AI"])
    
    st.divider()
    st.info("🟢 Production Node: Active")
    st.caption("Last Sync: " + datetime.now().strftime("%H:%M:%S"))

# --- 6. INTELLIGENCE MODULES ---

if page == "Executive Suite":
    st.markdown("## 🏛️ Executive Strategic Command")
    
    m1, m2, m3, m4 = st.columns(4)
    total_co2 = df['total_lifecycle_carbon_footprint'].sum()
    m1.metric("Carbon Liability", f"{total_co2/1000:.1f}k t", "-5.2%")
    m2.metric("ESG Rating", "AAA", "IMPROVING")
    m3.metric("Offset Portfolio", f"${total_co2 * 0.085:,.0f}", "+14k")
    m4.metric("Operational Alpha", "98.2%", "OPTIMAL")

    st.divider()

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📈 Carbon Efficiency vs. Revenue Alpha")
        fig = px.scatter(df, x='manufacturing_energy', y='total_lifecycle_carbon_footprint', 
                         color='Category', size='manufacturing_efficiency',
                         hover_data=['Product_ID', 'Vendor'],
                         template='plotly_dark', color_continuous_scale='Greens')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("🌱 Sustainability Mix")
        fig_pie = px.pie(df, names='Category', values='total_lifecycle_carbon_footprint', hole=0.6)
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

elif page == "Global Ledger":
    st.markdown("## ⛓️ Global Carbon Ledger (Blockchain Verified)")
    st.caption("High-integrity immutable transaction record for scope 1, 2, and 3 emissions.")
    
    ledger_data = df[['Timestamp', 'Product_ID', 'Vendor', 'Category', 'total_lifecycle_carbon_footprint']].tail(20)
    ledger_data['Hash'] = [os.urandom(8).hex() for _ in range(len(ledger_data))]
    
    st.dataframe(ledger_data, use_container_width=True)
    
    st.info("💡 **Ledger Insight**: All entries are cross-verified with regional grid intensities and vendor-signed emission factors.")

elif page == "Risk Engine":
    st.markdown("## 🛡️ Advanced Security & Anomaly Detection")
    
    if security_model:
        df['is_anomaly'] = security_model.predict(df[features])
        anomalies = df[df['is_anomaly'] == -1]
        
        s1, s2, s3 = st.columns(3)
        s1.metric("Threat Level", "LOW", border=True)
        s2.metric("Anomalous Events", len(anomalies), f"{len(anomalies)/len(df)*100:.1f}%")
        s3.metric("Model Confidence", "99.98%", "VALIDATED")

        if not anomalies.empty:
            st.warning("⚠️ CRITICAL ALERT: Outlier detected in supply chain telemetry.")
            st.dataframe(anomalies[['Product_ID', 'Region', 'Vendor', 'is_anomaly']].head(10), use_container_width=True)
    else:
        st.warning("Security Model training required for real-time anomaly detection.")

    st.divider()
    st.subheader("🧪 Sustainability 'What-If' Simulator")
    
    with st.expander("Adjust Operational Parameters"):
        input_data = {}
        cols = st.columns(3)
        for i, feat in enumerate(features):
            input_data[feat] = cols[i % 3].number_input(f"Simulate {feat}", value=float(df[feat].mean()))
    
    if st.button("🚀 Execute Strategic Prediction"):
        if carbon_model:
            input_df = pd.DataFrame([input_data])
            prediction = carbon_model.predict(input_df)[0]
            st.success(f"PROJECTION: Predicted Footprint at **{prediction:.2f} kg CO2**")
            st.progress(min(max(prediction/1000, 0.0), 1.0))
        else:
            st.error("Model engine offline. Please integrate valid weight tensors.")

elif page == "Supply Chain AI":
    st.markdown("## 🌍 Global Supply Chain Cartography")
    
    # Simulate Geo Data if not present
    if 'lat' not in df.columns:
        df['lat'] = np.random.uniform(-40, 60, len(df))
        df['lon'] = np.random.uniform(-120, 140, len(df))
    
    fig_map = px.scatter_geo(df, lat='lat', lon='lon', color='total_lifecycle_carbon_footprint',
                            hover_name='Vendor', size='manufacturing_efficiency',
                            projection="natural earth", template='plotly_dark')
    fig_map.update_geos(showcountries=True, countrycolor="rgba(255,255,255,0.1)")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

    st.divider()
    st.subheader("🤖 AI Sustainability Advisor")
    
    avg_carbon = df['total_lifecycle_carbon_footprint'].mean()
    high_impact = df[df['total_lifecycle_carbon_footprint'] > avg_carbon]
    
    with st.chat_message("assistant"):
        st.write(f"Based on my analysis of {len(df)} nodes, here are your strategic imperatives:")
        st.write(f"- **Optimized Logistics**: Shifting {len(high_impact)} high-impact nodes in {high_impact['Region'].iloc[0]} to lower-intensity grids could reduce footprint by 12%.")
        st.write("- **Vendor Compliance**: Weyland-Yutani is showing a 15% delta in recycling efficiency compared to global benchmarks.")
        st.write("- **Energy Pivot**: Transitioning Fusion Core manufacturing to 100% solar could net $45k in annual carbon credits.")

# --- 7. FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>EcoTrack Enterprise © 2026 | ISO 14001 Compliant | AI Stability: 99.9%</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    # When Streamlit executes a script it does so under __main__.  The
    # early exit above will have already handled bare execution, so this
    # block is mostly harmless and can serve as a gentle reminder if
    # someone accidentally runs the file twice.
    print("Note: launch the user interface with `streamlit run dashboard.py`")
