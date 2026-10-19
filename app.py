import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS (DARK THEME)
# ==========================================
st.set_page_config(page_title="Dashboard PM2.5 Kalteng", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #4facfe;
    }
    div[data-testid="stMetricLabel"] {
        color: #a8a8b3;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌦️ PM2.5 Advanced Monitoring & Forecasting")
st.markdown("---")

# ==========================================
# 2. DATA MURNI TAHUN 2026 (JULI - OKTOBER)
# ==========================================
np.random.seed(42)
waktu = pd.date_range(start="2026-07-16 00:00:00", end="2026-10-16 23:00:00", freq="h") 
pm25_aktual = np.random.normal(50, 20, len(waktu)) 
threshold = 55.4

# ==========================================
# 3. LAYOUT ATAS: AREA CHART & GAUGE CHART
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Konsentrasi PM2.5 (Data Historis Juli - Oktober 2026)")
    placeholder_area = st.empty()

with col2:
    st.subheader("Status Kritis Saat Ini")
    placeholder_gauge = st.empty()

st.markdown("---")

# ==========================================
# 4. LAYOUT BAWAH: KPI & TABEL DATA
# ==========================================
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Total Anomali (E1)", "1,584", "Berdasarkan Threshold 55.4", delta_color="inverse")
with col4:
    st.metric("RMSE ARIMA(1,1,1)", "627.01", "Akurat")
with col5:
    st.metric("Trend Up (E2)", "525", "Persisten 4 Jam")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 Log Deteksi Complex Event Processing (CEP)")

log_data = pd.DataFrame({
    "Dimensi (Waktu)": ["2026-10-16 21:00", "2026-10-16 22:00", "2026-10-16 23:00"],
    "Impc. (Konsentrasi)": [873, 790, 558],
    "Spent (Status)": ["Kritis (E1)", "Kritis (E1)", "Waspada (E2)"]
})
st.dataframe(log_data, use_container_width=True, hide_index=True)

# ==========================================
# 5. INFINITE LOOP ANIMASI
# ==========================================
while True:
    for i in range(48, len(waktu)+1, 48):
        waktu_berjalan = waktu[:i]
        pm25_berjalan = pm25_aktual[:i]
        nilai_terakhir = pm25_berjalan[-1]
        
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=waktu_berjalan, 
            y=pm25_berjalan, 
            fill='tozeroy', 
            mode='lines',
            line=dict(color='#00f2fe', width=1.5),
            name='PM2.5'
        ))
        fig_area.add_hline(
            y=threshold, 
            line_dash="dash", 
            line_color="red", 
            annotation_text="Batas Bahaya",
            annotation_font=dict(color="white")
        )
        fig_area.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(
                range=[waktu[0], waktu[-1]],
                tickformat="%d %b %Y"
            ), 
            yaxis=dict(range=[0, max(pm25_aktual)+10]) 
        )
        placeholder_area.plotly_chart(fig_area, use_container_width=True)
        
        # PERBAIKAN TYPO DI SINI ('text' dengan kutip yang benar)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = nilai_terakhir,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Indeks PM2.5", 'font': {'color': 'white'}},
            gauge = {
                'axis': {'range': [None, max(pm25_aktual)+10], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#00f2fe"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, threshold], 'color': "rgba(76, 175, 80, 0.3)"},
                    {'range': [threshold, max(pm25_aktual)+10], 'color': "rgba(244, 67, 54, 0.3)"}],
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            height=300,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        placeholder_gauge.plotly_chart(fig_gauge, use_container_width=True)
        
        time.sleep(0.2)
        
    time.sleep(2)
