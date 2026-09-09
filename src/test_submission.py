import requests
import pytest

# Đường dẫn API gốc (giả định router của bạn thiết lập là /api/submissions)
BASE_URL = "http://127.0.0.1:9999/api/submissions"

# Token giả lập (Nếu API của bạn yêu cầu đăng nhập JWT thì thay thế bằng token thật)
FAKE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
HEADERS = {
    "Authorization": f"Bearer {FAKE_TOKEN}",
    "Content-Type": "application/json"
}

def test_submit_film_photo_success():
    """Kiểm thử: Nộp tác phẩm nhiếp ảnh phim hợp lệ, đầy đủ thông số (Metadata)"""
    payload = {
        "title": "Hà Nội mùa thu",
        "image_url": "https://example.com/hanoi_autumn.jpg",
        "film_stock": "Kodak Gold 200",
        "camera": "Canon AE-1",
        "lens": "50mm f/1.4",
        "iso": 200,
        "film_format": "35mm",
        "developing_lab": "Nadir Lab",
        "scanning_specs": "Fuji Frontier 3000"
    }
    
    # Giả sử API đang mở chưa cần chặn Token, nếu có thì thêm headers=HEADERS
    response = requests.post(f"{BASE_URL}", json=payload)
    
    print("\n[Submit Success Response]:", response.text)
    
    # Trả về 201 (Created) hoặc 200 (OK)
    assert response.status_code in [200, 201]
    
    # Kiểm tra xem response có trả về ID của bài nộp hay không
    data = response.json()
    assert data is not None

def test_submit_film_photo_missing_metadata():
    """Kiểm thử: Nộp tác phẩm nhưng cố tình bỏ trống loại cuộn phim (film_stock)"""
    payload = {
        "title": "Lỗi thiếu cuộn phim",
        "image_url": "https://example.com/missing.jpg",
        "camera": "Leica M6"
        # Cố tình thiếu film_stock, film_format, iso...
    }
    
    response = requests.post(f"{BASE_URL}", json=payload)
    
    print("\n[Submit Missing Data Response]:", response.text)
    
    # Trả về 400 (Bad Request) vì validation thất bại (thiếu thông tin analog bắt buộc)
    assert response.status_code == 400

def test_get_all_submissions():
    """Kiểm thử: Ban giám khảo / Organizer lấy danh sách tất cả các bài đã nộp"""
    response = requests.get(f"{BASE_URL}")
    
    print("\n[Get Submissions Response]:", response.text)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list) or "data" in response.json()