import os
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QScrollArea, QPushButton)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl
from src.ui.styles import PANEL_STYLE
from src.utils.resource_manager import get_asset_path, get_resource_path

class ResultPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.current_link = ""
        self.setObjectName("ResultPanelFrame")
        
        # Load background image using resource manager
        bg_path = get_asset_path("images", "bg-result.png")
        
        # Chuyển đổi backslash thành forward slash cho QSS
        # QSS yêu cầu forward slash hoặc double backslash
        bg_path_qss = bg_path.replace("\\", "/")
        
        # Style with background image và transparent labels
        self.setStyleSheet(PANEL_STYLE + f"""
            #ResultPanelFrame {{
                border-image: url({bg_path_qss}) 0 0 0 0 stretch stretch;
            }}
            
            QLabel {{
                background-color: transparent;
            }}
        """)
        self.setup_ui()

    def setup_ui(self):
        layout_result = QVBoxLayout(self)
        layout_result.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_result.setContentsMargins(30, 30, 30, 20)

        # 1. Tiêu đề khu vực
        self.lbl_header = QLabel("KẾT QUẢ TƯ VẤN")
        self.lbl_header.setStyleSheet("font-size: 22px; font-weight: 1000; color: #27ae60; border: none;")
        self.lbl_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_result.addWidget(self.lbl_header)

        # 2. Ảnh sản phẩm
        self.lbl_image = QLabel()
        self.lbl_image.setFixedSize(300, 300)
        self.lbl_image.setStyleSheet("background-color: #f9f9f9; border-radius: 8px; border: 1px dashed #ccc;")
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_result.addWidget(self.lbl_image, 0, Qt.AlignmentFlag.AlignCenter)

        # 3. Tên sản phẩm
        self.lbl_name = QLabel("Vui lòng chọn tiêu chí bên trái...")
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px; border: none;")
        layout_result.addWidget(self.lbl_name)

        # Xuất xứ
        self.lbl_origin = QLabel("")
        self.lbl_origin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_origin.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")
        layout_result.addWidget(self.lbl_origin)

        # 4. Giá tiền
        self.lbl_price = QLabel("")
        self.lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_price.setStyleSheet("font-size: 18px; color: #e74c3c; font-weight: bold; border: none;")
        layout_result.addWidget(self.lbl_price)

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
        layout_result.addWidget(scroll, 1)

        self.btn_delta = QPushButton("MUA NGAY 🛒")
        self.btn_delta.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white;
                padding: 10px 10px 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.btn_delta.clicked.connect(self.click_product_link)
        self.btn_delta.hide()
        layout_result.addWidget(self.btn_delta, alignment=Qt.AlignmentFlag.AlignRight)

    def update_product(self, data):
        """Hàm này được gọi từ Main Window khi tìm thấy sản phẩm"""
        self.lbl_name.setText(data['name'])
        self.lbl_origin.setText(f"Xuất xứ: {data['origin']}")
        self.lbl_price.setText(f"Giá tham khảo: {data['price']}")
        self.lbl_desc.setText(data['description'])

        self.current_link = data.get('product_link', '')

        # Load ảnh - chuẩn hóa đường dẫn từ database
        img_path = data['image_path']
        
        # Nếu đường dẫn là tương đối, chuyển thành tuyệt đối
        if not os.path.isabs(img_path):
            img_path = get_resource_path(img_path)
        
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            self.lbl_image.setPixmap(pixmap.scaled(
                self.lbl_image.size(), 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.lbl_image.setText("📷 Không có ảnh")
        
        self.btn_delta.show()

    def show_not_found(self):
        """Hàm hiển thị khi không tìm thấy"""
        self.lbl_name.setText("❌ KHÔNG TÌM THẤY SẢN PHẨM")
        self.lbl_price.setText("")
        self.lbl_desc.setText("Rất tiếc, không có sản phẩm nào khớp hoàn toàn với bộ tiêu chí bạn chọn.\n\nHệ chuyên gia yêu cầu tính chính xác cao. Hãy thử thay đổi một vài tiêu chí (ví dụ: đổi Thương hiệu hoặc Khoảng giá).")
        self.lbl_image.clear()
        self.lbl_image.setText("Not Found")
        self.lbl_origin.setText("")

    def click_product_link(self):
        if self.current_link:
            print(f"Opening: {self.current_link}")
            # Dùng QDesktopServices để mở link trên trình duyệt mặc định của máy
            QDesktopServices.openUrl(QUrl(self.current_link))