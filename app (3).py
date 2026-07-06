
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="🚀 AstroMine-X", page_icon="🪐", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 3rem; color: #4A90E2; text-align: center; padding: 1rem 0; }
    .sub-header { font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .info-box { background-color: #f0f2f6; padding: 1rem; border-radius: 10px; border-left: 5px solid #4A90E2; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🪐 AstroMine-X</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Phát hiện ngoại hành tinh từ dữ liệu TESS với AI</p>', unsafe_allow_html=True)

with st.sidebar:
    st.title("📖 Hướng dẫn")
    st.markdown("""
    **AstroMine-X** là công cụ AI giúp bạn phát hiện ngoại hành tinh.

    ### Cách sử dụng:
    1. Tải lên file CSV (6 cột: pl_orbper, pl_radj, pl_bmasse, pl_orbincl, st_teff, st_logg)
    2. Nhấn **Phân tích**
    3. Xem kết quả độ tin cậy

    ### Độ chính xác:
    Khoảng **85.56%** trên dữ liệu thử nghiệm.
    """)

try:
    model = joblib.load("planet_model_lgb_fixed.pkl")
    scaler = joblib.load("scaler_lgb_fixed.pkl")
    st.success("✅ Model đã sẵn sàng!")
except:
    st.error("❌ Không tìm thấy model.")
    st.stop()

tab1, tab2 = st.tabs(["📂 Tải file CSV", "✏️ Nhập thủ công"])

with tab1:
    uploaded_file = st.file_uploader("Chọn file CSV", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        if st.button("🔍 Phân tích"):
            feature_cols = ['pl_orbper', 'pl_radj', 'pl_bmasse', 'pl_orbincl', 'st_teff', 'st_logg']
            X = df[feature_cols].copy()
            X = X.fillna(X.mean())
            X_scaled = scaler.transform(X)
            proba = model.predict_proba(X_scaled)[:, 1]
            df_result = df.copy()
            df_result['Confidence'] = np.round(proba, 3)
            st.subheader("📊 Kết quả")
            st.dataframe(df_result[['Confidence']])

with tab2:
    st.markdown("Nhập thông số để kiểm tra nhanh:")
    col1, col2 = st.columns(2)
    with col1:
        orbper = st.number_input('Chu kỳ (ngày)', value=5.0)
        radj = st.number_input('Bán kính (Rjup)', value=1.2)
        bmasse = st.number_input('Khối lượng (Mjup)', value=2.5)
    with col2:
        orbincl = st.number_input('Độ nghiêng (độ)', value=85.0)
        st_teff = st.number_input('Nhiệt độ sao (K)', value=5500.0)
        st_logg = st.number_input('log(g)', value=4.2)
    if st.button("🔍 Dự đoán"):
        input_data = np.array([[orbper, radj, bmasse, orbincl, st_teff, st_logg]])
        input_scaled = scaler.transform(input_data)
        proba = model.predict_proba(input_scaled)[0][1]
        if proba > 0.5:
            st.success(f"✅ CÓ HÀNH TINH! Độ tin cậy: {proba*100:.2f}%")
        else:
            st.warning(f"❌ KHÔNG CÓ HÀNH TINH. Độ tin cậy: {proba*100:.2f}%")

st.markdown("---")
st.markdown("<center>🚀 AstroMine-X v2.0 | Phát triển với ❤️</center>", unsafe_allow_html=True)
