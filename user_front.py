import io
import requests
from PIL import Image
import streamlit as st

# 1. Cấu hình trang (BẮT BUỘC đặt ở đầu file)
st.set_page_config(
    page_title="User Portal - Thí Sinh", page_icon="👤", layout="centered"
)

API_URL = "http://127.0.0.1:9999/api/submissions"


# 2. Hàm nén ảnh giảm dung lượng tệp
def compress_image(file):
    img = Image.open(file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.thumbnail((1200, 1200))  # Thu nhỏ chiều dài/rộng tối đa về 1200px
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=70)  # Nén chất lượng ảnh 70%
    buffer.seek(0)
    return buffer


# 3. Giao diện người dùng
st.title("👤 Cổng Người Dự Thi")
st.header("📸 Nộp Tác Phẩm Nhiếp Ảnh Phim")

with st.form("submission_form"):
    name = st.text_input("Họ và tên thí sinh (*)")
    title = st.text_input("Tiêu đề tác phẩm (*)")

    uploaded_file = st.file_uploader(
        "Tải tệp ảnh lên (*)", type=["jpg", "jpeg", "png", "webp"]
    )

    col1, col2 = st.columns(2)
    film_stock = col1.text_input("Loại phim (*)")
    camera = col2.text_input("Máy ảnh (*)")

    film_format = st.selectbox("Định dạng phim", ["35mm", "120mm", "4x5"])

    submitted = st.form_submit_button("🚀 Gửi bài dự thi")

    if submitted:
        if (
            not name
            or not title
            or not uploaded_file
            or not film_stock
            or not camera
        ):
            st.warning(
                "⚠️ Vui lòng điền đầy đủ các trường và chọn tệp ảnh (*)."
            )
        else:
            payload = {
                "name": name.strip(),
                "title": title.strip(),
                "film_stock": film_stock.strip(),
                "camera": camera.strip(),
                "film_format": film_format,
                "iso": "200",
                "lens": "N/A",
                "developing_lab": "N/A",
                "scanning_specs": "N/A",
            }

            with st.spinner("🚀 Đang nén ảnh và tải bài dự thi lên..."):
                try:
                    # Thực hiện nén ảnh trước khi đẩy qua API
                    compressed_bytes = compress_image(uploaded_file)
                    files = {
                        "file": (
                            uploaded_file.name,
                            compressed_bytes,
                            "image/jpeg",
                        )
                    }

                    res = requests.post(API_URL, data=payload, files=files)
                    if res.status_code in [200, 201]:
                        st.success("✨ Nộp bài thành công!")
                        st.balloons()
                    else:
                        st.error(f"❌ Lỗi Backend: {res.text}")
                except Exception as e:
                    st.error(f"❌ Không thể kết nối tới Backend: {e}")
