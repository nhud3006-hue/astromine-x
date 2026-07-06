import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import base64

# ==============================================================================
# 1. CẤU HÌNH TRANG & CSS TỔNG THỂ
# ==============================================================================
st.set_page_config(page_title="🚀 AstroMine-X | Phiên bản Linh Bảo", page_icon="🪐", layout="wide")

# CSS cho giao diện chính và con thú cưng
st.markdown("""
<style>
    /* Reset và font chữ */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
    html, body, .stApp {
        font-family: 'Quicksand', sans-serif;
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #2E4057;
        text-align: center;
        padding: 0.5rem 0 0.2rem 0;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6B7B8D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #F6F9FC;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #4A90E2;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    /* Container cho thú cưng */
    .pet-container {
        position: relative;
        width: 100%;
        height: 100px;
        background: linear-gradient(135deg, #e0eaf5 0%, #f5f9ff 100%);
        border-radius: 20px;
        margin: 20px 0 30px 0;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.8);
        overflow: hidden;
    }
    .pet-avatar {
        position: absolute;
        bottom: 0px;
        left: 10px;
        width: 80px;
        height: 80px;
        transition: left 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        z-index: 10;
        font-size: 3.8rem;
        line-height: 1;
        filter: drop-shadow(0 8px 12px rgba(0,0,0,0.1));
        cursor: pointer;
        user-select: none;
        animation: float 3s ease-in-out infinite;
    }
    /* Hiệu ứng bay lên nhẹ */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    /* Bong bóng thoại */
    .speech-bubble {
        position: absolute;
        bottom: 85px;
        left: 100px;
        background: white;
        padding: 10px 18px;
        border-radius: 30px 30px 30px 5px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        font-family: 'Quicksand', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        color: #2E4057;
        border: 1px solid rgba(74, 144, 226, 0.2);
        white-space: nowrap;
        max-width: 250px;
        opacity: 0;
        transition: opacity 0.4s ease, transform 0.3s ease;
        transform: translateY(5px);
        pointer-events: none;
    }
    .speech-bubble.show {
        opacity: 1;
        transform: translateY(0);
    }
    /* Các phần tử để tạo sân chơi */
    .ground-line {
        position: absolute;
        bottom: 20px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(to right, transparent, #cbd5e1, transparent);
        opacity: 0.4;
    }
    /* Nút thả tim */
    .hearts {
        position: absolute;
        bottom: 100px;
        left: 50%;
        font-size: 1.6rem;
        opacity: 0;
        transition: all 1s ease;
        pointer-events: none;
    }
    .hearts.show {
        opacity: 1;
        transform: translateY(-50px);
    }
    /* Tùy chỉnh sidebar */
    .css-1d391kg { /* sidebar */
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    /* Nút phân tích */
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 30px;
        padding: 0.5rem 2.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(74, 144, 226, 0.2);
    }
    .stButton > button:hover {
        background-color: #357ABD;
        transform: scale(1.02);
        box-shadow: 0 8px 15px -3px rgba(74, 144, 226, 0.3);
    }
    /* Dataframe */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    /* Chart */
    .stPlotlyChart, .stMatplotlib {
        border-radius: 12px;
        background: white;
        padding: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. JAVASCRIPT CHO LINH BẢO (Thú cưng ảo)
# ==============================================================================
# Nhúng một đoạn script JS nhỏ để điều khiển thú cưng
js_pet = """
<script>
    // Hàm khởi tạo và điều khiển Linh Bảo
    function initPet() {
        const container = document.querySelector('.pet-container');
        if (!container) return;

        const avatar = container.querySelector('.pet-avatar');
        const bubble = container.querySelector('.speech-bubble');
        const hearts = container.querySelector('.hearts');
        if (!avatar || !bubble) return;

        // Danh sách các câu nói ngẫu nhiên
        const messages = [
            'Chào chổi nhỏ! 🌟', 
            'Hành tinh đâu rồi nhỉ? 🔭', 
            'Em đã sẵn sàng chưa? 🚀',
            'Phân tích dữ liệu nào! 💫',
            'TESS đang quan sát đó! 🛰️',
            'Có hành tinh mới không? 🤔',
            'Em yêu thích AstroMine-X! ❤️',
            'Chúng ta là nhà thám hiểm! 🌍'
        ];

        let currentMessageIndex = 0;
        let messageTimeout = null;
        let isBubbleVisible = false;

        // Hiển thị bong bóng thoại
        function showBubble(text, duration = 2500) {
            if (messageTimeout) clearTimeout(messageTimeout);
            bubble.textContent = text;
            bubble.classList.add('show');
            isBubbleVisible = true;

            messageTimeout = setTimeout(() => {
                bubble.classList.remove('show');
                isBubbleVisible = false;
                // Tự động hiển thị lời nhắn mới sau một khoảng
                setTimeout(randomMessage, 3000);
            }, duration);
        }

        // Chọn tin nhắn ngẫu nhiên
        function randomMessage() {
            if (!isBubbleVisible) {
                const randomIdx = Math.floor(Math.random() * messages.length);
                showBubble(messages[randomIdx], 2500);
            }
        }

        // Di chuyển thú cưng (gọi từ sự kiện click)
        function movePet(direction = 'right') {
            const avatar = document.querySelector('.pet-avatar');
            if (!avatar) return;
            const currentLeft = parseInt(avatar.style.left) || 10;
            const containerWidth = document.querySelector('.pet-container')?.offsetWidth || 500;
            
            let newLeft;
            if (direction === 'right') {
                newLeft = Math.min(currentLeft + 120, containerWidth - 100);
            } else {
                newLeft = Math.max(currentLeft - 120, 10);
            }
            avatar.style.left = newLeft + 'px';

            // Hiệu ứng hạnh phúc
            if (hearts) {
                hearts.classList.remove('show');
                setTimeout(() => {
                    hearts.classList.add('show');
                    hearts.style.left = (newLeft + 30) + 'px';
                }, 100);
                setTimeout(() => {
                    hearts.classList.remove('show');
                }, 1000);
            }

            // Đổi hướng mặt (xoay icon)
            if (direction === 'right') {
                avatar.style.transform = 'scaleX(1)';
            } else {
                avatar.style.transform = 'scaleX(-1)';
            }
            // Phát lại animation float
            avatar.style.animation = 'none';
            requestAnimationFrame(() => {
                avatar.style.animation = 'float 3s ease-in-out infinite';
            });
        }

        // Xử lý click vào thú cưng
        avatar.addEventListener('click', function(e) {
            // Đổi hướng di chuyển ngẫu nhiên
            const dir = Math.random() > 0.5 ? 'right' : 'left';
            movePet(dir);
            // Nói một câu
            const randomIdx = Math.floor(Math.random() * messages.length);
            showBubble(messages[randomIdx], 2000);
        });

        // Tự động nói lần đầu sau 2 giây
        setTimeout(() => {
            showBubble('Chào bạn! Mình là Linh Bảo! 🌟', 3000);
        }, 2000);

        // Tự động di chuyển và nói chu kỳ
        setInterval(() => {
            if (Math.random() > 0.6) {
                const dir = Math.random() > 0.5 ? 'right' : 'left';
                movePet(dir);
            }
            if (Math.random() > 0.7 && !isBubbleVisible) {
                randomMessage();
            }
        }, 8000);

        // Lắng nghe sự kiện từ các nút bên ngoài (ví dụ khi upload file)
        window.movePet = movePet;
        window.showBubble = showBubble;
        window.randomMessage = randomMessage;
    }

    // Khởi tạo khi DOM sẵn sàng
    document.addEventListener('DOMContentLoaded', initPet);
    // Nếu Streamlit chỉ load lại phần nội dung, vẫn gọi lại init
    if (window.Streamlit) {
        window.Streamlit.events.addEventListener('rendered', () => {
            setTimeout(initPet, 100);
        });
    }
</script>
"""

# ==============================================================================
# 3. HIỂN THỊ GIAO DIỆN CHÍNH VÀ LINH BẢO
# ==============================================================================

# Header
st.markdown('<p class="main-header">🪐 AstroMine-X</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Phát hiện ngoại hành tinh từ dữ liệu TESS với AI • Phiên bản Linh Bảo</p>', unsafe_allow_html=True)

# --- Con thú cưng (Linh Bảo) ---
st.markdown("""
<div class="pet-container">
    <div class="pet-avatar" id="pet-avatar" style="left: 10px;">🐼</div>
    <div class="speech-bubble" id="speech-bubble">Chào bạn!</div>
    <div class="hearts" id="hearts">❤️✨</div>
    <div class="ground-line"></div>
</div>
""", unsafe_allow_html=True)

# Nhúng JS điều khiển thú cưng
st.markdown(js_pet, unsafe_allow_html=True)

# Sidebar Hướng dẫn
with st.sidebar:
    st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/tess_artist_0.jpg", use_container_width=True)
    st.title("📖 Hướng dẫn & Linh Bảo")
    st.markdown("""
    **🪐 AstroMine-X** là công cụ AI phát hiện ngoại hành tinh.

    **🐼 Linh Bảo - Trợ lý thông minh:**
    - Click vào em ấy để tương tác!
    - Em ấy sẽ nhảy, nói chuyện và khuyến khích bạn.

    **🚀 Cách sử dụng:**
    1. Tải lên file CSV (6 cột: `pl_orbper, pl_radj, pl_bmasse, pl_orbincl, st_teff, st_logg`)
    2. Hoặc nhập thông số thủ công.
    3. Nhấn **Phân tích** để xem kết quả.

    **🎯 Độ chính xác:** ~85.56% trên tập kiểm tra.
    """)

# ==============================================================================
# 4. TẢI MODEL VÀ XỬ LÝ CHÍNH
# ==============================================================================

# Load model và scaler
@st.cache_resource
def load_model():
    try:
        model = joblib.load("planet_model_lgb_fixed.pkl")
        scaler = joblib.load("scaler_lgb_fixed.pkl")
        return model, scaler
    except Exception as e:
        st.error(f"❌ Không thể tải model: {e}")
        return None, None

model, scaler = load_model()
if model is None:
    st.stop()

st.success("✅ Model và scaler đã sẵn sàng!")

# Tabs chính
tab1, tab2 = st.tabs(["📂 Tải file CSV", "✏️ Nhập thủ công"])

# ----- TAB 1: Upload CSV -----
with tab1:
    uploaded_file = st.file_uploader("Chọn file CSV (tối đa 200MB)", type=['csv'])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("🔍 Phân tích", key="analyze_csv"):
                feature_cols = ['pl_orbper', 'pl_radj', 'pl_bmasse', 'pl_orbincl', 'st_teff', 'st_logg']
                # Kiểm tra các cột có tồn tại không
                missing = [col for col in feature_cols if col not in df.columns]
                if missing:
                    st.error(f"❌ Thiếu các cột: {missing}. Vui lòng kiểm tra lại file CSV.")
                else:
                    X = df[feature_cols].copy()
                    X = X.fillna(X.mean())
                    X_scaled = scaler.transform(X)
                    proba = model.predict_proba(X_scaled)[:, 1]
                    df_result = df.copy()
                    df_result['Confidence'] = np.round(proba, 3)
                    
                    st.subheader("📊 Kết quả dự đoán")
                    st.dataframe(df_result[['Confidence']], use_container_width=True)
                    
                    # Biểu đồ phân bố
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.hist(df_result['Confidence'], bins=15, color='#4A90E2', edgecolor='white', alpha=0.8)
                    ax.set_xlabel('Độ tin cậy', fontweight='600')
                    ax.set_ylabel('Số lượng', fontweight='600')
                    ax.set_title('Phân bố độ tin cậy của các ứng viên', fontweight='600')
                    ax.grid(axis='y', alpha=0.3)
                    st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Lỗi xử lý file: {e}")

# ----- TAB 2: Nhập thủ công -----
with tab2:
    st.markdown('<div class="info-box">✏️ Nhập thông số của một ngôi sao để kiểm tra nhanh.</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        orbper = st.number_input('Chu kỳ quỹ đạo (ngày)', value=5.0, step=0.1)
        radj = st.number_input('Bán kính (Rjup)', value=1.2, step=0.01)
        bmasse = st.number_input('Khối lượng (Mjup)', value=2.5, step=0.1)
    with col2:
        orbincl = st.number_input('Độ nghiêng (độ)', value=85.0, step=0.1)
        st_teff = st.number_input('Nhiệt độ sao (K)', value=5500.0, step=50.0)
        st_logg = st.number_input('log(g) (cm/s²)', value=4.2, step=0.1)
    
    if st.button("🔍 Dự đoán ngôi sao này", key="predict_manual"):
        input_data = np.array([[orbper, radj, bmasse, orbincl, st_teff, st_logg]])
        input_scaled = scaler.transform(input_data)
        proba = model.predict_proba(input_scaled)[0][1]
        if proba > 0.5:
            st.success(f"✅ **CÓ HÀNH TINH!** Độ tin cậy: {proba*100:.2f}%")
            # Gửi tín hiệu đến Linh Bảo để ăn mừng
            js_celebrate = """
            <script>
                setTimeout(() => {
                    const bubble = document.querySelector('.speech-bubble');
                    if (bubble) {
                        bubble.textContent = '🎉 Chúc mừng! Hành tinh mới!';
                        bubble.classList.add('show');
                        setTimeout(() => bubble.classList.remove('show'), 3000);
                    }
                }, 200);
            </script>
            """
            st.markdown(js_celebrate, unsafe_allow_html=True)
        else:
            st.warning(f"❌ **KHÔNG CÓ HÀNH TINH.** Độ tin cậy: {proba*100:.2f}%")

# ==============================================================================
# 5. FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<center>
    🚀 AstroMine-X v2.0 | Phát triển với ❤️ và Linh Bảo 🐼<br>
    <span style="color:#888; font-size:0.8rem;">© 2026 Đội ngũ nghiên cứu trẻ</span>
</center>
""", unsafe_allow_html=True)
