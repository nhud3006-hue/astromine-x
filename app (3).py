import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Cấu hình trang
st.set_page_config(page_title="🚀 AstroMine-X", page_icon="🪐", layout="wide")

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header { font-size: 3rem; color: #4A90E2; text-align: center; padding: 1rem 0; }
    .sub-header { font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .info-box { background-color: #f0f2f6; padding: 1rem; border-radius: 10px; border-left: 5px solid #4A90E2; margin-bottom: 1rem; }
    .error-box { background-color: #ffebee; padding: 1rem; border-radius: 10px; border-left: 5px solid #e53935; margin-bottom: 1rem; }
    .result-box { background-color: #e8f5e9; padding: 1rem; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🪐 AstroMine-X</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Phát hiện ngoại hành tinh từ dữ liệu TESS với AI</p>', unsafe_allow_html=True)

# Sidebar hướng dẫn
with st.sidebar:
    st.title("📖 Hướng dẫn")
    st.markdown("""
    **AstroMine-X** là công cụ AI giúp bạn phát hiện ngoại hành tinh từ dữ liệu TESS.

    ### 🚀 Cách sử dụng:
    1. Tải lên file CSV (có thể có tên cột khác nhau, AI tự nhận diện).
    2. Nhấn **Phân tích**.
    3. Xem kết quả độ tin cậy (Confidence).

    ### 📌 Yêu cầu dữ liệu:
    File CSV cần có các cột chứa thông tin:
    - Chu kỳ quỹ đạo (period)
    - Bán kính (radius)
    - Khối lượng (mass)
    - Độ nghiêng (inclination)
    - Nhiệt độ sao (teff)
    - Trọng lực bề mặt (logg)

    ### ✅ Độ chính xác:
    Khoảng **85.56%** trên dữ liệu thử nghiệm.
    """)

# Load model
try:
    model = joblib.load("planet_model_lgb_fixed.pkl")
    scaler = joblib.load("scaler_lgb_fixed.pkl")
    st.success("✅ Model và scaler đã sẵn sàng!")
except Exception as e:
    st.error(f"❌ Không tìm thấy file model: {e}")
    st.stop()

# Hàm tự động tìm tên cột gần đúng
def find_column(df, possible_names):
    """Tìm tên cột trong dataframe khớp với một trong các tên khả dĩ"""
    # Kiểm tra khớp chính xác
    for name in possible_names:
        if name in df.columns:
            return name
    # Kiểm tra gần đúng (không phân biệt hoa thường, bỏ dấu gạch dưới)
    for col in df.columns:
        col_clean = col.lower().replace('_', '').replace(' ', '')
        for name in possible_names:
            name_clean = name.lower().replace('_', '').replace(' ', '')
            if col_clean == name_clean or col_clean in name_clean or name_clean in col_clean:
                return col
    return None

# Định nghĩa các cột cần thiết và tên gợi ý
required_fields = {
    'pl_orbper': ['pl_orbper', 'orbper', 'period', 'p_orb', 'orbital_period'],
    'pl_radj': ['pl_radj', 'radj', 'radius', 'planet_radius', 'r_planet'],
    'pl_bmasse': ['pl_bmasse', 'bmasse', 'mass', 'planet_mass', 'm_planet'],
    'pl_orbincl': ['pl_orbincl', 'orbincl', 'inclination', 'incl', 'i_orb'],
    'st_teff': ['st_teff', 'teff', 'temp', 'temperature', 'stellar_temp'],
    'st_logg': ['st_logg', 'logg', 'surface_gravity', 'gravity']
}

# Tab nhập liệu
tab1, tab2 = st.tabs(["📂 Tải file CSV", "✏️ Nhập thủ công"])

# ===== TAB 1: TẢI FILE CSV =====
with tab1:
    uploaded_file = st.file_uploader("Chọn file CSV (tối đa 200MB)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Đã tải file {uploaded_file.name} thành công! ({len(df)} dòng)")
            
            # Hiển thị 5 dòng đầu
            with st.expander("Xem trước dữ liệu"):
                st.dataframe(df.head())
            
            # Kiểm tra và ánh xạ các cột
            st.subheader("🔍 Phân tích cấu trúc dữ liệu")
            col_mapping = {}
            missing_cols = []
            
            for field, possible_names in required_fields.items():
                found = find_column(df, possible_names)
                if found:
                    col_mapping[field] = found
                    st.info(f"✅ Tìm thấy cột '{found}' cho '{field}'")
                else:
                    missing_cols.append(field)
                    st.error(f"❌ Không tìm thấy cột cho '{field}'")
            
            if missing_cols:
                st.markdown('<div class="error-box">⚠️ Không tìm thấy tất cả các cột cần thiết. Vui lòng kiểm tra lại file CSV.</div>', unsafe_allow_html=True)
                st.write("**Các tên cột được gợi ý:**")
                for field in missing_cols:
                    st.write(f"- `{field}` (hoặc các tên tương tự: {required_fields[field]})")
            else:
                st.success("✅ Tất cả các cột đều được tìm thấy! Sẵn sàng phân tích.")
                
                if st.button("🔍 Phân tích", key="btn_upload"):
                    # Xây dựng dataframe với các cột đã ánh xạ
                    X = pd.DataFrame()
                    for field, col_name in col_mapping.items():
                        X[field] = df[col_name]
                    
                    # Xử lý dữ liệu thiếu
                    X = X.fillna(X.mean())
                    
                    # Chuẩn hóa và dự đoán
                    X_scaled = scaler.transform(X)
                    proba = model.predict_proba(X_scaled)[:, 1]
                    
                    # Thêm kết quả vào dataframe gốc
                    df_result = df.copy()
                    df_result['Confidence'] = np.round(proba, 3)
                    
                    st.subheader("📊 Kết quả dự đoán")
                    st.dataframe(df_result[['Confidence']])
                    
                    # Biểu đồ phân bố độ tin cậy
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.hist(df_result['Confidence'], bins=20, color='skyblue', edgecolor='black')
                    ax.axvline(x=0.5, color='red', linestyle='--', label='Ngưỡng 50%')
                    ax.set_xlabel('Độ tin cậy (Confidence)')
                    ax.set_ylabel('Số lượng')
                    ax.set_title('Phân bố độ tin cậy của các ứng viên')
                    ax.legend()
                    st.pyplot(fig)
        
        except Exception as e:
            st.error(f"❌ Lỗi xử lý file: {e}")

# ===== TAB 2: NHẬP THỦ CÔNG =====
with tab2:
    st.markdown('<div class="info-box">✏️ Nhập thông số của một ngôi sao để kiểm tra nhanh.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        orbper = st.number_input('Chu kỳ quỹ đạo (ngày)', value=5.0, format="%.2f")
        radj = st.number_input('Bán kính (Rjup)', value=1.2, format="%.2f")
        bmasse = st.number_input('Khối lượng (Mjup)', value=2.5, format="%.2f")
    with col2:
        orbincl = st.number_input('Độ nghiêng (độ)', value=85.0, format="%.2f")
        st_teff = st.number_input('Nhiệt độ sao (K)', value=5500.0, format="%.0f")
        st_logg = st.number_input('log(g) (cm/s²)', value=4.2, format="%.2f")
    
    if st.button("🔍 Dự đoán ngôi sao này", key="btn_manual"):
        input_data = np.array([[orbper, radj, bmasse, orbincl, st_teff, st_logg]])
        input_scaled = scaler.transform(input_data)
        proba = model.predict_proba(input_scaled)[0][1]
        
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        if proba > 0.5:
            st.success(f"✅ **CÓ HÀNH TINH!** Độ tin cậy: {proba*100:.2f}%")
        else:
            st.warning(f"❌ **KHÔNG CÓ HÀNH TINH.** Độ tin cậy: {proba*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<center>🚀 AstroMine-X v2.0 | Phát triển với ❤️ bởi đội ngũ nghiên cứu trẻ</center>", unsafe_allow_html=True)
