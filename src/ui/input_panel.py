from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                               QPushButton, QFrame)
from PySide6.QtCore import Signal, Qt
from src.ui.styles import BUTTON_STYLE, PANEL_STYLE

# Import dữ liệu hằng số để nạp vào combobox
from src.logic.constants import SKIN_TYPES, BENEFITS, FEATURES, PRICES, BRANDS, ORIGINS

class InputPanel(QFrame):
    # Tạo tín hiệu: Khi bấm nút tìm kiếm -> Báo cho Main Window biết
    search_signal = Signal(list) 

    def __init__(self):
        super().__init__()
        self.setStyleSheet(PANEL_STYLE) # Áp dụng style khung trắng bo góc
        self.setFixedWidth(380)         # Cố định chiều rộng cột trái
        
        self.inputs = {} # Lưu trữ các widget
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tiêu đề
        lbl_title = QLabel("🔍 BỘ LỌC TÌM KIẾM")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #2c3e50; border: none;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Danh sách các trường nhập liệu
        fields = [
            ("🧴Loại Da", SKIN_TYPES, "L"),
            ("✨Công Dụng", BENEFITS, "C"),
            ("🧪Đặc Tính", FEATURES, "D"),
            ("💰Khoảng Giá", PRICES, "G"),
            ("🏷️Thương Hiệu", BRANDS, "H"),
            ("🌍Xuất Xứ", ORIGINS, "X"),
        ]

        for label, data, key in fields:
            # Label
            lbl = QLabel(label)
            lbl.setStyleSheet("font-weight: bold; font-size: 13px; border: none;")
            layout.addWidget(lbl)
            
            # ComboBox
            combo = QComboBox()
            combo.setStyleSheet("color: #2c3e50; font-family: 'Segoe UI';")
            for k, v in data.items():
                combo.addItem(f"{v}", k) # Hiển thị Value, lưu Key
            
            layout.addWidget(combo)
            self.inputs[key] = combo

        layout.addStretch() # Đẩy nút xuống dưới cùng

        # Nút Tìm Kiếm
        self.btn_search = QPushButton("TÌM SẢN PHẨM")
        self.btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_search.setStyleSheet(BUTTON_STYLE)
        self.btn_search.clicked.connect(self.on_click)
        layout.addWidget(self.btn_search)

    def on_click(self):
        # Thu thập dữ liệu từ 6 combobox
        data = [
            self.inputs["L"].currentData(),
            self.inputs["C"].currentData(),
            self.inputs["D"].currentData(),
            self.inputs["G"].currentData(),
            self.inputs["H"].currentData(),
            self.inputs["X"].currentData(),
        ]
        # Gửi tín hiệu ra ngoài (Main Window sẽ bắt tín hiệu này)
        self.search_signal.emit(data)