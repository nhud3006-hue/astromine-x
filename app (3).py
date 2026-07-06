import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import random
import json  # <--- Thêm import này

# --- Cấu hình trang ---
st.set_page_config(page_title="🚀 AstroMine-X", page_icon="🪐", layout="wide")

# --- CSS tích hợp Linh Bảo ---
st.markdown("""
<style>
    /* Định dạng chính */
    .main-header {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4A90E2;
        margin-bottom: 1rem;
    }
    
    /* Linh Bảo - con thú cưng ảo */
    .linhbao-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        cursor: pointer;
        text-align: center;
        transition: transform 0.3s ease;
        background: rgba(255,255,255,0.9);
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        width: 100px;
        height: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .linhbao-container:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .linhbao-avatar {
        font-size: 3.5rem;
        line-height: 1.2;
        animation: float 3s ease-in-out infinite;
    }
    .linhbao-bubble {
        background: white;
        border-radius: 15px;
        padding: 8px 15px;
        font-size: 0.8rem;
        color: #333;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 5px;
        max-width: 120px;
        border: 1px solid #eee;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .linhbao-speaking {
        animation: speak 0.5s ease-in-out 3;
    }
    @keyframes speak {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    /* Điều chỉnh để tránh đè lên nội dung chính */
    .main-content {
        padding-bottom: 120px;
    }
</style>
""", unsafe_allow_html=True)

# --- Danh sách câu nói của Linh Bảo ---
LINHBAO_SAYINGS = [
    "Chào bạn! Mình là Linh Bảo đây! 🐾",
    "Bạn có muốn tìm hành tinh mới không? 🚀",
    "Hãy thử upload file CSV nhé! 📁",
    "Tớ thấy bạn rất thông minh đó! 😊",
    "Nếu cần giúp gì, cứ hỏi tớ nha! 💡",
    "Woohoo! Lại thêm một hành tinh mới! 🌟",
    "Bạn có tin vào người ngoài hành tinh không? 👽",
    "Mình thích khám phá vũ trụ lắm! ✨",
    "Bạn đang làm tốt lắm, tiếp tục đi nào! 💪",
    "Nếu không có dữ liệu, tớ sẽ buồn lắm đấy! 😢",
    "AstroMine-X là dự án tuyệt vời phải không? 😎",
    "Hãy nhìn lên bầu trời và mơ mộng đi! 🌌"
]

# --- Hiển thị Linh Bảo (đã sửa) ---
def show_linhbao():
    # Chuyển danh sách câu nói thành JSON để JavaScript hiểu
    sayings_json = json.dumps(LINHBAO_SAYINGS)
    
    html = f"""
    <div id="linhbao-wrapper">
        <div class="linhbao-container" id="linhbao" onclick="linhBaoSay()">
            <div class="linhbao-bubble" id="bubble">Chào bạn! Click vào tớ nhé! 🐾</div>
            <div class="linhbao-avatar">🐼</div>
        </div>
    </div>
    <script>
        // Biến sayings được truyền từ Python qua JSON
        const sayings = {sayings_json};
        
        function linhBaoSay() {{
            const bubble = document.getElementById('bubble');
            const avatar = document.querySelector('.linhbao-avatar');
            const randomIndex = Math.floor(Math.random() * sayings.length);
            const msg = sayings[randomIndex];
            bubble.textContent = msg;
            avatar.classList.add('linhbao-speaking');
            setTimeout(() => avatar.classList.remove('linhbao-speaking'), 1500);
        }}
        
        setTimeout(() => {{
            const bubble = document.getElementById('bubble');
            bubble.textContent = 'Mình là Linh Bảo! Rất vui được gặp bạn! 🐼';
        }}, 3000);
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- Nội dung chính ---
st.markdown('<p class="main-header">🪐 AstroMine-X</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Phát hiện ngoại hành tinh từ dữ liệu TESS với AI và Linh Bảo 🐼</p>', unsafe_allow_html=True)

# --- Sidebar hướng dẫn ---
with st.sidebar:
    st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/tess_artist_0.jpg", use_container_width=True)
    st.title("📖 Hướng dẫn & Linh Bảo")
    st.markdown("""
    **AstroMine-X** là công cụ AI phát hiện ngoại hành tinh.
    
    **Linh Bảo** – Trợ lý thông minh của bạn:
    - Click vào em ấy để tương tác!
    - Em ấy sẽ nhảy, nói chuyện và khuyến khích bạn.
    
    **Cách sử dụng:**
    1. Tải lên file CSV (6 cột: `pl_orbper, pl_radj, pl_bmasse, pl_orbincl, st_teff, st_logg`)
    2. Hoặc nhập thông số thủ công.
    3. Nhấn **Phân tích** để xem kết quả.
    
    **Độ chính xác:** ~85.56% trên tập kiểm tra.
    """)

# --- Hiển thị Linh Bảo ---
show_linhbao()

# --- Load model ---
try:
    model = joblib.load("planet_model_lgb_fixed.pkl")
    scaler = joblib.load("scaler_lgb_fixed.pkl")
    st.success("✅ Model và scaler đã sẵn sàng!")
except Exception as e:
    st.error(f"❌ Không tìm thấy model: {e}")
    st.stop()

# --- Tab nhập liệu ---
tab1, tab2 = st.tabs(["📂 Tải file CSV", "✏️ Nhập thủ công"])

with tab1:
    uploaded_file = st.file_uploader("Chọn file CSV (đúng 6 cột)", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        if st.button("🔍 Phân tích", key="btn_upload"):
            feature_cols = ['pl_orbper', 'pl_radj', 'pl_bmasse', 'pl_orbincl', 'st_teff', 'st_logg']
            # Kiểm tra cột
            missing = [col for col in feature_cols if col not in df.columns]
            if missing:
                st.error(f"❌ Thiếu các cột: {missing}. Vui lòng kiểm tra file CSV.")
                st.stop()
            X = df[feature_cols].copy()
            X = X.fillna(X.mean())
            X_scaled = scaler.transform(X)
            proba = model.predict_proba(X_scaled)[:, 1]
            df_result = df.copy()
            df_result['Confidence'] = np.round(proba, 3)
            st.subheader("📊 Kết quả dự đoán")
            st.dataframe(df_result[['Confidence']])
            
            fig, ax = plt.subplots()
            ax.hist(df_result['Confidence'], bins=20, color='skyblue', edgecolor='black')
            ax.set_xlabel('Độ tin cậy')
            ax.set_ylabel('Số lượng')
            ax.set_title('Phân bố độ tin cậy của các ứng viên')
            st.pyplot(fig)

with tab2:
    st.markdown("### ✏️ Nhập thông số để kiểm tra nhanh")
    col1, col2 = st.columns(2)
    with col1:
        orbper = st.number_input('Chu kỳ (ngày)', value=5.0)
        radj = st.number_input('Bán kính (Rjup)', value=1.2)
        bmasse = st.number_input('Khối lượng (Mjup)', value=2.5)
    with col2:
        orbincl = st.number_input('Độ nghiêng (độ)', value=85.0)
        st_teff = st.number_input('Nhiệt độ sao (K)', value=5500.0)
        st_logg = st.number_input('log(g) (cm/s²)', value=4.2)
    
    if st.button("🔍 Dự đoán", key="btn_manual"):
        input_data = np.array([[orbper, radj, bmasse, orbincl, st_teff, st_logg]])
        input_scaled = scaler.transform(input_data)
        proba = model.predict_proba(input_scaled)[0][1]
        if proba > 0.5:
            st.success(f"✅ **CÓ HÀNH TINH!** Độ tin cậy: {proba*100:.2f}%")
        else:
            st.warning(f"❌ **KHÔNG CÓ HÀNH TINH.** Độ tin cậy: {proba*100:.2f}%")

# --- Footer ---
st.markdown("---")
st.markdown("<center>🚀 AstroMine-X v2.0 | Phát triển với ❤️ và Linh Bảo 🐼<br>© 2026 Đội ngũ nghiên cứu trẻ</center>", unsafe_allow_html=True)
