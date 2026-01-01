# Bảng màu chủ đạo (Color Palette)
PRIMARY_COLOR = "#2980b9"   # Xanh dương đậm
HOVER_COLOR = "#3498db"     # Xanh dương nhạt
BG_COLOR = "#ecf0f1"        # Xám nhạt nền
TEXT_COLOR = "#2c3e50"      # Màu chữ đen xám
WHITE = "#ffffff"

# CSS cho toàn bộ ứng dụng
STYLESHEET = f"""
    QMainWindow {{
        background-color: {BG_COLOR};
    }}
    QLabel {{
        color: {TEXT_COLOR};
    }}
    QComboBox {{
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        padding: 5px;
        background-color: white;
        font-size: 14px;
        color: {TEXT_COLOR}
    }}
    QComboBox::drop-down {{
        border: 0px;
    }}
"""

# Style riêng cho nút bấm
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {PRIMARY_COLOR};
        color: white;
        font-weight: bold;
        font-size: 15px;
        border-radius: 6px;
        padding: 10px;
    }}
    QPushButton:hover {{
        background-color: {HOVER_COLOR};
    }}
"""

# Style cho khung chứa (Panel)
PANEL_STYLE = """
    QFrame {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #dcdcdc;
    }
"""