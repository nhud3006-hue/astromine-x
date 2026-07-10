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

# ─── Linh Bảo bay nhảy ────────────────────────────────────────────
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
            overflow: hidden;
            width: 100vw;
            height: 100vh;
            font-family: 'Inter', sans-serif;
            pointer-events: none;
        }}
        .wrapper {{
            position: fixed;
            top: 50px;
            left: 50px;
            pointer-events: auto;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: all 0.1s linear;
            user-select: none;
            z-index: 99999;
        }}
        .wrapper:hover {{ transform: scale(1.05); }}
        .bubble {{
            background: rgba(20,30,50,0.85);
            backdrop-filter: blur(12px);
            color: #e6f1ff;
            padding: 8px 14px;
            border-radius: 20px 20px 20px 4px;
            font-size: 0.75rem;
            max-width: 150px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.6);
            border: 1px solid rgba(0,212,255,0.15);
            margin-bottom: 8px;
            text-align: center;
            line-height: 1.3;
            transition: all 0.3s;
            white-space: nowrap;
        }}
        .avatar {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00d4ff, #7b2ffc);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2rem;
            box-shadow: 0 8px 32px rgba(0,212,255,0.3);
            animation: float 4s ease-in-out infinite;
            border: 2px solid rgba(255,255,255,0.1);
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-8px); }}
        }}
        .speaking .avatar {{
            animation: speak 0.5s ease 3;
        }}
        @keyframes speak {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.15) rotate(-4deg); }}
        }}
        .bouncing {{
            animation: bounce 0.3s ease;
        }}
        @keyframes bounce {{
            0% {{ transform: scale(1); }}
            30% {{ transform: scale(1.3) rotate(10deg); }}
            60% {{ transform: scale(0.9) rotate(-5deg); }}
            100% {{ transform: scale(1); }}
        }}
    </style>
    </head>
    <body>
    <div class="wrapper" id="wrapper" onclick="say()">
        <div class="bubble" id="bubble">🐼 Click vào em!</div>
        <div class="avatar" id="avatar">🐼</div>
    </div>
    <script>
        const sayings = {sayings_json};
        const wrapper = document.getElementById('wrapper');
        const bubble = document.getElementById('bubble');
        const avatar = document.getElementById('avatar');

        let vx = 1.2, vy = 0.8;
        let x = 50, y = 50;
        let lastBubbleText = '';

        function move() {{
            const w = window.innerWidth - 120;
            const h = window.innerHeight - 160;

            x += vx; y += vy;

            if (x > w) {{ x = w; vx = -vx; bounceEffect(); sayRandom(); }}
            if (x < 0) {{ x = 0; vx = -vx; bounceEffect(); sayRandom(); }}
            if (y > h) {{ y = h; vy = -vy; bounceEffect(); sayRandom(); }}
            if (y < 0) {{ y = 0; vy = -vy; bounceEffect(); sayRandom(); }}

            wrapper.style.left = x + 'px';
            wrapper.style.top = y + 'px';

            if (Math.random() < 0.005) {{
                vx += (Math.random() - 0.5) * 0.8;
                vy += (Math.random() - 0.5) * 0.8;
                const sp = Math.sqrt(vx*vx + vy*vy);
                if (sp > 2.5) {{ vx = (vx/sp)*2.5; vy = (vy/sp)*2.5; }}
                if (sp < 0.6) {{ vx = (vx/sp)*0.8 || 1.2; vy = (vy/sp)*0.8 || 0.8; }}
            }}
        }}

        function bounceEffect() {{
            avatar.classList.add('bouncing');
            setTimeout(() => avatar.classList.remove('bouncing'), 400);
        }}

        function sayRandom() {{
            const idx = Math.floor(Math.random() * sayings.length);
            const msg = sayings[idx];
            if (msg !== lastBubbleText) {{
                bubble.textContent = msg;
                lastBubbleText = msg;
            }}
            avatar.classList.remove('speaking');
            void avatar.offsetWidth;
            avatar.classList.add('speaking');
        }}

        function say() {{
            const idx = Math.floor(Math.random() * sayings.length);
            const msg = sayings[idx];
            bubble.textContent = msg;
            lastBubbleText = msg;
            avatar.classList.remove('speaking');
            void avatar.offsetWidth;
            avatar.classList.add('speaking');
            vx = (Math.random() - 0.5) * 4;
            vy = (Math.random() - 0.5) * 4;
        }}

        setTimeout(() => {{
            bubble.textContent = 'Tiểu thư, em đang bay đây! 🌟';
            lastBubbleText = 'Tiểu thư, em đang bay đây! 🌟';
        }}, 1500);

        setInterval(move, 30);

        wrapper.addEventListener('mouseenter', () => {{
            if (!bubble.textContent.includes('Click')) {{
                const old = bubble.textContent;
                bubble.textContent = '👆 Click để trò chuyện!';
                setTimeout(() => {{
                    if (bubble.textContent === '👆 Click để trò chuyện!') {{
                        bubble.textContent = sayings[Math.floor(Math.random() * sayings.length)];
                    }}
                }}, 1200);
            }}
        }});

        avatar.addEventListener('click', (e) => {{
            e.stopPropagation();
            say();
        }});

        console.log('🐼 Linh Bảo đã sẵn sàng bay nhảy!');
    </script>
    </body>
    </html>
    """
    st.components.v1.html(html, height=0, scrolling=False)

# ─── Load model (sửa lỗi) ────────────────────────────────────────
@st.cache_resource
def load_model():
    # Tìm file model ở nhiều đường dẫn
    possible_paths = [
        "planet_model_lgb_fixed.pkl",
        "./planet_model_lgb_fixed.pkl",
        "../planet_model_lgb_fixed.pkl",
        "models/planet_model_lgb_fixed.pkl",
        "/mount/src/astromine-x/planet_model_lgb_fixed.pkl",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "planet_model_lgb_fixed.pkl")
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        st.error("❌ Không tìm thấy file model!")
        st.info(f"📂 Thư mục hiện tại: {os.getcwd()}")
        st.info(f"📂 Các file trong thư mục: {', '.join(os.listdir('.')) if os.path.exists('.') else 'Không thể đọc'}")
        # Tạo model giả từ numpy (không cần sklearn)
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler
            np.random.seed(42)
            X_fake = np.random.randn(1000, 6)
            y_fake = (np.random.rand(1000) < 0.3).astype(int)
            model_fake = RandomForestClassifier(n_estimators=50, random_state=42)
            model_fake.fit(X_fake, y_fake)
            scaler_fake = StandardScaler()
            scaler_fake.fit(X_fake)
            st.warning("⚠️ Đang sử dụng model dự phòng (độ chính xác thấp, chỉ để demo).")
            return model_fake, scaler_fake
        except:
            st.error("❌ Không thể tạo model dự phòng. Vui lòng cài 'scikit-learn'.")
            return None, None
    
    try:
        scaler_path = model_path.replace("planet_model_lgb_fixed.pkl", "scaler_lgb_fixed.pkl")
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except Exception as e:
        st.error(f"❌ Lỗi load model: {e}")
        return None, None

model, scaler = load_model()
if model is None:
    st.stop()

# ─── Khởi tạo session_state an toàn ─────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'rankings' not in st.session_state:
    st.session_state.rankings = {}
if 'nasa_data' not in st.session_state:
    st.session_state.nasa_data = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'paste_default' not in st.session_state:
    st.session_state.paste_default = ""

RANKING_FILE = "rankings.json"
def load_rankings():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
def save_rankings(r):
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(r, f, indent=2, ensure_ascii=False)

if not st.session_state.rankings:
    st.session_state.rankings = load_rankings()

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
        username = st.text_input("Tên", placeholder="Nhập tên", key="login_name")
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
        3️⃣ NASA (có fallback)<br><br>
        <strong>Độ chính xác:</strong> 85.56%<br>
        <strong>Mô hình:</strong> LightGBM<br><br>
        <span style="color:#64ffda;">🐼 Linh Bảo đang bay nhảy quanh màn hình!</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Hiển thị Linh Bảo ─────────────────────────────────────────
show_linhbao()

# ─── Header ──────────────────────────────────────────────────────
st.markdown('<div class="main-header">🪐 AstroMine-X Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">✨ Khám phá ngoại hành tinh với AI • Dữ liệu TESS • Linh Bảo 🐼</div>', unsafe_allow_html=True)

# ─── Hàm phân tích ──────────────────────────────────────────────
def analyze_data(df, show_chart=True, update_score=True):
    feature_cols = ['pl_orbper', 'pl_radj', 'pl_bmasse', 'pl_orbincl', 'st_teff', 'st_logg']
    # Đổi tên cột nếu có
    for col in df.columns:
        if col.lower() in ['pl_bmassj', 'pl_bmass'] and 'pl_bmasse' not in df.columns:
            df = df.rename(columns={col: 'pl_bmasse'})
    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        st.error(f"❌ Thiếu cột: {missing}")
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
        fig = px.histogram(df_result, x='Confidence', nbins=30,
                           title='Phân bố độ tin cậy',
                           color_discrete_sequence=['#00d4ff'],
                           labels={'Confidence': 'Độ tin cậy', 'count': 'Số lượng'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font_color='#a8b2d1', showlegend=False, margin=dict(l=20,r=20,t=40,b=20), height=350)
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig, use_container_width=True)
    if update_score and st.session_state.logged_in:
        cur = st.session_state.rankings.get(st.session_state.username, 0)
        if n_planets > cur:
            st.session_state.rankings[st.session_state.username] = n_planets
            save_rankings(st.session_state.rankings)
            st.success(f"🎉 Cập nhật điểm: {n_planets} hành tinh (kỷ lục mới!)")
        else:
            st.info(f"📌 Điểm: {cur} – lần này: {n_planets} hành tinh")
    st.session_state.history.append({
        'time': datetime.now().strftime("%H:%M:%S"),
        'n_candidates': len(df_result),
        'n_planets': n_planets,
        'user': st.session_state.username if st.session_state.logged_in else 'Anonymous'
    })
    return df_result

# ─── Tabs ────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Dán CSV", "📂 Tải CSV", "🌐 NASA",
    "🎯 Dự đoán nhanh", "📊 Thống kê", "🏆 Bảng xếp hạng"
])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📝</span> Dán dữ liệu</div>', unsafe_allow_html=True)
    example = """pl_orbper,pl_radj,pl_bmasse,pl_orbincl,st_teff,st_logg
1.17,1.187,2.36,89.9,5613.0,4.200
3.23,1.169,1.89,88.93,5647.0,4.236
5.47,0.987,0.56,89.95,5626.0,4.100
0.82,0.456,0.12,88.50,5780.0,4.500
2.15,0.789,0.45,87.50,5500.0,4.100"""
    with st.expander("📋 Lấy mẫu"):
        st.code(example, language="text")
        if st.button("📥 Điền mẫu"):
            st.session_state.paste_default = example
            st.rerun()
    pasted = st.text_area("✏️ Dán dữ liệu", value=st.session_state.paste_default, height=200)
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

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📂</span> Tải CSV</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Chọn file CSV", type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head())
        if st.button("🔍 Phân tích", key="btn_csv"):
            analyze_data(df)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">🌐</span> NASA</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("📥 Tải từ NASA"):
            with st.spinner("Đang kết nối..."):
                try:
                    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
                    params = {"query": "SELECT pl_orbper,pl_radj,pl_bmassj,pl_orbincl,st_teff,st_logg FROM ps", "format": "csv"}
                    r = requests.get(url, params=params, timeout=30)
                    if r.status_code == 200:
                        df = pd.read_csv(StringIO(r.text))
                        st.session_state.nasa_data = df
                        st.success(f"✅ Đã tải {len(df)} ứng viên!")
                        st.dataframe(df.head())
                    else:
                        st.error(f"HTTP {r.status_code}: {r.text[:200]}")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
    with col2:
        if st.button("📦 Mẫu"):
            sample = """pl_orbper,pl_radj,pl_bmassj,pl_orbincl,st_teff,st_logg
1.17,1.187,2.36,89.9,5613.0,4.200
3.23,1.169,1.89,88.93,5647.0,4.236
5.47,0.987,0.56,89.95,5626.0,4.100
0.82,0.456,0.12,88.50,5780.0,4.500
2.15,0.789,0.45,87.50,5500.0,4.100"""
            df = pd.read_csv(StringIO(sample))
            st.session_state.nasa_data = df
            st.success("✅ Đã tải mẫu (5 ứng viên)!")
            st.dataframe(df.head())
    if st.session_state.nasa_data is not None:
        if st.button("🔍 Phân tích NASA"):
            analyze_data(st.session_state.nasa_data)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">🎯</span> Dự đoán nhanh</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        orbper = st.slider('🔄 Chu kỳ', 0.1, 50.0, 5.0, 0.1)
        radj = st.slider('📏 Bán kính', 0.1, 5.0, 1.2, 0.01)
        bmasse = st.slider('⚖️ Khối lượng', 0.01, 20.0, 2.5, 0.01)
    with c2:
        orbincl = st.slider('📐 Độ nghiêng', 10, 90, 85, 1)
        st_teff = st.slider('🌡️ Nhiệt độ sao', 3000, 8000, 5500, 100)
        st_logg = st.slider('📊 log(g)', 3.0, 5.5, 4.2, 0.01)
    if st.button("🔮 Dự đoán"):
        inp = np.array([[orbper, radj, bmasse, orbincl, st_teff, st_logg]])
        inp_scaled = scaler.transform(inp)
        proba = model.predict_proba(inp_scaled)[0][1]
        if proba > 0.5:
            st.success(f"✅ CÓ HÀNH TINH! Độ tin cậy: {proba*100:.2f}%")
            st.balloons()
        else:
            st.warning(f"❌ KHÔNG CÓ HÀNH TINH. Độ tin cậy: {proba*100:.2f}%")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=proba*100,
            title={'text': "Độ tin cậy (%)", 'font': {'color': '#a8b2d1'}},
            domain={'x': [0,1], 'y': [0,1]},
            gauge={
                'axis': {'range': [0,100], 'tickcolor': '#a8b2d1'},
                'bar': {'color': '#7b2ffc' if proba>0.5 else '#ff6fd8'},
                'steps': [{'range': [0,50], 'color': 'rgba(255,100,100,0.15)'}, {'range': [50,100], 'color': 'rgba(0,212,255,0.15)'}],
                'threshold': {'line': {'color': '#64ffda', 'width': 4}, 'thickness': 0.75, 'value': proba*100}
            }
        ))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#a8b2d1', height=300, margin=dict(l=30,r=30,t=30,b=30))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📊</span> Thống kê</div>', unsafe_allow_html=True)
    if st.session_state.history:
        dfh = pd.DataFrame(st.session_state.history)
        st.dataframe(dfh)
        fig = px.line(dfh, x='time', y='n_planets', title='Số hành tinh theo thời gian')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#a8b2d1')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chưa có lịch sử.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab6:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">🏆</span> Bảng xếp hạng</div>', unsafe_allow_html=True)
    if st.session_state.rankings:
        sorted_rank = sorted(st.session_state.rankings.items(), key=lambda x: x[1], reverse=True)
        dfr = pd.DataFrame(sorted_rank, columns=['Người dùng', 'Điểm'])
        dfr.index = dfr.index + 1
        dfr.index.name = 'Hạng'
        if st.session_state.logged_in:
            dfr[''] = dfr['Người dùng'].apply(lambda x: '⭐' if x == st.session_state.username else '')
        st.dataframe(dfr)
        if len(sorted_rank) > 1:
            top = sorted_rank[:10]
            fig = px.bar(x=[u[0] for u in top], y=[u[1] for u in top], title='Top 10')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#a8b2d1', showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chưa có người dùng.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🚀 AstroMine-X Pro · v3.3 · Phát triển với ❤️ và Linh Bảo 🐼<br>
    Dữ liệu từ NASA Exoplanet Archive · © 2026
</div>
""", unsafe_allow_html=True)
