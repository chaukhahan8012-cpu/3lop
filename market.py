import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Cấu hình trang chuyên nghiệp
st.set_page_config(page_title="AgriLoop QC System", layout="wide", page_icon="🌱")

# Tùy chỉnh CSS để nhìn hiện đại hơn
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2E7D32; color: white; }
    .status-box { padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 AgriLoop: Hệ thống Kiểm định & Truy xuất Nguồn gốc")
st.markdown("---")

# Khởi tạo Database giả lập trong Session State
if 'data_log' not in st.session_state:
    st.session_state.data_log = pd.DataFrame(columns=['Thời gian', 'Loại phụ phẩm', 'Độ ẩm (%)', 'Tạp chất (%)', 'Trạng thái'])

# Giao diện chính chia làm 3 cột quy trình
col1, col2, col3 = st.columns(3, gap="large")

# --- BƯỚC 1: PHÂN LOẠI AI ---
with col1:
    st.subheader("1️⃣ Phân loại Nguồn (AI)")
    with st.container():
        source_type = st.selectbox("Chọn loại phụ phẩm:", ["Rơm rạ", "Vỏ trấu", "Bã mía", "Vỏ cà phê"])
        if st.button("🚀 Kích hoạt AI Vision"):
            with st.status("Đang phân tích hình ảnh...", expanded=True) as status:
                time.sleep(1.5)
                st.write("Đang nhận diện thành phần...")
                time.sleep(1)
                status.update(label="Phân tích hoàn tất!", state="complete", expanded=False)
            st.session_state['step1_done'] = True
            st.success(f"Nhận diện: {source_type} - Độ thuần 98%")

# --- BƯỚC 2: KIỂM ĐỊNH LÝ HÓA ---
with col2:
    st.subheader("2️⃣ Chỉ số Lý - Hóa")
    moisture = st.slider("Chỉ số độ ẩm (%)", 0, 100, 15)
    impurities = st.slider("Tỉ lệ tạp chất (%)", 0, 10, 2)
    
    # Logic kiểm định của AgriLoop
    is_qualified = moisture <= 20 and impurities <= 5
    
    if is_qualified:
        st.info("✅ Chỉ số đạt ngưỡng tối ưu cho chế biến.")
    else:
        st.error("⚠️ Chỉ số vượt ngưỡng! Cần xử lý nhiệt lại.")

# --- BƯỚC 3: SỐ HÓA & TRUY XUẤT ---
with col3:
    st.subheader("3️⃣ Digital Passport")
    if st.button("📝 Chốt đơn & Cấp mã QR"):
        new_data = {
            'Thời gian': datetime.now().strftime("%H:%M:%S"),
            'Loại phụ phẩm': source_type,
            'Độ ẩm (%)': moisture,
            'Tạp chất (%)': impurities,
            'Trạng thái': "ĐẠT CHUẨN" if is_qualified else "REJECT"
        }
        # Cập nhật vào bảng dữ liệu
        st.session_state.data_log = pd.concat([pd.DataFrame([new_data]), st.session_state.data_log], ignore_index=True)
        
        # Hiển thị QR Code giả lập
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={new_data}", caption="Quét để truy xuất ESG")
        st.balloons()

st.markdown("---")

# --- PHẦN QUẢN TRỊ DỮ LIỆU CHO DÂN MIS ---
st.subheader("📊 Bảng điều khiển Quản trị (Dành cho Doanh nghiệp thu mua)")
m1, m2, m3 = st.columns(3)
m1.metric("Tổng lô hàng đã quét", len(st.session_state.data_log))
m2.metric("Tỉ lệ đạt chuẩn", f"{len(st.session_state.data_log[st.session_state.data_log['Trạng thái'] == 'ĐẠT CHUẨN'])} đơn")
m3.metric("Lượng phát thải giảm (Dự tính)", f"{len(st.session_state.data_log)*5} kg CO2")

st.write("### Nhật ký hệ thống thời gian thực")
st.dataframe(st.session_state.data_log, use_container_width=True)
