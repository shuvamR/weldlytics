# app.py
import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
from pathway_pipeline import data_queue

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Weldlytics | AI Welding Intelligence",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS (PROFESSIONAL DARK THEME) ====================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark theme background */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0f1629 100%);
    }

    /* Glassmorphism card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }

    /* Metric cards with gradients */
    .metric-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    .metric-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 16px;
        padding: 1.2rem;
        color: white;
        text-align: center;
    }
    .metric-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 16px;
        padding: 1.2rem;
        color: white;
        text-align: center;
    }
    .metric-info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 16px;
        padding: 1.2rem;
        color: white;
        text-align: center;
    }

    /* Worker screen huge indicators */
    .worker-good {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        border-radius: 50px;
        padding: 2rem;
        text-align: center;
        animation: pulse-green 1.5s infinite;
    }
    .worker-bad {
        background: linear-gradient(135deg, #cb2d3e, #ef473a);
        border-radius: 50px;
        padding: 2rem;
        text-align: center;
        animation: pulse-red 1s infinite;
    }
    .worker-adjust {
        background: linear-gradient(135deg, #f2994a, #f2c94c);
        border-radius: 50px;
        padding: 2rem;
        text-align: center;
        animation: pulse-orange 1.2s infinite;
    }
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(0,176,155,0.7); }
        70% { box-shadow: 0 0 0 20px rgba(0,176,155,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,176,155,0); }
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(203,45,62,0.7); }
        70% { box-shadow: 0 0 0 20px rgba(203,45,62,0); }
        100% { box-shadow: 0 0 0 0 rgba(203,45,62,0); }
    }
    @keyframes pulse-orange {
        0% { box-shadow: 0 0 0 0 rgba(242,153,74,0.7); }
        70% { box-shadow: 0 0 0 20px rgba(242,153,74,0); }
        100% { box-shadow: 0 0 0 0 rgba(242,153,74,0); }
    }

    /* Big circle indicator */
    .circle-good {
        width: 180px;
        height: 180px;
        background: radial-gradient(circle at 30% 30%, #00ff88, #00b09b);
        border-radius: 50%;
        margin: 0 auto;
        box-shadow: 0 0 30px rgba(0,255,136,0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    .circle-bad {
        width: 180px;
        height: 180px;
        background: radial-gradient(circle at 30% 30%, #ff4444, #cb2d3e);
        border-radius: 50%;
        margin: 0 auto;
        box-shadow: 0 0 30px rgba(255,68,68,0.5);
        animation: glow 1s ease-in-out infinite alternate;
    }
    .circle-adjust {
        width: 180px;
        height: 180px;
        background: radial-gradient(circle at 30% 30%, #ffaa44, #f2994a);
        border-radius: 50%;
        margin: 0 auto;
        box-shadow: 0 0 30px rgba(255,170,68,0.5);
        animation: pulse 1.2s infinite;
    }
    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(255,255,255,0.3); }
        to { box-shadow: 0 0 40px rgba(255,255,255,0.6); }
    }

    /* Custom sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 15, 30, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }

    /* Headers */
    h1, h2, h3 {
        font-weight: 700 !important;
        background: linear-gradient(135deg, #fff, #a0a0ff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    /* Dataframes */
    .dataframe {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    /* Alert cards */
    .alert-high {
        background: rgba(203,45,62,0.2);
        border-left: 4px solid #cb2d3e;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .alert-medium {
        background: rgba(242,153,74,0.2);
        border-left: 4px solid #f2994a;
        padding: 0.8rem;
        border-radius: 8px;
    }
    .alert-low {
        background: rgba(0,176,155,0.2);
        border-left: 4px solid #00b09b;
        padding: 0.8rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        'timestamp', 'current', 'temperature', 'vibration', 'quality', 'confidence', 'explanation'
    ])
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'machine_on' not in st.session_state:
    st.session_state.machine_on = True

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🔥 **WELDLYTICS**")
    st.markdown("*AI-Powered Welding Intelligence*")
    st.divider()

    # Navigation icons (using emojis as icons)
    page = st.radio(
        "**MENU**",
        [
            "👨‍🏭 Worker Screen",
            "📊 Live Monitor",
            "🧠 AI Insight",
            "💰 Cost Savings",
            "🧵 Consumables",
            "📈 Learning (BDH)",
            "🚨 Alerts",
            "⚙️ Settings",
            "📋 Analytics",
            "💬 ASK AI"
        ],
        index=0,
        format_func=lambda x: x
    )

    st.divider()
    # System status
    st.markdown("### 🟢 System Status")
    st.caption("Real-time connection: **ACTIVE**")
    st.caption("ESP32 Simulator: **RUNNING**")
    st.caption("BDH Model: **ONLINE**")

    # Version
    st.divider()
    st.caption("v2.0 | Enterprise Edition")


# ==================== HELPER FUNCTIONS ====================
def get_latest_data():
    try:
        data = data_queue.get_nowait()
        if 'alert' in data:
            st.session_state.alerts.append(data)
            return None
        return data
    except:
        return None


# Get initial data
latest = get_latest_data()

# ==================== PAGE 1: WORKER SCREEN ====================
if page == "👨‍🏭 Worker Screen":
    st.markdown("## 👨‍🏭 **Operator View**")
    st.markdown("*Extremely simple – for shop floor use*")

    if latest:
        quality = latest['quality']
        suggestion = latest.get('suggestion', '')

        # Big colored card
        if quality == "GOOD":
            st.markdown('<div class="worker-good"><h1 style="color:white; font-size:4rem;">✅ GOOD WELD</h1></div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; margin-top:1rem;"><h3>🟢 Suggestion: {suggestion}</h3></div>',
                        unsafe_allow_html=True)
            # Big circle
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="circle-good"></div>', unsafe_allow_html=True)
        elif quality == "REJECTED":
            st.markdown('<div class="worker-bad"><h1 style="color:white; font-size:4rem;">❌ BAD WELD</h1></div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; margin-top:1rem;"><h3>🔴 Suggestion: {suggestion}</h3></div>',
                        unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="circle-bad"></div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="worker-adjust"><h1 style="color:white; font-size:3rem;">⚠️ ADJUST PARAMETERS</h1></div>',
                unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; margin-top:1rem;"><h3>🟡 Suggestion: {suggestion}</h3></div>',
                        unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="circle-adjust"></div>', unsafe_allow_html=True)
    else:
        st.info("⏳ Waiting for welding data...")

# ==================== PAGE 2: LIVE MONITOR ====================
elif page == "📊 Live Monitor":
    st.markdown("## 📊 **Real‑time Weld Monitor**")
    st.caption("Live current signature with anomaly detection")

    # Metrics row
    if latest:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-primary"><h3>⚡ Current</h3><h2>{latest["current"]:.1f} A</h2></div>',
                        unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-info"><h3>🌡️ Temp</h3><h2>{latest["temperature"]:.1f} °C</h2></div>',
                        unsafe_allow_html=True)
        with col3:
            st.markdown(
                f'<div class="metric-warning"><h3>📳 Vibration</h3><h2>{latest["vibration"]:.2f} mm/s</h2></div>',
                unsafe_allow_html=True)
        with col4:
            stability = "✅ Stable" if 80 <= latest["current"] <= 120 else "⚠️ Unstable"
            st.markdown(f'<div class="metric-success"><h3>📊 Stability</h3><h2>{stability}</h2></div>',
                        unsafe_allow_html=True)

    # Live chart placeholder
    chart_placeholder = st.empty()
    spike_placeholder = st.empty()

    # Update loop (30 seconds)
    for _ in range(60):
        data = get_latest_data()
        if data and 'current' in data:
            # Update history
            new_row = pd.DataFrame([{
                'timestamp': data['timestamp'],
                'current': data['current'],
                'temperature': data['temperature'],
                'vibration': data['vibration'],
                'quality': data['quality'],
                'confidence': data['confidence'],
                'explanation': data['explanation']
            }])
            st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)
            if len(st.session_state.history) > 100:
                st.session_state.history = st.session_state.history.tail(100)

            # Professional Plotly chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=st.session_state.history['timestamp'],
                y=st.session_state.history['current'],
                mode='lines',
                name='Welding Current',
                line=dict(color='#00f2fe', width=3),
                fill='tozeroy',
                fillcolor='rgba(0,242,254,0.1)'
            ))
            # Thresholds
            fig.add_hline(y=140, line_dash="dash", line_color="#ff4444", annotation_text="Spike Threshold")
            fig.add_hline(y=60, line_dash="dash", line_color="#ffaa44", annotation_text="Drop Threshold")
            fig.add_hrect(y0=80, y1=120, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Optimal Range")

            fig.update_layout(
                title="Welding Current Signature",
                xaxis_title="Time",
                yaxis_title="Current (Amperes)",
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)

            # Spike detection
            if data['current'] > 140:
                spike_placeholder.error(
                    f"⚠️ **SPIKE DETECTED!** Current: {data['current']:.0f}A – Reduce current immediately")
            elif data['current'] < 60:
                spike_placeholder.warning(f"⚠️ **DROP DETECTED!** Current: {data['current']:.0f}A – Increase current")
            else:
                spike_placeholder.success("✅ No anomalies detected – arc stable")

        time.sleep(0.5)

# ==================== PAGE 3: AI INSIGHT ====================
elif page == "🧠 AI Insight":
    st.markdown("## 🧠 **AI Insight Panel**")
    st.caption("*Explainable AI – Why did the weld pass or fail?*")

    if latest:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-primary"><h3>🎯 Confidence</h3><h2>{latest["confidence"]:.0%}</h2></div>',
                        unsafe_allow_html=True)
        with col2:
            color = "metric-success" if latest["quality"] == "GOOD" else "metric-warning"
            st.markdown(f'<div class="{color}"><h3>🔮 Prediction</h3><h2>{latest["quality"]}</h2></div>',
                        unsafe_allow_html=True)

        st.divider()
        st.subheader("🔍 Root Cause Analysis")
        st.info(f"📢 {latest['explanation']}")

        # Additional insights
        st.subheader("📊 Parameter Breakdown")
        params = {
            "Current": latest['current'],
            "Temperature": latest['temperature'],
            "Vibration": latest['vibration']
        }
        for param, value in params.items():
            st.progress(min(value / 200, 1.0) if param == "Current" else min(value / 100, 1.0))
            st.caption(f"{param}: {value:.1f}")
    else:
        st.info("Awaiting data for analysis...")

# ==================== PAGE 4: COST SAVINGS ====================
elif page == "💰 Cost Savings":
    st.markdown("## 💰 **Cost Savings Dashboard**")
    st.caption("*Realized savings from quality improvement*")

    if latest:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-success" style="text-align:center">
                <h3>💵 Material Saved</h3>
                <h1>₹{latest['material_saved']:.0f}</h1>
                <small>this week</small>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-primary" style="text-align:center">
                <h3>🔧 Rework Saved</h3>
                <h1>₹{latest['rework_saved']:.0f}</h1>
                <small>this week</small>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-warning" style="text-align:center">
                <h3>✅ Defects Prevented</h3>
                <h1>{latest['defects_prevented']}</h1>
                <small>this week</small>
            </div>
            """, unsafe_allow_html=True)

        total = latest['material_saved'] + latest['rework_saved']
        st.success(f"## 🎉 **Total Savings This Week: ₹{total:.0f}**")
        st.progress(min(total / 50000, 1.0))
        st.caption("📈 Target: ₹50,000 monthly savings | On track: {:.0%}".format(total / 12500))

        # Savings trend (simulated)
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        savings = [total - 3000, total - 2000, total - 1000, total]
        fig = px.line(x=weeks, y=savings, title="Savings Trend (Last 4 Weeks)",
                      labels={'x': 'Week', 'y': 'Savings (₹)'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Calculating savings...")

# ==================== PAGE 5: CONSUMABLES ====================
elif page == "🧵 Consumables":
    st.markdown("## 🧵 **Consumable Tracker**")
    st.caption("*Real-time electrode and gas usage*")

    if latest:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔌 Electrode Remaining")
            electrode_pct = (latest['electrode_usage'] / 1000) * 100
            st.progress(electrode_pct / 100)
            st.metric("Length Left", f"{latest['electrode_usage']:.0f} mm")
            if latest['electrode_usage'] < 100:
                st.warning("⚠️ **LOW STOCK ALERT** – Replace electrode soon")

        with col2:
            st.subheader("⛽ Gas Remaining")
            st.progress(latest['gas_remaining'] / 100)
            st.metric("Gas Left", f"{latest['gas_remaining']:.0f}%")
            if latest['gas_remaining'] < 15:
                st.warning("⚠️ **LOW GAS ALERT** – Refill cylinder")

        # Consumption chart
        st.subheader("📉 Consumption Rate (Last 8 hours)")
        consumption = pd.DataFrame({
            'Hour': list(range(1, 9)),
            'Electrode (mm)': np.random.uniform(5, 20, 8),
            'Gas (%)': np.random.uniform(1, 6, 8)
        })
        fig = px.line(consumption, x='Hour', y=['Electrode (mm)', 'Gas (%)'], title="Consumption Trend")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tracking consumables...")

# ==================== PAGE 6: LEARNING (BDH) ====================
elif page == "📈 Learning (BDH)":
    st.markdown("## 📈 **Baby Dragon Hatchling – Learning Status**")
    st.caption("*Continuous online learning – accuracy improves over time*")

    if latest:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f'<div class="metric-primary"><h3>🎯 Current Accuracy</h3><h2>{latest["training_accuracy"]:.0%}</h2></div>',
                unsafe_allow_html=True)
            st.markdown(f'<div class="metric-info"><h3>📅 Days Trained</h3><h2>{latest["days_trained"]}</h2></div>',
                        unsafe_allow_html=True)
        with col2:
            # Accuracy improvement over time
            accuracies = [0.70, 0.73, 0.77, 0.80, 0.83, 0.85, 0.87, 0.89, 0.90, latest['training_accuracy']]
            days = list(range(1, len(accuracies) + 1))
            fig = px.line(x=days, y=accuracies, title="Model Accuracy Improvement",
                          labels={'x': 'Day', 'y': 'Accuracy'})
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig, use_container_width=True)

        st.progress(latest['training_accuracy'])
        if latest['training_accuracy'] > 0.85:
            st.success("🎉 **Target accuracy achieved!** Model is production-ready.")
        else:
            st.warning("🔄 **Still learning** – more data needed to reach 90% accuracy")

        st.caption("💡 *BDH adapts to new materials and operators in real time*")
    else:
        st.info("Initializing learning model...")

# ==================== PAGE 7: ALERTS ====================
elif page == "🚨 Alerts":
    st.markdown("## 🚨 **Alert Center**")
    st.caption("*Actionable alerts with severity levels*")

    if st.session_state.alerts:
        for alert in st.session_state.alerts[-10:]:
            if alert.get('severity') == 'HIGH':
                st.markdown(f'<div class="alert-high">🔴 **HIGH** – {alert.get("message", "Bad weld detected")}</div>',
                            unsafe_allow_html=True)
            elif alert.get('severity') == 'MEDIUM':
                st.markdown(f'<div class="alert-medium">🟡 **MEDIUM** – {alert.get("message", "Quality issue")}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-low">🟢 **LOW** – {alert.get("message", "Info")}</div>',
                            unsafe_allow_html=True)
    else:
        st.success("✅ No active alerts – all systems normal")

    if latest:
        st.divider()
        st.subheader("🏭 Machine Risk Assessment")
        risk = latest.get('machine_risk', 'LOW')
        if risk == 'HIGH':
            st.error("⚠️ **HIGH RISK** – Machine overheating! Immediate inspection required.")
        elif risk == 'MEDIUM':
            st.warning("⚠️ **MEDIUM RISK** – Temperature elevated, schedule maintenance.")
        else:
            st.success("✅ **LOW RISK** – All parameters within safe limits.")

# ==================== PAGE 8: SETTINGS ====================
elif page == "⚙️ Settings":
    st.markdown("## ⚙️ **Settings & Integration**")
    st.caption("*Configure machines, sensors, and enterprise integration*")

    with st.expander("🔧 Machine Configuration", expanded=True):
        machine = st.selectbox("Select Welding Machine", ["Machine #1 - ArcMaster 3000", "Machine #2 - TechWeld Pro",
                                                          "Machine #3 - Industrial 500"])
        st.checkbox("Enable Auto-Calibration", value=True)
        st.slider("Current Sensor Offset (A)", -20, 20, 0)

    with st.expander("🌐 Integration", expanded=True):
        st.checkbox("Connect to PLC/SCADA", value=False)
        st.text_input("MQTT Broker URL", "mqtt://localhost:1883")
        st.text_input("API Endpoint", "http://localhost:8000/api/welds")

    with st.expander("🔔 Notification Rules"):
        st.slider("Alert Threshold – Current Spike (A)", 120, 200, 140)
        st.slider("Alert Threshold – Temperature (°C)", 60, 100, 80)

    if st.button("💾 Save All Settings"):
        st.success("Settings saved successfully!")

# ==================== PAGE 9: ANALYTICS ====================
elif page == "📋 Analytics":
    st.markdown("## 📋 **Historical Analytics**")
    st.caption("*Quality trends and performance metrics*")

    if not st.session_state.history.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Quality Distribution")
            counts = st.session_state.history['quality'].value_counts()
            fig = px.pie(values=counts.values, names=counts.index, title="Weld Quality Breakdown")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Confidence Trend (Last 50)")
            st.line_chart(st.session_state.history['confidence'].tail(50))

        st.subheader("Recent Welds")
        st.dataframe(st.session_state.history.tail(20)[['timestamp', 'current', 'quality', 'confidence']],
                     use_container_width=True)

        # Export option
        csv = st.session_state.history.to_csv(index=False)
        st.download_button("📥 Export to CSV", csv, "weld_history.csv", "text/csv")
    else:
        st.info("No historical data yet. Run live monitor to collect data.")

# ==================== PAGE 10: ASK AI ====================
else:
    st.markdown("## 💬 **ASK AIt**")
    st.caption("*Ask anything about your welding operations*")


    def mock_llm(question, latest_data):
        q = question.lower()
        if "current" in q:
            return f"⚡ Current welding current is **{latest_data['current']:.0f}A**. Optimal range: 100-120A."
        elif "saving" in q or "cost" in q:
            total = latest_data['material_saved'] + latest_data['rework_saved']
            return f"💰 Total savings this week: **₹{total:.0f}** from {latest_data['defects_prevented']} prevented defects."
        elif "accuracy" in q or "learning" in q:
            return f"🎯 BDH model accuracy: **{latest_data['training_accuracy']:.0%}** after {latest_data['days_trained']} days of training."
        elif "consumable" in q or "electrode" in q:
            return f"🔌 Electrode remaining: {latest_data['electrode_usage']:.0f} mm. Gas: {latest_data['gas_remaining']:.0f}%."
        else:
            return "I can help with current readings, cost savings, model accuracy, consumables, and welding parameters. What would you like to know?"


    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant",
                                          "content": "Hi! I'm Weldlytics AI. Ask me about welding data, costs, consumables, or model performance."}]

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask anything..."):
        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.spinner("Analyzing..."):
            response = mock_llm(prompt, latest) if latest else "Awaiting data connection..."
            st.chat_message("assistant").write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("<center><small>🔥 Weldlytics Team | Beyond Transformers Hackathon | © 2026</small></center>",
            unsafe_allow_html=True)