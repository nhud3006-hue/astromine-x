import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import json

# ─── Cấu hình trang ────────────────────────────────────────────────
st.set_page_config(
    page_title="AstroMine-X | Exoplanet AI",
    page_icon="🪐",
    layout="wide"
)

# ─── CSS chung (giữ nguyên phần trước) ───────────────────────────
st.markdown("""
<style>
    /* Toàn bộ CSS như cũ, giữ nguyên */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #0B0E17;
        color: #E8EDF5;
    }
    .main-container { padding: 2rem 3rem; max-width: 1400px; margin: 0 auto; }
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 2rem;
    }
    .app-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    .app-subtitle { font-size: 1rem; font-weight: 300; color: #94A3B8; margin-top: 0.25rem; }
    .app-badge {
        background: rgba(96, 165, 250, 0.15);
        padding: 0.4rem 1.2rem;
        border-radius: 100px;
        font-size: 0.85rem;
        border: 1px solid rgba(96, 165, 250, 0.25);
        color: #93C5FD;
    }
    .card {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 1.8rem 2rem;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 2rem;
        transition: all 0.2s ease;
    }
    .card:hover { border-color: rgba(255,255,255,0.12); box-shadow: 0 12px 48px rgba(0,0,0,0.5); }
    .card-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 1.2rem; color: #E8EDF5; display: flex; align-items: center; gap: 0.6rem; }
    .card-title .icon { font-size: 1.4rem; }
    .css-1d391kg, .css-12oz5g7 { background: #0F1320 !important; }
    .sidebar-content { padding: 1.5rem 0.5rem; }
    .sidebar-title { font-size: 1.1rem; font-weight: 600; color: #E8EDF5; margin-bottom: 1rem; }
    .sidebar-text { font-size: 0.9rem; color: #94A3B8; line-height: 1.6; }
    .sidebar-divider { height: 1px; background: rgba(255,255,255,0.06); margin: 1.5rem 0; }
    .stButton button {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3) !important;
    }
    .stButton button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(59, 130, 246, 0.4) !important; }
    .stButton button:active { transform: scale(0.96) !important; }
    .dataframe { background: transparent !important; color: #E8EDF5 !important; border-collapse: collapse !important; }
    .dataframe th { background: rgba(255,255,255,0.05) !important; color: #93C5FD !important; font-weight: 600 !important; padding: 0.8rem !important; border-bottom: 2px solid rgba(255,255,255,0.08) !important; }
    .dataframe td { padding: 0.8rem !important; border-bottom: 1px solid rgba(255,255,255,0.04) !important; }
    .dataframe tr:hover { background: rgba(255,255,255,0.03) !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 1.5rem; background: transparent; border-bottom: 2px solid rgba(255,255,255,0.06); }
    .stTabs [data-baseweb="tab"] { font-weight: 500; color: #94A3B8; padding: 0.6rem 0; font-size: 1rem; border-bottom: 2px solid transparent; transition: all 0.2s; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #60A5FA; border-bottom: 2px solid #60A5FA; }
    .stNumberInput input, .stFileUploader > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: #E8EDF5 !important;
        padding: 0.6rem 1rem !important;
    }
    .stNumberInput input:focus { border-color: #3B82F6 !important; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important; }
    .stAlert { border-radius: 16px !important; background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.06) !important; backdrop-filter: blur(8px); }
    .footer { margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.06); text-align: center; font-size: 0.85rem; color: #64748B; }
    .footer span { color: #93C5FD; }
    @media (max-width: 768px) {
        .main-container { padding: 1rem; }
        .app-title { font-size: 2rem; }
        .app-header { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ─── Danh sách câu nói ──────────────────────────────────────────
LINHBAO_SAYINGS = [
    "Chào tiểu thư! Tôi là Linh Bảo đây! 🐼",
    "Sẵn sàng tìm hành tinh mới chưa? 🚀",
    "Hãy upload file CSV hoặc nhập thông số nhé!",
    "Tiểu thư thông minh quá! 😊",
    "Tôi ở đây để giúp tiểu thư mọi lúc!",
    "Woohoo! Lại một hành tinh tiềm năng! 🌟",
    "Tiểu thư có tin vào người ngoài hành tinh không?",
    "Khám phá vũ trụ thật thú vị phải không? ✨",
    "Cố lên! Dữ liệu đang chờ chúng ta! 💪",
    "Nếu cần giúp, cứ gọi tôi nhé!",
    "AstroMine-X – sản phẩm đỉnh cao! 😎",
    "Hãy nhìn lên bầu trời và mơ ước! 🌌"
]

# ─── Hàm tạo Linh Bảo bằng components.html ─────────────────────
def show_linhbao():
    sayings_json = json.dumps(LINHBAO_SAYINGS)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                background: transparent;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                font-family: 'Inter', sans-serif;
            }}
            .linhbao-wrapper {{
                position: relative;
                display: flex;
                flex-direction: column;
                align-items: center;
                cursor: pointer;
                user-select: none;
                transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            }}
            .linhbao-wrapper:hover {{
                transform: scale(1.05);
            }}
            .linhbao-bubble {{
                background: #1E293B;
                color: #E8EDF5;
                padding: 10px 18px;
                border-radius: 20px 20px 20px 4px;
                font-size: 0.85rem;
                max-width: 200px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5);
                border: 1px solid rgba(255,255,255,0.08);
                margin-bottom: 10px;
                backdrop-filter: blur(8px);
                text-align: center;
                line-height: 1.4;
                transition: all 0.3s ease;
            }}
            .linhbao-avatar {{
                width: 72px;
                height: 72px;
                border-radius: 50%;
                background: linear-gradient(135deg, #3B82F6, #8B5CF6);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.8rem;
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
                transition: all 0.3s ease;
                animation: float 4s ease-in-out infinite;
                border: 2px solid rgba(255,255,255,0.1);
            }}
            .linhbao-avatar:active {{
                transform: scale(0.92);
            }}
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-12px); }}
            }}
            .linhbao-speaking .linhbao-avatar {{
                animation: speak 0.5s ease 3;
            }}
            @keyframes speak {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.15) rotate(-5deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="linhbao-wrapper" id="linhbaoWrapper" onclick="linhBaoSpeak()">
            <div class="linhbao-bubble" id="linhbaoBubble">Chào tiểu thư! Click vào tôi nhé 🐾</div>
            <div class="linhbao-avatar" id="linhbaoAvatar">🐼</div>
        </div>
        <script>
            const sayings = {sayings_json};
            const bubble = document.getElementById('linhbaoBubble');
            const avatar = document.getElementById('linhbaoAvatar');
            const wrapper = document.getElementById('linhbaoWrapper');

            function linhBaoSpeak() {{
                const randomIndex = Math.floor(Math.random() * sayings.length);
                const msg = sayings[randomIndex];
                bubble.textContent = msg;
                avatar.classList.remove('linhbao-speaking');
                // Force reflow để animation chạy lại
                void avatar.offsetWidth;
                avatar.classList.add('linhbao-speaking');
            }}

            // Lời chào sau 2 giây
            setTimeout(() => {{
                bubble.textContent = 'Tiểu thư, tôi là Linh Bảo! Rất vui được đồng hành cùng bạn! 🐼✨';
            }}, 2000);

            // Hiệu ứng hover hint
            wrapper.addEventListener('mouseenter', () => {{
                if (!bubble.textContent.includes('Click')) {{
                    bubble.textContent = '👆 Click vào tôi để trò chuyện!';
                    setTimeout(() => {{
                        if (bubble.textContent === '👆 Click vào tôi để trò chuyện!') {{
                            bubble.textContent = sayings[Math.floor(Math.random() * sayings.length)];
                        }}
                    }}, 1500);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Dùng components.html với chiều cao cố định để không chiếm quá nhiều không gian
    st.components.v1.html(html_code, height=200, scrolling=False)

# ─── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:1.5rem;">
            <span style="font-size:2rem;">🪐</span>
            <span style="font-size:1.2rem; font-weight:700;">AstroMine-X</span>
        </div>
        <div class="sidebar-text">
            <strong style="color:#E8EDF5;">Phát hiện ngoại hành tinh</strong> từ dữ liệu TESS với AI &amp; Linh Bảo.
        </div>
        <div class="sidebar-divider"></div>
        <div class="sidebar-title">📖 Hướng dẫn</div>
        <div class="sidebar-text">
            <ol style="padding-left:1.2rem; margin:0.5rem 0;">
                <li>Tải lên CSV (6 cột)</li>
                <li>Hoặc nhập thông số</li>
                <li>Nhấn <strong>Phân tích</strong></li>
            </ol>
            <p style="margin-top:0.8rem;">
                <span style="color:#93C5FD;">Độ chính xác:</span> 85.56%<br>
                <span style="color:#93C5FD;">Mô hình:</span> LightGBM
            </p>
        </div>
        <div class="sidebar-divider"></div>
        <div class="sidebar-text" style="font-size:0.8rem; color:#64748B;">
            Phiên bản 3.0 · © 2026<br>
            Thiết kế bởi <span style="color:#93C5FD;">Linh Bảo</span> &amp; Team
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Hiển thị Linh Bảo ──────────────────────────────────────────
show_linhbao()

# ─── Nội dung chính ──────────────────────────────────────────────
st.markdown("""
<div class="main-container">
    <div class="app-header">
        <div>
            <div class="app-title">🪐 AstroMine-X</div>
            <div class="app-subtitle">Khám phá ngoại hành tinh với trí tuệ nhân tạo</div>
        </div>
        <div class="app-badge">⚡ AI-powered · TESS · v3.0</div>
    </div>
""", unsafe_allow_html=True)

# ─── Load model ──────────────────────────────────────────────────
try:
    model = joblib.load("planet_model_lgb_fixed.pkl")
    scaler = joblib.load("scaler_lgb_fixed.pkl")
    st.markdown("""
    <div class="card" style="border-left: 4px solid #3B82F6; padding:0.8rem 1.5rem; background:rgba(59,130,246,0.05);">
        <span style="color:#93C5FD;">✅ Model & Scaler đã được tải thành công</span>
    </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"❌ Lỗi tải model: {e}")
    st.stop()

# ─── Tabs ────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📂 Tải file CSV", "✏️ Nhập thủ công"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📁</span> Tải lên dữ liệu hành tinh</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Chọn file CSV (đúng 6 cột)", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(10), use_container_width=True)
        if st.button("🔍 Phân tích", key="analyze_csv", use_container_width=True):
            feature_cols = ['pl_orbper', 'pl_radj', 'pl_bmasse', 'pl_orbincl', 'st_teff', 'st_logg']
            missing = [col for col in feature_cols if col not in df.columns]
            if missing:
                st.error(f"❌ Thiếu các cột: {missing}. Vui lòng kiểm tra file.")
                st.stop()
            X = df[feature_cols].copy()
            X = X.fillna(X.mean())
            X_scaled = scaler.transform(X)
            proba = model.predict_proba(X_scaled)[:, 1]
            df_result = df.copy()
            df_result['Confidence'] = np.round(proba, 3)
            
            st.markdown("#### 📊 Kết quả dự đoán")
            st.dataframe(df_result[['Confidence']], use_container_width=True)
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(df_result['Confidence'], bins=20, color='#60A5FA', edgecolor='#1E293B', alpha=0.8)
            ax.set_xlabel('Độ tin cậy', color='#94A3B8')
            ax.set_ylabel('Số lượng', color='#94A3B8')
            ax.set_title('Phân bố độ tin cậy', color='#E8EDF5')
            ax.tick_params(colors='#94A3B8')
            ax.spines['bottom'].set_color('#334155')
            ax.spines['left'].set_color('#334155')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_facecolor('transparent')
            fig.patch.set_facecolor('transparent')
            st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">✏️</span> Nhập thông số hành tinh</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        orbper = st.number_input('🔄 Chu kỳ (ngày)', value=5.0, step=0.1, format="%.2f")
        radj = st.number_input('📏 Bán kính (Rjup)', value=1.2, step=0.1, format="%.2f")
        bmasse = st.number_input('⚖️ Khối lượng (Mjup)', value=2.5, step=0.1, format="%.2f")
    with col2:
        orbincl = st.number_input('📐 Độ nghiêng (độ)', value=85.0, step=0.5, format="%.1f")
        st_teff = st.number_input('🌡️ Nhiệt độ sao (K)', value=5500.0, step=100.0, format="%.0f")
        st_logg = st.number_input('📊 log(g) (cm/s²)', value=4.2, step=0.1, format="%.2f")
    
    if st.button("🔮 Dự đoán", key="predict_manual", use_container_width=True):
        input_data = np.array([[orbper, radj, bmasse, orbincl, st_teff, st_logg]])
        input_scaled = scaler.transform(input_data)
        proba = model.predict_proba(input_scaled)[0][1]
        
        st.markdown("#### Kết quả")
        if proba > 0.5:
            st.success(f"✅ **CÓ HÀNH TINH!** Độ tin cậy: {proba*100:.2f}%")
            st.balloons()
        else:
            st.warning(f"❌ **KHÔNG CÓ HÀNH TINH.** Độ tin cậy: {proba*100:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🚀 AstroMine-X v3.0 · Phát triển với ❤️ và sự đồng hành của <span>Linh Bảo</span> 🐼<br>
    Dữ liệu từ sứ mệnh TESS · NASA
</div>
</div>
""", unsafe_allow_html=True)
