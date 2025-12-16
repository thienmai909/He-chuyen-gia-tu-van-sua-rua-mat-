# main.py
import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Khởi chạy cửa sổ chính
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())