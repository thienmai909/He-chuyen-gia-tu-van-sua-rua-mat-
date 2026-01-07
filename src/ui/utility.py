import os
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QResizeEvent
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
        self._pixmap = QPixmap(image_path)
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