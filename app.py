import streamlit as st
import pandas as pd
from automation import run_task
import time

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Khaservice Automation", layout="wide")
st.title("🤖 Khaservice Automation Tool")
st.markdown("""
### Hướng dẫn:
1. Copy dữ liệu từ Excel (2 cột: **Dự án** và **Tháng**).
2. Dán trực tiếp vào bảng bên dưới (hoặc chỉnh sửa ngay tại đây).
3. Nhấn **[BẮT ĐẦU CHẠY]**. 
Hệ thống sẽ mở Tab mới xử lý từng dòng rồi đóng lại để tiết kiệm RAM.
""")

# --- PHẦN NHẬP DỮ LIỆU ---
# Tạo bảng trống mẫu
df_init = pd.DataFrame([
    {"Dự án": "Kha Vạn Cân", "Tháng": "02/2024"},
    {"Dự án": "Vạn Phúc", "Tháng": "02/2024"}
])

st.subheader("📋 Danh sách dữ liệu (Tab 1)")
data_input = st.data_editor(df_init, num_rows="dynamic", use_container_width=True)

# --- NÚT ĐIỀU KHIỂN ---
if st.button("🚀 BẮT ĐẦU CHẠY", type="primary"):
    if data_input.empty:
        st.error("Vui lòng nhập dữ liệu!")
    else:
        total_rows = len(data_input)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Log hiển thị trên giao diện
        log_container = st.container()
        
        with log_container:
            for index, row in data_input.iterrows():
                row_idx = index + 1
                status_text.text(f"Đang xử lý dòng {row_idx}/{total_rows}: {row['Dự án']}")
                
                # Gọi hàm automation cho từng dòng
                try:
                    run_task(row.to_dict(), row_idx)
                    st.success(f"✅ Đã xong: {row['Dự án']} ({row['Tháng']})")
                except Exception as e:
                    st.error(f"❌ Lỗi dòng {row_idx}: {e}")
                
                # Cập nhật thanh tiến trình
                progress_bar.progress(row_idx / total_rows)
                time.sleep(1) # Nghỉ ngắn trước khi mở tab mới

        st.balloons()
        st.success("TẤT CẢ ĐÃ HOÀN THÀNH!")
