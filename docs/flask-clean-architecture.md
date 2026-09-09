# Architecture

```bash
    ├── frontend                 
│   ├── user_front.py           # Cổng Thí sinh
│   ├── jugde_front.py          # Cổng Giám khảo
│   ├── admin_front.py          # Cổng Quản trị viên
│   ├── assets                  # Chứa file tĩnh (CSS, Logo, font chữ...)
│   └── requirements.txt        # Các thư viện riêng cho Frontend (streamlit, pandas, requests...)
├── migrations                  # Các file lịch sử migrate DB (Alembic)
├── scripts
│   └── run_postgres.sh         # Script khởi chạy DB
├── src                         # ⚙️ MÃ NGUỒN BACKEND (Flask)
│   ├── api                     # Giao tiếp HTTP (RESTful API)
│   │   ├── controllers         # Nhận Request từ Frontend -> Gọi Service -> Trả về Response
│   │   ├── schemas             # Marshmallow (Validate dữ liệu đầu vào/ra)
│   │   ├── middleware.py       # Xử lý trung gian (VD: Check Token, Ghi Log)
│   │   ├── responses.py        # Định dạng chuẩn hóa câu trả lời (JSON)
│   │   └── requests.py         # Lọc và parse request body
│   ├── infrastructure          # Tương tác với hệ thống bên ngoài (Database, 3rd party API)
│   │   ├── services            # Dịch vụ bên ngoài (Gửi Email, S3 Upload...)
│   │   ├── databases           # Khởi tạo kết nối DB (PostgreSQL, MySQL...)
│   │   ├── repositories        # Nơi chứa các câu lệnh truy vấn CSDL (CRUD)
│   │   └── models              # 👈 ORM NẰM Ở ĐÂY: Ánh xạ Class Python -> Table CSDL
│   ├── domain                  # Logic nghiệp vụ cốt lõi (Không phụ thuộc Framework)
│   │   ├── constants.py
│   │   ├── exceptions.py       # Các lỗi nghiệp vụ tự định nghĩa
│   │   └── models              # Thực thể nghiệp vụ (Business Entities)
│   ├── services                # Điều phối logic: Nhận từ API -> Gọi Domain/Repo xử lý
│   ├── app.py                  # File chạy chính của Backend (Chứa app.run)
│   ├── config.py               # Cấu hình môi trường (DB_URL, SECRET_KEY)
│   ├── cors.py                 # Xử lý chính sách CORS cho phép Frontend gọi API
│   ├── create_app.py           # Factory Pattern khởi tạo Flask App
│   ├── dependency_container.py # Injection (Tiêm phụ thuộc)
│   ├── error_handler.py        # Bắt lỗi Global
│   └── logging.py              # Cấu hình ghi log
├── .env                        # Biến môi trường
├── requirements.txt            # Thư viện cho Backend
└── README.md
```


