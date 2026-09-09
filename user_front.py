import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:9999/api/submissions"
st.set_page_config(page_title="User Portal - Thí Sinh", page_icon="👤", layout="centered")

st.title("👤 Cổng Người Dự Thi")
st.header("📸 Nộp Tác Phẩm Nhiếp Ảnh Phim")

with st.form("submission_form"):
    name = st.text_input("Họ và tên thí sinh (*)")
    title = st.text_input("Tiêu đề tác phẩm (*)")
    
    # Sử dụng file_uploader để chọn tệp từ máy tính
    uploaded_file = st.file_uploader("Tải tệp ảnh lên (*)", type=["jpg", "jpeg", "png", "webp"])
    
    col1, col2 = st.columns(2)
    film_stock = col1.text_input("Loại phim (*)")
    camera = col2.text_input("Máy ảnh (*)")
    
    film_format = st.selectbox("Định dạng phim", ["35mm", "120mm", "4x5"])
    
    submitted = st.form_submit_button("🚀 Gửi bài dự thi")

    if submitted:
        if not title or not uploaded_file or not film_stock or not camera:
            st.warning("⚠️ Vui lòng điền đầy đủ các trường và chọn tệp ảnh (*).")
        else:
            # Gửi dữ liệu dưới dạng form-data kèm tệp binary
            payload = {
                "title": title.strip(),
                "film_stock": film_stock.strip(), 
                "camera": camera.strip(), 
                "film_format": film_format,
                "iso": "200",
                "lens": "N/A",
                "developing_lab": "N/A",
                "scanning_specs": "N/A"
            }
            
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            
            with st.spinner("🤖 AI System đang quét tính hợp lệ..."):
                time.sleep(1)
                try:
                    res = requests.post(API_URL, data=payload, files=files)
                    if res.status_code in [200, 201]:
                        st.success("✨ Nộp bài thành công!")
                        st.balloons()
                    else:
                        st.error(f"❌ Lỗi Backend: {res.text}")
                except Exception as e:
                    st.error(f"❌ Không thể kết nối tới Backend: {e}")