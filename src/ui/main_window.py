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
        self.image_label = AutoResizeLabel(parent=self.start_widget)
        self.image_label.set_image(get_asset_path("images", "start.jpg"))
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

        # --- BUTTON HOTLINE (lienhe) ---
        btn_hotline_path = get_asset_path("images", "btn-lienhe.png")
        btn_size_hotline = QPixmap(btn_hotline_path).size()
        self.btn_hotline = HoverImageButton(
            normal_img_path=btn_hotline_path,
            hover_img_path=get_asset_path("images", "btn-lienhe-hover.png"),
            custom_size=btn_size_hotline,
            parent=self.start_widget
        )
        self.btn_hotline.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hotline.setStyleSheet(BUTTON_START_SHEET)
        self.btn_hotline.show()
        self.btn_hotline.clicked.connect(self.hotline)

        # Tính toán vị trí lần đầu
        self.recalc_button_position()

    def recalc_button_position(self):
        # 1. Kiểm tra an toàn
        if not getattr(self, 'start_widget', None) or \
           not getattr(self, 'btn_start', None) or \
           not getattr(self, 'btn_no', None) or \
           not getattr(self, 'btn_hotline', None):
            return

        try:
            # Lấy kích thước màn hình
            screen_w = self.start_widget.width()
            screen_h = self.start_widget.height()
            
            # Lấy kích thước các nút
            w_yes = self.btn_start.width()
            h_yes = self.btn_start.height() # Cần chiều cao để căn giữa dọc
            
            w_no = self.btn_no.width()
            h_no = self.btn_no.height()
            
            w_hot = self.btn_hotline.width()
            h_hot = self.btn_hotline.height()

            spacing_center = 100 # Khoảng cách giữa nút No và Start
            
            # Tính tổng chiều rộng cụm giữa
            total_group_width = w_no + spacing_center + w_yes
            
            # Tính điểm bắt đầu X để căn giữa màn hình
            start_x = (screen_w - total_group_width) / 3

            # Tính vị trí Y (Cao độ) - Đặt ở 82% màn hình
            base_y = int(screen_h * 0.82)
            
            # Tính đường tâm của nút to nhất (Nút Start)
            center_line_y = base_y + (h_yes / 2)

            y_no = int(center_line_y - (h_no / 2))
            self.btn_no.move(int(start_x), y_no)

            self.btn_start.move(int(start_x + w_no + spacing_center), base_y)

            margin_right = 30  # Cách lề phải 30px
            margin_top = 30    # Cách lề trên 30px

            # Công thức tính X: Tổng chiều rộng màn hình - Chiều rộng nút - Lề phải
            x_hot = screen_w - w_hot - margin_right
            
            # Công thức tính Y: Lề trên
            y_hot = margin_top

            self.btn_hotline.move(int(x_hot), int(y_hot))
        except RuntimeError:
            pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.recalc_button_position()
        self.recalc_button_back_position()

    def click_close(self):
        self.close()
    
    def hotline(self):
        self.hotline_widget = QWidget()
        self.hotline_widget.resize(QSize(WIDTH_MAIN_SCREEN, HEIGHT_MAIN_SCREEN))
        self.setCentralWidget(self.hotline_widget)

        layout = QGridLayout(self.hotline_widget)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.image_hotline = AutoResizeLabel()
        self.image_hotline.set_image(get_asset_path("images", "bg-hotline.png"))
        layout.addWidget(self.image_hotline, 0, 0)

        # Button Back
        self.btn_back = HoverImageButton(
            normal_img_path=get_asset_path("images", "btn-back.png"),
            hover_img_path=get_asset_path("images", "btn-back-hover.png"),
            parent=self.hotline_widget
        )
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setStyleSheet(BUTTON_START_SHEET)
        self.btn_back.show()
        self.btn_back.clicked.connect(self.start_screen)

        self.recalc_button_back_position()
    
    def recalc_button_back_position(self):
        if not getattr(self, 'btn_back', None):
            return

        screen_w = self.start_widget.width()
        screen_h = self.start_widget.height()

        self.btn_back.move((screen_w * 0.4), (screen_h * 0.85))


BUTTON_START_SHEET = """
    QPushButton {
        border: none;
        background: transparent;
        /* Đặt radius thật lớn để nút luôn tròn dù kích thước nào */
        border-radius: 50px; 
    }
"""