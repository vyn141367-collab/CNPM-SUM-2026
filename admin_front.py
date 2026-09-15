import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:9999/api/submissions"
st.set_page_config(page_title="Admin Portal - Quản Trị", page_icon="🛠️", layout="wide")

st.title("🛠️ Cổng Quản Trị Hệ Thống")

def fetch_data():
    res = requests.get(API_URL)
    if res.status_code == 200:
        return res.json().get("data", [])
    return []

try:
    data = fetch_data()
    if data:
        tab1, tab2, tab3 = st.tabs(["🖼️ Triển lãm", "📊 Dữ liệu", "⚙️ Quản lý & Chỉnh sửa"])
        
        with tab1:
            st.subheader("Triển lãm trực quan các tác phẩm đã nộp")
            cols = st.columns(3)
            for idx, sub in enumerate(data):
                col = cols[idx % 3]
                with col:
                    st.markdown(f"**{sub.get('title')}**")
                    st.markdown(f"👤 *Tác giả: {sub.get('name', 'N/A')}*")
                    
                    # HIỂN THỊ ĐIỂM SỐ TẠI TAB TRIỂN LÃM
                    score_val = sub.get('score')
                    if score_val is not None:
                        st.markdown(f"⭐ **Điểm số:** `{score_val}/10`")
                    else:
                        st.markdown("⭐ **Điểm số:** *Chưa chấm*")
                    
                    img_url = sub.get('image_url')
                    if img_url:
                        try:
                            st.image(img_url, use_container_width=True)
                        except Exception:
                            st.warning("⚠️ Link ảnh không hợp lệ hoặc bị hỏng.")
                            
                    st.caption(f"📷 {sub.get('camera')} | 🎞️ {sub.get('film_stock')}")
                    if sub.get('comment'):
                        st.info(f"💬 **Giám khảo:** {sub.get('comment')}")
                    st.divider()

        with tab2:
            st.subheader("Bảng dữ liệu chi tiết")
            df = pd.DataFrame(data)
            
            # Sắp xếp lại thứ tự cột cho dễ nhìn
            cols_order = ['id', 'name', 'title', 'score', 'comment', 'camera', 'film_stock', 'film_format', 'image_url']
            df = df.reindex(columns=[c for c in cols_order if c in df.columns])
            
            st.dataframe(df, use_container_width=True, column_config={
                "score": st.column_config.NumberColumn("Điểm", format="%d ⭐"),
                "comment": "Nhận xét Giám khảo",
                "image_url": st.column_config.LinkColumn("Link File Gốc")
            })
            
        with tab3:
            st.subheader("Kiểm soát & Chỉnh sửa thông tin bài thi")
            for sub in data:
                sub_id = sub.get('id')
                
                with st.expander(f"Sửa bài: {sub.get('title')} (Bởi: {sub.get('name', 'N/A')} - ID: {sub_id})"):
                    with st.form(f"edit_form_{sub_id}"):
                        new_title = st.text_input("Tiêu đề", value=sub.get('title'))
                        new_name = st.text_input("Tên Thí Sinh", value=sub.get('name', 'N/A'))
                        
                        col1, col2 = st.columns(2)
                        new_camera = col1.text_input("Máy ảnh", value=sub.get('camera'))
                        new_film = col2.text_input("Loại phim", value=sub.get('film_stock'))
                        
                        # SỬA ĐIỂM VÀ NHẬN XÉT TRỰC TIẾP TỪ ADMIN (NẾU CẦN)
                        col3, col4 = st.columns([1, 2])
                        current_score = sub.get('score') if sub.get('score') is not None else 0
                        new_score = col3.number_input("Điểm số", min_value=0, max_value=10, value=int(current_score))
                        new_comment = col4.text_input("Nhận xét", value=sub.get('comment', ''))

                        format_opts = ["35mm", "120mm", "4x5"]
                        current_format = sub.get('film_format')
                        idx_fmt = format_opts.index(current_format) if current_format in format_opts else 0
                        new_format = st.selectbox("Định dạng", format_opts, index=idx_fmt)
                        
                        submit_update = st.form_submit_button("💾 Lưu thay đổi")
                        
                        if submit_update:
                            payload = {
                                "title": new_title,
                                "name": new_name,
                                "camera": new_camera,
                                "film_stock": new_film,
                                "film_format": new_format,
                                "score": new_score,
                                "comment": new_comment
                            }
                            res = requests.put(f"{API_URL}/{sub_id}", json=payload)
                            if res.status_code == 200:
                                st.success("Cập nhật thành công!")
                                st.rerun()
                            else:
                                st.error("Lỗi cập nhật!")
                    
                    if st.button("🗑️ Xóa bài thi này", key=f"del_{sub_id}", type="primary"):
                        res = requests.delete(f"{API_URL}/{sub_id}")
                        if res.status_code == 200:
                            st.success("Đã xóa bài thi!")
                            st.rerun()
                        else:
                            st.error("Lỗi khi xóa!")
    else:
        st.info("Chưa có dữ liệu bài thi nào trong hệ thống.")
except Exception as e:
    st.error(f"Không thể kết nối Backend Flask: {e}")
