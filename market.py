import streamlit as st
import pandas as pd

def show_trust_scoring():
    st.title("Hệ Thống Đánh Giá Tín Nhiệm Đối Tác")
    st.write("Cơ chế tự động xếp hạng dựa trên dữ liệu giao dịch thực tế.")

    # 1. Tổng quan các chỉ số tín nhiệm
    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng số đối tác", "150", "Hoạt động")
    c2.metric("Tỷ lệ uy tín trung bình", "92%", "+1.5%")
    c3.metric("Giao dịch an toàn", "1,200", "Thành công")

    # 2. Bảng xếp hạng tín nhiệm
    st.subheader("Bảng Xếp Hạng Uy Tín (Trust Score)")
    
    # Giả lập dữ liệu đánh giá
    trust_data = pd.DataFrame({
        'Đối tác': ['Nông dân Hân', 'Nông dân An', 'Nhà máy Alpha', 'Tài xế Bình', 'Hợp tác xã Chi'],
        'Vai trò': ['Người bán', 'Người bán', 'Người mua', 'Vận chuyển', 'Người bán'],
        'Điểm Uy Tín': [98, 85, 95, 92, 78],
        'Tiêu chí đánh giá': [
            'Chất lượng phế phẩm đồng đều', 
            'Giao hàng đúng hẹn', 
            'Thanh toán sòng phẳng', 
            'Lộ trình tối ưu', 
            'Hay bị trễ chuyến'
        ],
        'Trạng thái': ['⭐ Ưu tiên', '✅ Đạt', '⭐ Ưu tiên', '✅ Đạt', '⚠️ Cần cải thiện']
    })

    # Hiển thị bảng dữ liệu sạch sẽ
    st.dataframe(trust_data.set_index('Đối tác'), use_container_width=True)

    # 3. Chi tiết cách tính điểm (Dành cho Pitching)
    with st.expander("Xem cách AgriLoop tính điểm uy tín"):
        st.write("""
        Hệ thống tự động cộng/trừ điểm dựa trên:
        - **Chất lượng:** Độ ẩm, tạp chất phế phẩm (từ dữ liệu nhà máy quét).
        - **Đúng hạn:** Thời gian xe đến so với kế hoạch (từ dữ liệu GPS).
        - **Thanh toán:** Tốc độ thanh toán tiền cho nông dân (từ dữ liệu ngân hàng).
        """)

# Nhớ gọi hàm này trong menu điều hướng của bà nhé!
