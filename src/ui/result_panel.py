import os
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QScrollArea, QWidget)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from src.ui.styles import PANEL_STYLE

class ResultPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(PANEL_STYLE)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(30, 30, 30, 30)

        # 1. Tiêu đề khu vực
        self.lbl_header = QLabel("KẾT QUẢ TƯ VẤN")
        self.lbl_header.setStyleSheet("font-size: 22px; font-weight: 1000; color: #27ae60; border: none;")
        self.lbl_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_header)

        # 2. Ảnh sản phẩm
        self.lbl_image = QLabel()
        self.lbl_image.setFixedSize(300, 300)
        self.lbl_image.setStyleSheet("background-color: #f9f9f9; border-radius: 8px; border: 1px dashed #ccc;")
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_image, 0, Qt.AlignmentFlag.AlignCenter)

        # 3. Tên sản phẩm
        self.lbl_name = QLabel("Vui lòng chọn tiêu chí bên trái...")
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; border: none;")
        layout.addWidget(self.lbl_name)

        # Xuất xứ
        self.lbl_origin = QLabel("")
        self.lbl_origin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_origin.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")
        layout.addWidget(self.lbl_origin)

        # 4. Giá tiền
        self.lbl_price = QLabel("")
        self.lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_price.setStyleSheet("font-size: 18px; color: #e74c3c; font-weight: bold; border: none;")
        layout.addWidget(self.lbl_price)

        # 5. Mô tả (Có thanh cuộn nếu dài)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame) # Bỏ viền scroll area
        scroll.setStyleSheet("border: none; background-color: transparent;")
        
        self.lbl_desc = QLabel("")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setStyleSheet("font-size: 15px; color: #555; line-height: 1.5; border: none;")
        self.lbl_desc.setAlignment(Qt.AlignmentFlag.AlignJustify)
        
        scroll.setWidget(self.lbl_desc)
        layout.addWidget(scroll)

    def update_product(self, data):
        """Hàm này được gọi từ Main Window khi tìm thấy sản phẩm"""
        self.lbl_name.setText(data['name'])
        self.lbl_origin.setText(f"Xuất xứ: {data['origin']}")
        self.lbl_price.setText(f"Giá tham khảo: {data['price']}")
        self.lbl_desc.setText(data['description'])

        # Load ảnh
        img_path = data['image_path']
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            self.lbl_image.setPixmap(pixmap.scaled(
                self.lbl_image.size(), 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.lbl_image.setText("📷 Không có ảnh")

    def show_not_found(self):
        """Hàm hiển thị khi không tìm thấy"""
        self.lbl_name.setText("❌ KHÔNG TÌM THẤY SẢN PHẨM")
        self.lbl_price.setText("")
        self.lbl_desc.setText("Rất tiếc, không có sản phẩm nào khớp hoàn toàn với bộ tiêu chí bạn chọn.\n\nHệ chuyên gia yêu cầu tính chính xác cao. Hãy thử thay đổi một vài tiêu chí (ví dụ: đổi Thương hiệu hoặc Khoảng giá).")
        self.lbl_image.clear()
        self.lbl_image.setText("Not Found")