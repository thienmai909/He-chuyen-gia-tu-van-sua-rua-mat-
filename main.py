import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "assets", "fonts", "Nunito-ExtraBold.ttf")
    if not os.path.exists(font_path):
        print(f"Lỗi: Không tìm thấy file font tại: {font_path}")

    QFontDatabase.addApplicationFont(font_path)
    
    app.setStyleSheet("""
        * {
            font-family: "Nunito";
        }
    """)

    # Khởi chạy cửa sổ chính
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())