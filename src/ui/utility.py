import os
from PySide6.QtWidgets import QLabel, QSizePolicy, QPushButton
from PySide6.QtGui import QPixmap, QResizeEvent, QIcon
from PySide6.QtCore import Qt, QSize

WIDTH_MAIN_SCREEN = 1200
HEIGHT_MAIN_SCREEN = 700

class AutoResizeLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None 
        self.setAlignment(Qt.AlignCenter)

        # Cho phép Label co giãn tự do, bỏ qua kích thước thật của ảnh
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

    def set_image(self, image_path):
        if not os.path.exists(image_path):
            print(f"Cảnh báo: Không tìm thấy ảnh tại: {image_path}")
            self._pixmap = None
            return
        
        self._pixmap = QPixmap(image_path)
        if self._pixmap.isNull():
            print(f"Cảnh báo: Không thể load ảnh từ: {image_path}")
            self._pixmap = None
        self.update_display()

    def update_display(self):
        if self._pixmap and not self._pixmap.isNull():
            # Lấy kích thước hiện tại của Label (do Layout quy định)
            target_size = self.size()
            
            # Scale ảnh gốc theo kích thước đó
            scaled_pixmap = self._pixmap.scaled(
                target_size, 
                Qt.AspectRatioMode.IgnoreAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            super().setPixmap(scaled_pixmap)

    def resizeEvent(self, event: QResizeEvent):
        self.update_display()
        super().resizeEvent(event)

class HoverImageButton(QPushButton):
    def __init__(self, normal_img_path: str, hover_img_path: str, custom_size=None | QSize, parent=None):
        super().__init__(parent)
        
        # Kiểm tra file tồn tại
        if not os.path.exists(normal_img_path):
            print(f"Cảnh báo: Không tìm thấy ảnh normal tại: {normal_img_path}")
        if not os.path.exists(hover_img_path):
            print(f"Cảnh báo: Không tìm thấy ảnh hover tại: {hover_img_path}")
        
        # Load trước 2 ảnh vào bộ nhớ
        self.pixmap_normal = QPixmap(normal_img_path)
        self.pixmap_hover = QPixmap(hover_img_path)
        
        # Kiểm tra pixmap hợp lệ
        if self.pixmap_normal.isNull():
            print(f"Cảnh báo: Không thể load ảnh normal từ: {normal_img_path}")
        if self.pixmap_hover.isNull():
            print(f"Cảnh báo: Không thể load ảnh hover từ: {hover_img_path}")

        # Mặc định hiển thị ảnh Normal
        self.setIcon(QIcon(self.pixmap_normal))
        
        # Set kích thước nút bằng kích thước ảnh
        self.setIconSize(self.pixmap_normal.size())
        self.setFixedSize(self.pixmap_normal.size())
        
        # Con trỏ chuột
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if custom_size is None:
            # Nếu người dùng truyền kích thước muốn ép (VD: 100x100)
            self.setIconSize(custom_size)
            self.setFixedSize(custom_size)
        else:
            # Nếu không truyền gì thì lấy theo kích thước gốc của ảnh
            self.setIconSize(self.pixmap_normal.size())
            self.setFixedSize(self.pixmap_normal.size())

    def enterEvent(self, event):
        """Khi chuột đi VÀO -> Đổi sang ảnh Hover"""
        self.setIcon(QIcon(self.pixmap_hover))
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Khi chuột đi RA -> Đổi về ảnh Normal"""
        self.setIcon(QIcon(self.pixmap_normal))
        super().leaveEvent(event)