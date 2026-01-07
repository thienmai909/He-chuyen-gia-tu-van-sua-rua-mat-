from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QPushButton, QGridLayout
from PySide6.QtGui import QIcon, QPixmap, Qt, QPicture
from PySide6.QtCore import QSize, QMargins
from src.ui.styles import STYLESHEET
from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel
from src.logic.inference_engine import ExpertSystem

from src.ui.utility import AutoResizeLabel

WIDTH_MAIN_SCREEN = 1200
HEIGHT_MAIN_SCREEN = 700

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Chuyên Gia Tư Vấn Sữa Rửa Mặt")
        self.setWindowIcon(QIcon("assets\\icons\\logo.jpg"))
        self.resize(WIDTH_MAIN_SCREEN, HEIGHT_MAIN_SCREEN)
        
        # Load style chung
        self.setStyleSheet(STYLESHEET)

        # Khởi tạo Logic Engine
        self.engine = ExpertSystem()
        self.click_start()
        # self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.start_widget = None 
        self.btn_start = None

        # Layout chính: Xếp ngang (Horizontal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(QMargins(10, 10, 10, 10)) # Căn lề ngoài
        main_layout.setSpacing(10) # Khoảng cách giữa 2 cột

        # 1. Tạo cột trái (Input)
        self.input_panel = InputPanel()
        # self.input_panel = WizardPanel()
        # KẾT NỐI TÍN HIỆU: Khi input_panel bắn tín hiệu 'search_signal', gọi hàm handle_search
        self.input_panel.search_signal.connect(self.handle_search)
        
        # 2. Tạo cột phải (Result)
        self.result_panel = ResultPanel()

        # 3. Thêm vào layout
        main_layout.addWidget(self.input_panel)
        main_layout.addWidget(self.result_panel, stretch=1) # stretch=1 để cột phải giãn rộng hơn

    def handle_search(self, input_data):
        """Xử lý logic khi người dùng bấm tìm kiếm"""
        print(f"Main Window nhận được yêu cầu tìm kiếm: {input_data}")
        
        # Gọi engine suy luận
        result = self.engine.consult(input_data)
        
        if result:
            # Nếu có kết quả -> Cập nhật panel phải
            self.result_panel.update_product(result)
        else:
            # Nếu không -> Báo lỗi trên panel phải
            self.result_panel.show_not_found()

    def click_start(self):
        self.start_widget = QWidget()
        self.start_widget.resize(QSize(WIDTH_MAIN_SCREEN, HEIGHT_MAIN_SCREEN))
        self.setCentralWidget(self.start_widget)

        layout = QGridLayout(self.start_widget)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.image_label = AutoResizeLabel()
        self.image_label.set_image("assets/images/start.png")
        layout.addWidget(self.image_label, 0, 0)

        self.btn_img = QPixmap("assets/images/btn-yes.png")
        self.btn_start = QPushButton(parent=self.start_widget, icon=self.btn_img)
        self.btn_start.setIconSize(self.btn_img.size())
        self.btn_start.setFixedSize(self.btn_img.size())
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;                     
                background-color: #ff6b6b;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)
        self.btn_start.clicked.connect(self.setup_ui)
        self.btn_start.show()

        self.recalc_button_position()

    def recalc_button_position(self):
        # Kiểm tra xem nút đã được tạo và đang hiển thị chưa
        if not getattr(self, 'start_widget', None) or not getattr(self, 'btn_start', None):
            return
  
        try:
            screen_w = self.start_widget.width()
            screen_h = self.start_widget.height()
            btn_w = self.btn_start.width()
            btn_h = self.btn_start.height()

            # Tính toán vị trí
            x = (screen_w - btn_w) / 2
            y = (screen_h * 0.95) - (btn_h / 2) # Để 0.85 hoặc 0.9 tùy bạn

            self.btn_start.move(int(x), int(y))

        except RuntimeError:
            pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.recalc_button_position()
