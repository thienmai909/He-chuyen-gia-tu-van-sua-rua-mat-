import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from src.utils.resource_manager import get_asset_path, resource_exists
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load font using resource manager
    font_path = get_asset_path("fonts", "Nunito-ExtraBold.ttf")
    
    if not resource_exists("assets", "fonts", "Nunito-ExtraBold.ttf"):
        print(f"Cảnh báo: Không tìm thấy file font tại: {font_path}")
        print("Ứng dụng sẽ sử dụng font mặc định của hệ thống.")
    else:
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Cảnh báo: Không thể load font từ: {font_path}")
        else:
            print(f"Đã load font thành công từ: {font_path}")
    
    app.setStyleSheet("""
        * {
            font-family: "Nunito";
        }
    """)

    # Khởi chạy cửa sổ chính
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())