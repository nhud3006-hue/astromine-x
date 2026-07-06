import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import requests
from io import StringIO
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ─── Cấu hình trang ──────────────────────────────────────────────
st.set_page_config(
    page_title="🪐 AstroMine-X Pro",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS cao cấp ──────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .stApp {
        background: #0a0e1a;
        background-image: radial-gradient(ellipse at 20% 50%, rgba(72,0,255,0.08) 0%, transparent 50%),
                          radial-gradient(ellipse at 80% 50%, rgba(0,200,255,0.05) 0%, transparent 50%);
    }
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ffc 50%, #ff6fd8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(0,212,255,0.3);
        letter-spacing: 0.05em;
        padding: 1.5rem 0 0.5rem;
        animation: glowPulse 3s ease-in-out infinite;
    }
    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 30px rgba(0,212,255,0.3); }
        50% { text-shadow: 0 0 60px rgba(123,47,252,0.5); }
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 300;
        color: #8892b0;
        text-align: center;
        letter-spacing: 0.15em;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 1.5rem;
    }
    .card {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 24px;
        padding: 1.8rem 2rem;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 40px rgba(0,0,0,0.6);
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        margin-bottom: 1.8rem;
    }
    .card:hover {
        border-color: rgba(0,212,255,0.2);
        box-shadow: 0 12px 56px rgba(0,0,0,0.8);
        transform: translateY(-2px);
    }
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: #e6f1ff;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    .card-title .icon { font-size: 1.6rem; }
    .css-1d391kg, .css-12oz5g7 {
        background: rgba(10,14,26,0.9) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    .sidebar-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
        color: #64ffda;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
    .sidebar-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #a8b2d1;
        line-height: 1.7;
    }
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ffc 100%) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.7rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0,212,255,0.3) !important;
        letter-spacing: 0.02em;
    }
    .stButton button:hover {
        transform: scale(1.04) translateY(-3px) !important;
        box-shadow: 0 8px 40px rgba(0,212,255,0.5) !important;
    }
    .stButton button:active { transform: scale(0.96) !important; }
    .stNumberInput input, .stTextArea textarea, .stFileUploader > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        color: #e6f1ff !important;
        padding: 0.8rem 1.2rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s;
    }
    .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 4px rgba(0,212,255,0.15) !important;
    }
    .dataframe {
        background: transparent !important;
        color: #e6f1ff !important;
        border-collapse: collapse !important;
        font-family: 'Inter', sans-serif !important;
    }
    .dataframe th {
        background: rgba(0,212,255,0.08) !important;
        color: #64ffda !important;
        font-weight: 600 !important;
        padding: 0.8rem !important;
        border-bottom: 2px solid rgba(0,212,255,0.15) !important;
    }
    .dataframe td {
        padding: 0.8rem !important;
        border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    }
    .dataframe tr:hover td {
        background: rgba(0,212,255,0.04) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
        border-bottom: 2px solid rgba(255,255,255,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #8892b0;
        padding: 0.6rem 0;
        font-size: 1rem;
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #64ffda;
        border-bottom: 2px solid #64ffda;
    }
    .stAlert {
        border-radius: 16px !important;
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        backdrop-filter: blur(8px);
    }
    .stAlert .st-emotion-cache-1wmy9hl { color: #e6f1ff !important; }
    .footer {
        margin-top: 4rem;
        padding: 2rem 0 1rem;
        border-top: 1px solid rgba(255,255,255,0.04);
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #495670;
        letter-spacing: 0.05em;
    }
    .footer span { color: #64ffda; }
    @media (max-width: 768px) {
        .main-header { font-size: 2.4rem; }
        .card { padding: 1.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# ─── Linh Bảo ────────────────────────────────────────────────────
LINHBAO_SAYINGS = [
    "Chào tiểu thư! Em là Linh Bảo đây! 🐼",
    "Sẵn sàng săn hành tinh chưa? 🚀",
    "Dán dữ liệu hoặc tải CSV lên nhé!",
    "Tiểu thư thông minh quá đi! 😊",
    "Em luôn đồng hành cùng tiểu thư!",
    "Woohoo! Lại một hành tinh mới! 🌟",
    "Bí mật vũ trụ đang chờ chúng ta!",
    "Khám phá thôi nào! ✨",
    "Cố lên, sắp có kết quả rồi! 💪",
    "Nếu cần gì, cứ gọi em nhé!",
    "AstroMine-X là đỉnh cao! 😎",
    "Hãy luôn mơ ước, tiểu thư! 🌌"
]

def show_linhbao():
    sayings_json = json.dumps(LINHBAO_SAYINGS)
    html = f"""
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
            pointer-events: none;
        }}
        .wrapper {{
            pointer-events: auto;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            user-select: none;
        }}
        .wrapper:hover {{ transform: scale(1.05); }}
        .bubble {{
            background: rgba(20,30,50,0.85);
            backdrop-filter: blur(12px);
            color: #e6f1ff;
            padding: 10px 16px;
            border-radius: 20px 20px 20px 4px;
            font-size: 0.8rem;
            max-width: 160px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.6);
            border: 1px solid rgba(0,212,255,0.15);
            margin-bottom: 10px;
            text-align: center;
            line-height: 1.4;
            transition: all 0.3s;
        }}
        .avatar {{
            width: 68px;
            height: 68px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00d4ff, #7b2ffc);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.6rem;
            box-shadow: 0 8px 32px rgba(0,212,255,0.3);
            animation: float 4s ease-in-out infinite;
            border: 2px solid rgba(255,255,255,0.1);
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        .speaking .avatar {{
            animation: speak 0.5s ease 3;
        }}
        @keyframes speak {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.15) rotate(-4deg); }}
        }}
    </style>
    </head>
    <body>
    <div class="wrapper" onclick="say()">
        <div class="bubble" id="bubble">🐼 Click vào em!</div>
        <div class="avatar" id="avatar">🐼</div>
    </div>
    <script>
        const sayings = {sayings_json};
        const bubble = document.getElementById('bubble');
        const avatar = document.getElementById('avatar');
        const wrapper = document.querySelector('.wrapper');

        function say() {{
            const idx = Math.floor(Math.random() * sayings.length);
            bubble.textContent = sayings[idx];
            avatar.classList.remove('speaking');
            void avatar.offsetWidth;
            avatar.classList.add('speaking');
        }}

        setTimeout(() => {{
            bubble.textContent = 'Tiểu thư, em đây! 🌟';
        }}, 2000);

        wrapper.addEventListener('mouseenter', () => {{
            if (!bubble.textContent.includes('Click')) {{
                bubble.textContent = '👆 Click để nói chuyện!';
                setTimeout(() => {{
                    if (bubble.textContent === '👆 Click để nói chuyện!') {{
                        bubble.textContent = sayings[Math.floor(Math.random() * sayings.length)];
                    }}
                }}, 1500);
            }}
        }});
    </script>
    </body>
    </html>
    """
    st.components.v1.html(html, height=220, scrolling=False)

# ─── Load model ──────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        model = joblib.load("planet_model_lgb_fixed.pkl")
        scaler = joblib.load("scaler_lgb_fixed.pkl")
        return model, scaler
    except:
        return None, None

model, scaler = load_model()
if model is None:
    st.error("❌ Không tìm thấy model. Vui lòng đảm bảo có file 'planet_model_lgb_fixed.pkl' và 'scaler_lgb_fixed.pkl'.")
    st.stop()

# ─── Hàm lưu / tải bảng xếp hạng ──────────────────────────────
RANKING_FILE = "rankings.json"

def load_rankings():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_rankings(rankings):
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=2, ensure_ascii=False)

# ─── KHỞI TẠO SESSION_STATE AN TOÀN ─────────────────────────────
# Sử dụng get để tránh lỗi AttributeError nếu chưa có key
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'rankings' not in st.session_state:
    st.session_state.rankings = load_rankings()
if 'nasa_data' not in st.session_state:
    st.session_state.nasa_data = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'paste_default' not in st.session_state:
    st.session_state.paste_default = ""

# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1.5rem;">
        <span style="font-size:2.2rem;">🪐</span>
        <span style="font-family:'Orbitron',sans-serif; font-size:1.1rem; font-weight:700; color:#64ffda;">AstroMine-X</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">🔐 Tài khoản</div>', unsafe_allow_html=True)
    if not st.session_state.logged_in:
        username = st.text_input("Tên", placeholder="Nhập tên của bạn", key="login_name")
        if st.button("🚀 Đăng nhập / Đăng ký", use_container_width=True):
            if username.strip():
                st.session_state.username = username.strip()
                st.session_state.logged_in = True
                if st.session_state.username not in st.session_state.rankings:
                    st.session_state.rankings[st.session_state.username] = 0
                    save_rankings(st.session_state.rankings)
                st.success(f"✅ Chào {st.session_state.username}!")
                st.rerun()
            else:
                st.warning("Vui lòng nhập tên!")
    else:
        st.success(f"👋 {st.session_state.username}")
        st.write(f"🏆 **Điểm**: {st.session_state.rankings.get(st.session_state.username, 0)}")
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    st.markdown("---")
    st.markdown('<div class="sidebar-title">📖 Hướng dẫn</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-text">
        <strong>3 cách nhập:</strong><br>
        1️⃣ Dán CSV<br>
        2️⃣ Tải CSV<br>
        3️⃣ NASA (có fallback)
        <br><br>
        <strong>Độ chính xác:</strong> 85.56%<br>
        <strong>Mô hình:</strong> LightGBM
        <br><br>
        <span style="color:#64ffda;">💡 Kéo thanh trượt ở tab "Dự đoán nhanh" để thử ngay.</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Hiển thị Linh Bảo ─────────────────────────────────────────
show_linhbao()

# ─── Header chính ──────────────────────────────────────────────
st.markdown('<div class="main-header">🪐 AstroMine-X Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">✨ Khám phá ngoại hành tinh với AI • Dữ liệu TESS • Linh Bảo 🐼</div>', unsafe_allow_html=True)

# ─── Hàm phân tích chung ──────────────────────────────────────
def analyze_data(df, show_chart=True, update_score=True):
    feature_cols = ['pl_orbper', 'pl_radj', 'pl_bmasse', 'pl_orbincl', 'st_teff', 'st_logg']
    # Nếu có cột khác tương ứng
    rename_map = {}
    for col in df.columns:
        if col.lower() in ['pl_bmassj', 'pl_bmass'] and 'pl_bmasse' not in df.columns:
            rename_map[col] = 'pl_bmasse'
    if rename_map:
        df = df.rename(columns=rename_map)
    
    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        st.error(f"❌ Thiếu các cột: {missing}. Vui lòng kiểm tra dữ liệu.")
        return None
    
    X = df[feature_cols].copy()
    X = X.fillna(X.mean())
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[:, 1]
    df_result = df.copy()
    df_result['Confidence'] = np.round(proba, 3)
    df_result['Prediction'] = (proba > 0.5).astype(int)
    n_planets = int((proba > 0.5).sum())
    
    st.subheader(f"📊 Kết quả – {len(df_result)} ứng viên, {n_planets} hành tinh tiềm năng")
    st.dataframe(df_result[['Confidence', 'Prediction']], use_container_width=True)
    
    if show_chart:
        fig = px.histogram(
            df_result, x='Confidence', nbins=30,
            title='Phân bố độ tin cậy',
            color_discrete_sequence=['#00d4ff'],
            labels={'Confidence': 'Độ tin cậy', 'count': 'Số lượng'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#a8b2d1',
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            height=350
        )
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig, use_container_width=True)
    
    if update_score and st.session_state.logged_in:
        current_score = st.session_state.rankings.get(st.session_state.username, 0)
        if n_planets > current_score:
            st.session_state.rankings[st.session_state.username] = n_planets
            save_rankings(st.session_state.rankings)
            st.success(f"🎉 Cập nhật điểm: {n_planets} hành tinh (kỷ lục mới!)")
        else:
            st.info(f"📌 Điểm hiện tại: {current_score} – lần này tìm được {n_planets} hành tinh.")
    
    # Lưu lịch sử (an toàn)
    history = st.session_state.history
    history.append({
        'time': datetime.now().strftime("%H:%M:%S"),
        'n_candidates': len(df_result),
        'n_planets': n_planets,
        'user': st.session_state.username if st.session_state.logged_in else 'Anonymous'
    })
    st.session_state.history = history
    return df_result

# ─── Các tab ────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Dán CSV",
    "📂 Tải CSV",
    "🌐 NASA",
    "🎯 Dự đoán nhanh",
    "📊 Thống kê",
    "🏆 Bảng xếp hạng"
])

# ─── Tab 1: Dán ─────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📝</span> Dán trực tiếp dữ liệu</div>', unsafe_allow_html=True)
    example = """pl_orbper,pl_radj,pl_bmasse,pl_orbincl,st_teff,st_logg
1.17,1.187,2.36,89.9,5613.0,4.200
3.23,1.169,1.89,88.93,5647.0,4.236
5.47,0.987,0.56,89.95,5626.0,4.100
0.82,0.456,0.12,88.50,5780.0,4.500
2.15,0.789,0.45,87.50,5500.0,4.100"""
    with st.expander("📋 Lấy dữ liệu mẫu"):
        st.code(example, language="text")
        if st.button("📥 Điền mẫu", key="sample_paste"):
            st.session_state.paste_default = example
            st.rerun()
    default_text = st.session_state.get('paste_default', '')
    pasted = st.text_area("✏️ Dán dữ liệu (CSV, dấu phẩy hoặc tab)", value=default_text, height=200)
    if st.button("🔍 Phân tích", key="btn_paste"):
        if pasted.strip():
            try:
                df = pd.read_csv(StringIO(pasted), sep=None, engine='python')
                analyze_data(df)
            except Exception as e:
                st.error(f"❌ Lỗi đọc: {e}")
        else:
            st.warning("Vui lòng dán dữ liệu!")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Tab 2: Tải CSV ────────────────────────────────────────────
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📂</span> Tải file CSV</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Chọn file CSV (6 cột)", type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head(), use_container_width=True)
        if st.button("🔍 Phân tích", key="btn_csv"):
            analyze_data(df)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Tab 3: NASA (đã sửa lỗi) ──────────────────────────────────
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">🌐</span> Tải dữ liệu từ NASA</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(0,212,255,0.05); border-radius:12px; padding:0.8rem 1.2rem; margin-bottom:1rem; border-left:3px solid #00d4ff;">
        📡 Tải dữ liệu ứng viên hành tinh mới nhất từ <b>NASA Exoplanet Archive</b>.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("📥 Tải dữ liệu NASA", key="btn_nasa"):
            with st.spinner("Đang kết nối NASA..."):
                try:
                    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
                    params = {
                        "query": "SELECT pl_orbper, pl_radj, pl_bmassj, pl_orbincl, st_teff, st_logg FROM ps",
                        "format": "csv"
                    }
                    response = requests.get(url, params=params, timeout=30)
                    if response.status_code == 200:
                        df_nasa = pd.read_csv(StringIO(response.text))
                        st.session_state.nasa_data = df_nasa
                        st.success(f"✅ Đã tải {len(df_nasa)} ứng viên!")
                        st.dataframe(df_nasa.head(), use_container_width=True)
                    else:
                        st.error(f"❌ HTTP {response.status_code}: {response.text[:200]}")
                        st.info("💡 Sử dụng dữ liệu mẫu bên dưới.")
                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")
                    st.info("💡 Sử dụng dữ liệu mẫu bên dưới.")
    
    with col2:
        if st.button("📦 Dữ liệu mẫu", key="sample_nasa"):
            sample = """pl_orbper,pl_radj,pl_bmassj,pl_orbincl,st_teff,st_logg
1.17,1.187,2.36,89.9,5613.0,4.200
3.23,1.169,1.89,88.93,5647.0,4.236
5.47,0.987,0.56,89.95,5626.0,4.100
0.82,0.456,0.12,88.50,5780.0,4.500
2.15,0.789,0.45,87.50,5500.0,4.100"""
            df_sample = pd.read_csv(StringIO(sample))
            st.session_state.nasa_data = df_sample
            st.success("✅ Đã tải mẫu (5 ứng viên)!")
            st.dataframe(df_sample.head(), use_container_width=True)
    
    if st.session_state.nasa_data is not None:
        if st.button("🔍 Phân tích dữ liệu NASA", key="btn_analyze_nasa"):
            analyze_data(st.session_state.nasa_data)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Tab 4: Dự đoán nhanh ──────────────────────────────────────
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">🎯</span> Dự đoán nhanh – Kéo thanh trượt</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        orbper = st.slider('🔄 Chu kỳ (ngày)', 0.1, 50.0, 5.0, 0.1)
        radj = st.slider('📏 Bán kính (Rjup)', 0.1, 5.0, 1.2, 0.01)
        bmasse = st.slider('⚖️ Khối lượng (Mjup)', 0.01, 20.0, 2.5, 0.01)
    with col2:
        orbincl = st.slider('📐 Độ nghiêng (độ)', 10, 90, 85, 1)
        st_teff = st.slider('🌡️ Nhiệt độ sao (K)', 3000, 8000, 5500, 100)
        st_logg = st.slider('📊 log(g) (cm/s²)', 3.0, 5.5, 4.2, 0.01)
    
    if st.button("🔮 Dự đoán", key="btn_slider"):
        input_data = np.array([[orbper, radj, bmasse, orbincl, st_teff, st_logg]])
        input_scaled = scaler.transform(input_data)
        proba = model.predict_proba(input_scaled)[0][1]
        st.markdown("### Kết quả")
        if proba > 0.5:
            st.success(f"✅ **CÓ HÀNH TINH!** Độ tin cậy: {proba*100:.2f}%")
            st.balloons()
        else:
            st.warning(f"❌ **KHÔNG CÓ HÀNH TINH.** Độ tin cậy: {proba*100:.2f}%")
        # Đồng hồ đo
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=proba*100,
            title={'text': "Độ tin cậy (%)", 'font': {'color': '#a8b2d1'}},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#a8b2d1'},
                'bar': {'color': '#7b2ffc' if proba>0.5 else '#ff6fd8'},
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(255,100,100,0.15)'},
                    {'range': [50, 100], 'color': 'rgba(0,212,255,0.15)'}
                ],
                'threshold': {
                    'line': {'color': '#64ffda', 'width': 4},
                    'thickness': 0.75,
                    'value': proba*100
                }
            }
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#a8b2d1',
            height=300,
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Tab 5: Thống kê ────────────────────────────────────────────
with tab5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📊</span> Thống kê tổng quan</div>', unsafe_allow_html=True)
    if len(st.session_state.history) > 0:
        hist_df = pd.DataFrame(st.session_state.history)
        st.dataframe(hist_df, use_container_width=True)
        fig = px.line(hist_df, x='time', y='n_planets', title='Số hành tinh phát hiện theo thời gian',
                      labels={'time': 'Thời gian', 'n_planets': 'Số hành tinh'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#a8b2d1')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 Chưa có lịch sử phân tích. Hãy bắt đầu dự đoán!")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Tab 6: Bảng xếp hạng ──────────────────────────────────────
with tab6:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">🏆</span> Bảng xếp hạng</div>', unsafe_allow_html=True)
    rankings = st.session_state.rankings
    if rankings:
        sorted_rank = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
        rank_df = pd.DataFrame(sorted_rank, columns=['Người dùng', 'Điểm'])
        rank_df.index = rank_df.index + 1
        rank_df.index.name = 'Hạng'
        if st.session_state.logged_in:
            current = st.session_state.username
            rank_df[''] = rank_df['Người dùng'].apply(lambda x: '⭐' if x == current else '')
        st.dataframe(rank_df, use_container_width=True)
        top10 = sorted_rank[:10]
        if top10:
            fig = px.bar(x=[u[0] for u in top10], y=[u[1] for u in top10],
                         title="Top 10 Thợ săn hành tinh",
                         labels={'x': 'Người dùng', 'y': 'Điểm'})
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font_color='#a8b2d1', showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 Chưa có người dùng. Hãy đăng nhập và săn hành tinh!")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🚀 AstroMine-X Pro · v3.2 · Phát triển với ❤️ và Linh Bảo 🐼<br>
    Dữ liệu từ NASA Exoplanet Archive · © 2026
</div>
""", unsafe_allow_html=True)
