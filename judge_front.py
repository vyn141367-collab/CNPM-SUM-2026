import streamlit as st
import requests

API_URL = "http://127.0.0.1:9999/api/submissions"
st.set_page_config(page_title="Judge Portal - Giám Khảo", page_icon="⚖️", layout="wide")

st.title("⚖️ Cổng Ban Giám Khảo")
st.subheader("Danh sách bài thi chờ chấm điểm")

try:
    res = requests.get(API_URL)
    if res.status_code == 200:
        submissions = res.json().get("data", [])
        if not submissions:
            st.info("Chưa có bài thi nào được nộp.")
        else:
            for sub in submissions:
                sub_id = sub.get("id")
                title = sub.get("title", "Không tiêu đề")
                image_url = sub.get("image_url")
                
                with st.container():
                    st.subheader(f"📸 {title} (ID: #{sub_id})")
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        if image_url:
                            try:
                                # Hiển thị tệp ảnh tải lên từ Server Flask
                                st.image(image_url, use_container_width=True)
                            except Exception as e:
                                st.error(f"❌ Không thể tải ảnh từ URL: {image_url}")
                        else:
                            st.warning("⚠️ Bài thi không có tệp ảnh.")
                            
                    with col2:
                        st.markdown("### 🎞️ Thông số kỹ thuật")
                        st.write(f" **Tên Thí Sinh:** {sub.get('name', 'N/A')}")
                        st.write(f"📷 **Máy ảnh:** {sub.get('camera', 'N/A')}")
                        st.write(f"🎞️ **Loại phim:** {sub.get('film_stock', 'N/A')}")
                        st.write(f"📐 **Định dạng:** {sub.get('film_format', 'N/A')}")
                        st.write(f"🔍 **Ống kính (Lens):** {sub.get('lens', 'N/A')}")
                        st.write(f"⚡ **ISO:** {sub.get('iso', 'N/A')}")
                        
                        st.divider()
                        
                        st.markdown("### 📝 Đánh giá & Chấm điểm")
                        score = st.slider("Chấm điểm (1-10)", 1, 10, 5, key=f"score_{sub_id}")
                        comment = st.text_area("Nhận xét bài thi", key=f"comment_{sub_id}", placeholder="Nhập cảm nhận/đánh giá...")
                        
                        if st.button("💾 Lưu kết quả chấm", key=f"btn_{sub_id}"):
                            st.success(f"✅ Đã lưu điểm {score}/10 cho bài thi #{sub_id}!")
                            
                    st.divider()
    else:
        st.error(f"Lỗi Server: status code {res.status_code}")
except Exception as e:
    st.error(f"Không thể kết nối tới Backend Flask (Cổng 9999): {e}")