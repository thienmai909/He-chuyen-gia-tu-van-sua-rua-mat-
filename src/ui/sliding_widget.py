# src/ui/sliding_widget.py
from PySide6.QtWidgets import QStackedWidget, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QParallelAnimationGroup

class SlidingStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Thời gian trượt (mili giây) - 300ms là chuẩn mượt
        self.m_duration = 300 
        
        # Kiểu chuyển động (nhanh dần rồi chậm dần)
        self.m_easing_curve = QEasingCurve.Type.OutCubic 

    def slideInIdx(self, next_idx):
        """Hàm chính để chuyển trang với hiệu ứng trượt"""
        curr_idx = self.currentIndex()
        
        # Nếu đang ở đúng trang đó rồi thì không làm gì
        if curr_idx == next_idx:
            return

        # Tính hướng trượt: 
        # Nếu next > current (Ví dụ trang 1 -> 2): Trượt sang trái (hướng tới)
        # Nếu next < current (Ví dụ trang 2 -> 1): Trượt sang phải (hướng lùi)
        offset_x = self.frameRect().width()
        if next_idx > curr_idx:
            direction = 1 # Trang mới bay từ bên phải vào
        else:
            direction = -1 # Trang mới bay từ bên trái vào
            offset_x = -offset_x

        # Lấy widget hiện tại và widget tiếp theo
        current_widget = self.widget(curr_idx)
        next_widget = self.widget(next_idx)

        # Đặt lại kích thước cho widget tiếp theo (đề phòng cửa sổ bị resize)
        next_widget.setGeometry(0, 0, self.frameRect().width(), self.frameRect().height())

        # Vị trí ban đầu của next_widget (Nằm ngoài khung nhìn)
        start_pos_next = QPoint(offset_x, 0)
        end_pos_next = QPoint(0, 0)
        
        # Vị trí kết thúc của current_widget (Sẽ bị đẩy ra ngoài)
        start_pos_curr = QPoint(0, 0)
        end_pos_curr = QPoint(-offset_x, 0)

        # Thiết lập vị trí
        next_widget.move(start_pos_next)
        next_widget.show()
        next_widget.raise_() # Đưa lên lớp trên cùng

        # --- TẠO ANIMATION ---
        self.anim_group = QParallelAnimationGroup(self)

        # 1. Animation cho trang CŨ (Trượt ra ngoài)
        anim_curr = QPropertyAnimation(current_widget, b"pos")
        anim_curr.setDuration(self.m_duration)
        anim_curr.setEasingCurve(self.m_easing_curve)
        anim_curr.setStartValue(start_pos_curr)
        anim_curr.setEndValue(end_pos_curr)

        # 2. Animation cho trang MỚI (Trượt vào trong)
        anim_next = QPropertyAnimation(next_widget, b"pos")
        anim_next.setDuration(self.m_duration)
        anim_next.setEasingCurve(self.m_easing_curve)
        anim_next.setStartValue(start_pos_next)
        anim_next.setEndValue(end_pos_next)

        self.anim_group.addAnimation(anim_curr)
        self.anim_group.addAnimation(anim_next)

        # Khi chạy xong thì set chính thức trang đó là current
        self.anim_group.finished.connect(lambda: self.on_animation_finished(next_idx))
        
        # Bắt đầu chạy
        self.anim_group.start()

    def on_animation_finished(self, index):
        self.setCurrentIndex(index)