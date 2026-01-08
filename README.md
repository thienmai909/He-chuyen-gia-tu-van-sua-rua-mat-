# Hệ Chuyên Gia Tư Vấn Sữa Rửa Mặt 🧴

Hệ thống chuyên gia tư vấn sản phẩm sữa rửa mặt dựa trên các tiêu chí về loại da, công dụng, đặc tính, giá cả, thương hiệu và xuất xứ.

## 🚀 Cách chạy dự án

### 1. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

```bash
python main.py
```

## 🛠️ Công cụ quản lý sản phẩm

Để quản lý (thêm/sửa/xóa) sản phẩm trong database:

```bash
python create_db.py
```

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- PySide6 (Qt for Python)

## 📁 Cấu trúc dự án

```
├── main.py              # File chạy ứng dụng chính
├── create_db.py         # Công cụ quản lý database
├── src/                 # Mã nguồn
│   ├── logic/           # Logic suy luận
│   │   ├── constants.py
│   │   ├── knowledge_base.py
│   │   └── inference_engine.py
│   ├── ui/             # Giao diện người dùng
│   └── utils/          # Tiện ích
├── data/               # Database SQLite
├── assets/             # Tài nguyên (font, ảnh, icon)
└── requirements.txt    # Thư viện cần cài đặt
```

## 💡 Tính năng

- ✅ 638 luật suy luận cho 28 sản phẩm
- ✅ Giao diện thân thiện với PySide6
- ✅ Quản lý sản phẩm qua GUI
- ✅ Tích hợp link mua hàng