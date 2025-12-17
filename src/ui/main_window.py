# src/ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QIcon
from src.ui.styles import STYLESHEET
from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel
from src.logic.inference_engine import ExpertSystem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Chuyên Gia Tư Vấn Sữa Rửa Mặt")
        self.setWindowIcon(QIcon("assets\\icons\\logo.jpg"))
        self.resize(1100, 700)
        
        # Load style chung
        self.setStyleSheet(STYLESHEET)

        # Khởi tạo Logic Engine
        self.engine = ExpertSystem()

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính: Xếp ngang (Horizontal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20) # Căn lề ngoài
        main_layout.setSpacing(20) # Khoảng cách giữa 2 cột

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