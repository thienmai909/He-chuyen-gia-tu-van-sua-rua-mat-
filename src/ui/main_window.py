from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QPushButton, QGridLayout
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtCore import QSize, QMargins
from src.ui.styles import STYLESHEET
from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel
from src.logic.inference_engine import ExpertSystem
from src.utils.resource_manager import get_asset_path

from src.ui.utility import AutoResizeLabel, HoverImageButton

WIDTH_MAIN_SCREEN = 1200
HEIGHT_MAIN_SCREEN = 700

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Chuyên Gia Tư Vấn Sữa Rửa Mặt")
        self.setWindowIcon(QIcon(get_asset_path("icons", "logo.jpg")))
        self.resize(WIDTH_MAIN_SCREEN, HEIGHT_MAIN_SCREEN)
        
        self.setStyleSheet(STYLESHEET)

        self.engine = ExpertSystem()
        self.start_screen()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.start_widget = None 
        self.btn_start = None

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(QMargins(10, 10, 10, 10)) # Căn lề ngoài
        main_layout.setSpacing(10) # Khoảng cách giữa 2 cột

        self.input_panel = InputPanel()
        self.input_panel.search_signal.connect(self.handle_search)
        
        self.result_panel = ResultPanel()

        main_layout.addWidget(self.input_panel)
        main_layout.addWidget(self.result_panel, stretch=1) # stretch=1 để cột phải giãn rộng hơn

    def handle_search(self, input_data):
        """Xử lý logic khi người dùng bấm tìm kiếm"""
        print(f"Main Window nhận được yêu cầu tìm kiếm: {input_data}")
        
        # Gọi engine suy luận
        result = self.engine.consult(input_data)
        
        if result:
            self.result_panel.update_product(result)
        else:
            self.result_panel.show_not_found()

    def start_screen(self):
        self.start_widget = QWidget()
        self.start_widget.resize(QSize(WIDTH_MAIN_SCREEN, HEIGHT_MAIN_SCREEN))
        self.setCentralWidget(self.start_widget)

        layout = QGridLayout(self.start_widget)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))

        # Background Image Label
        self.image_label = AutoResizeLabel()
        self.image_label.set_image(get_asset_path("images", "start.png"))
        layout.addWidget(self.image_label, 0, 0)
        
        # --- BUTTON NO (CLOSE) ---
        self.btn_no = HoverImageButton(
            normal_img_path=get_asset_path("images", "btn-no.png"),
            hover_img_path=get_asset_path("images", "btn-no-hover.png"),
            parent=self.start_widget
        )
        self.btn_no.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_no.setStyleSheet(BUTTON_START_SHEET)
        self.btn_no.show()
        self.btn_no.clicked.connect(self.click_close)

        # --- BUTTON YES (START) ---
        btn_yes_path = get_asset_path("images", "btn-yes.png")
        btn_size_start = QPixmap(btn_yes_path).size() * 2
        self.btn_start = HoverImageButton(
            normal_img_path=btn_yes_path,
            hover_img_path=get_asset_path("images", "btn-yes-hover.png"),
            custom_size=btn_size_start,
            parent=self.start_widget
        )
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.setStyleSheet(BUTTON_START_SHEET)
        self.btn_start.show()
        self.btn_start.clicked.connect(self.setup_ui)

        # Tính toán vị trí lần đầu
        self.recalc_button_position()

    def recalc_button_position(self):
        # Kiểm tra nếu các nút chưa được khởi tạo thì không làm gì cả
        if not getattr(self, 'start_widget', None) or \
           not getattr(self, 'btn_start', None) or \
           not getattr(self, 'btn_no', None):
            return

        try:
            screen_w = self.start_widget.width()
            screen_h = self.start_widget.height()
            
            w_yes = self.btn_start.width()
            w_no = self.btn_no.width()
            
            # Khoảng cách giữa 2 nút (pixel)
            spacing = 100 

            # --- TÍNH TOÁN VỊ TRÍ Y (Cao độ) ---
            # Đặt nút ở vị trí 82% chiều cao màn hình (gần đáy)
            pos_y = int(screen_h * 0.82) 

            # --- TÍNH TOÁN VỊ TRÍ X (Ngang) ---
            # Tổng chiều rộng của cả cụm = (Rộng Nút No) + (Khoảng cách) + (Rộng Nút Yes)
            total_group_width = w_no + spacing + w_yes
            
            start_x = (screen_w - total_group_width) / 3

            self.btn_no.move(int(start_x), pos_y)

            self.btn_start.move(int(start_x + w_no + spacing), pos_y)

        except RuntimeError:
            pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.recalc_button_position()

    def click_close(self):
        self.close()

BUTTON_START_SHEET = """
    QPushButton {
        border: none;
        background: transparent;
        /* Đặt radius thật lớn để nút luôn tròn dù kích thước nào */
        border-radius: 25px; 
    }
    QPushButton:hover {
        /* Hiệu ứng mờ đen khi hover */
        background-color: rgba(0, 0, 0, 0.1);
    }
    QPushButton:pressed {
        background-color: rgba(0, 0, 0, 0.3);
    }
"""