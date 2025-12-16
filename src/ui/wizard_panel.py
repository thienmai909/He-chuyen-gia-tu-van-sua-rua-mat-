# src/ui/wizard_panel.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QRadioButton, QPushButton, QButtonGroup, 
                               QStackedWidget, QFrame, QMessageBox, QScrollArea)
from PySide6.QtCore import Signal, Qt
from src.ui.sliding_widget import SlidingStackedWidget
from src.ui.styles import PANEL_STYLE

# Import dữ liệu
from src.logic.constants import SKIN_TYPES, BENEFITS, FEATURES, PRICES, BRANDS, ORIGINS

class WizardPanel(QFrame):
    # Tín hiệu bắn ra khi hoàn tất 6 bước (gửi dữ liệu list ra ngoài)
    search_signal = Signal(list)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(PANEL_STYLE)
        self.setFixedWidth(400) # Cột nhập liệu rộng hơn một chút để hiện rõ text

        # Dữ liệu cấu hình cho 6 bước
        # Format: (Tiêu đề Bước, Dữ liệu Nguồn, Key lưu trữ)
        self.steps_config = [
            ("Bước 1: Loại Da Của Bạn", SKIN_TYPES, "L"),
            ("Bước 2: Công Dụng Mong Muốn", BENEFITS, "C"),
            ("Bước 3: Đặc Tính Sản Phẩm", FEATURES, "D"),
            ("Bước 4: Khoảng Giá Phù Hợp", PRICES, "G"),
            ("Bước 5: Thương Hiệu Ưa Thích", BRANDS, "H"),
            ("Bước 6: Xuất Xứ Sản Phẩm", ORIGINS, "X"),
        ]
        
        # Biến lưu kết quả tạm thời: {"L": "L2", "C": "C1"...}
        self.user_choices = {} 
        self.button_groups = [] # Quản lý nhóm nút radio từng trang

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        
        # 1. Khu vực hiển thị nội dung từng bước (Stacked Widget)
        self.stack = SlidingStackedWidget()
        
        # Tạo vòng lặp để sinh ra 6 trang
        for title, data_source, key in self.steps_config:
            page = self.create_step_page(title, data_source, key)
            self.stack.addWidget(page)
            
        self.main_layout.addWidget(self.stack)

        # 2. Khu vực nút điều hướng (Back / Next) nằm dưới cùng
        nav_layout = QHBoxLayout()
        
        self.btn_back = QPushButton("Quay lại")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setEnabled(False) # Trang 1 thì tắt nút Back
        self.btn_back.setStyleSheet("background-color: #95a5a6; color: white; border: none; padding: 10px; border-radius: 5px;")
        
        self.btn_next = QPushButton("Tiếp theo")
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_next.clicked.connect(self.go_next)
        self.btn_next.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; border: none; padding: 10px; border-radius: 5px;")

        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_next)
        
        self.main_layout.addLayout(nav_layout)

    def create_step_page(self, title_text, options_dict, key):
        """Hàm hỗ trợ tạo giao diện cho 1 trang (Có thanh cuộn)"""
        page = QWidget()
        
        # Layout chính của trang: Chứa Tiêu đề + Vùng cuộn
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # 1. Tiêu đề bước (Cố định bên trên)
        lbl = QLabel(title_text)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-top: 10px; margin-bottom: 5px; border: none;")
        lbl.setWordWrap(True)
        main_layout.addWidget(lbl)

        # 2. Tạo Vùng Cuộn (Scroll Area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True) # Cho phép nội dung co giãn theo chiều ngang
        scroll.setFrameShape(QFrame.Shape.NoFrame) # Bỏ viền đen mặc định của scroll area
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                border: none; background: #f1f1f1; width: 8px; margin: 0; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7; min-height: 20px; border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: #95a5a6; }
        """)

        # 3. Widget chứa nội dung bên trong (Container)
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;") # Trong suốt để tiệp màu nền
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(5, 5, 15, 5) # Chừa lề phải nhiều chút để không bị thanh cuộn che mất nút

        # Group chứa các radio button
        btn_group = QButtonGroup(page)
        self.button_groups.append(btn_group) 

        # Tạo các Radio Button từ dữ liệu
        for code, text in options_dict.items():
            rb = QRadioButton(text)
            # Style cho Radio Button
            rb.setStyleSheet("""
                QRadioButton {
                    font-size: 14px; padding: 10px;
                    background-color: white;
                    color: #2c3e50;
                    border: 1px solid #dfe6e9; border-radius: 6px;
                }
                QRadioButton::indicator { width: 18px; height: 18px; }
                QRadioButton:checked {
                    background-color: #eaf2f8; border: 1px solid #3498db; font-weight: bold; color: #2980b9;
                }
                QRadioButton:hover {
                    border: 1px solid #bdc3c7;
                }
            """)
            
            content_layout.addWidget(rb)
            btn_group.addButton(rb)
            rb.setProperty("code_val", code)

        # Chọn mặc định cái đầu tiên
        if btn_group.buttons():
            btn_group.buttons()[0].setChecked(True)

        content_layout.addStretch() # Đẩy các nút lên trên cùng nếu ít option

        # 4. Gán nội dung vào Scroll Area
        scroll.setWidget(content_widget)
        
        # 5. Thêm Scroll Area vào layout chính của trang
        main_layout.addWidget(scroll)

        return page

    def go_next(self):
        current_idx = self.stack.currentIndex()
        total_pages = self.stack.count()

        self.save_current_step_data(current_idx)

        if current_idx < total_pages - 1:
            new_idx = current_idx + 1
            self.stack.slideInIdx(new_idx)
            self.update_nav_buttons(new_idx)
        else:
            self.finish_wizard()

    def go_back(self):
        current_idx = self.stack.currentIndex()
        if current_idx > 0:
            new_idx = current_idx - 1
            self.stack.slideInIdx(new_idx)
            self.update_nav_buttons(new_idx)

    def update_nav_buttons(self, target_idx=None):
        """Cập nhật trạng thái nút Back/Next"""
        idx = target_idx if target_idx is not None else self.stack.currentIndex()
        total = self.stack.count()

        # Nút Back: Chỉ hiện khi không phải trang 1
        self.btn_back.setEnabled(idx > 0)
        self.btn_back.setStyleSheet(f"background-color: {'#7f8c8d' if idx > 0 else '#bdc3c7'}; color: white; padding: 10px; border-radius: 5px;")

        # Nút Next: Đổi chữ thành "TÌM KIẾM" nếu là trang cuối
        if idx == total - 1:
            self.btn_next.setText("🔍 TÌM KIẾM")
            self.btn_next.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        else:
            self.btn_next.setText("Tiếp theo ➜")
            self.btn_next.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")

    def save_current_step_data(self, idx):
        """Lấy giá trị Radio Button đang chọn lưu vào biến"""
        group = self.button_groups[idx]
        checked_btn = group.checkedButton()
        
        # Lấy Key cấu hình (L, C, D...)
        key_config = self.steps_config[idx][2]
        
        if checked_btn:
            # Lấy mã code (L1, C2...) đã giấu trong property
            val = checked_btn.property("code_val")
            self.user_choices[key_config] = val
            print(f"Bước {idx+1}: Đã chọn {val}")

    def finish_wizard(self):
        """Hoàn tất, gom dữ liệu gửi ra Main Window"""
        # Đảm bảo format đúng thứ tự [L, C, D, G, H, X]
        try:
            final_data = [
                self.user_choices["L"],
                self.user_choices["C"],
                self.user_choices["D"],
                self.user_choices["G"],
                self.user_choices["H"],
                self.user_choices["X"]
            ]
            # Bắn tín hiệu ra ngoài
            self.search_signal.emit(final_data)
            
            # (Tùy chọn) Reset về trang 1 sau khi tìm? 
            # self.stack.setCurrentIndex(0) 
            # self.update_nav_buttons()
            
        except KeyError:
            QMessageBox.warning(self, "Lỗi", "Có vẻ bạn chưa chọn đủ thông tin!")
    
