# Hệ thống Chat với Chữ ký số

Ứng dụng web cho phép người dùng chat và chia sẻ file với tính năng chữ ký số để đảm bảo tính toàn vẹn và xác thực nguồn gốc của file.

## Tính năng chính

- Đăng ký và đăng nhập người dùng
- Tạo và tham gia phòng chat
- Chia sẻ file trong phòng chat
- Ký số file bằng RSA
- Xác minh chữ ký số của file
- Giao diện thân thiện với người dùng

## Cài đặt

1. Clone repository:
```bash
git clone [URL_REPOSITORY]
cd [TEN_THU_MUC]
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Chạy ứng dụng:
```bash
python run.py
```

4. Truy cập ứng dụng tại: http://localhost:8080

## Cấu trúc dự án

```
RSA/
├── app/                    # Thư mục chính chứa mã nguồn
│   ├── __init__.py        # File khởi tạo ứng dụng
│   ├── models/            # Chứa các model
│   │   └── user.py        # Model User
│   ├── routes/            # Chứa các route
│   │   ├── auth.py        # Route xác thực
│   │   └── main.py        # Route chính
│   ├── utils/             # Chứa các tiện ích
│   │   ├── crypto.py      # Hàm mã hóa
│   │   └── room.py        # Quản lý phòng
│   ├── static/            # Chứa file tĩnh (CSS, JS)
│   └── templates/         # Chứa file template
├── uploads/               # Thư mục lưu file upload
├── run.py                # File chạy ứng dụng
└── requirements.txt      # File chứa các thư viện cần thiết
```

## Công nghệ sử dụng

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-SocketIO
- Cryptography
- Bootstrap 5

## Tác giả

[Tên của bạn]
[MSSV]
[Lớp]

## Giấy phép

MIT License 