# This Python file uses the following encoding: utf-8
import sys
import os
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QListView,
    QVBoxLayout,
    QInputDialog,
    QMessageBox,
    QDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QDialogButtonBox,
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QFontDatabase, QFont, QPainterPath
from PySide6.QtCore import Qt, QPoint, QUrl, QRect, QSize
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from VideoWorker import VideoWorker
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from main_form import Ui_Form
from quality_dialog import VideoConfigDialog
from src.service.detection import face_detection
class TextInputDialog(QDialog):
    def __init__(self, image_path, media_items, IMAGE_WIDTH, IMAGE_HEIGHT, BLUE_WIDTH, BLUE_HEIGHT, parent=None):
        super().__init__(parent)
        self.media_items = media_items
        self.IMAGE_WIDTH = IMAGE_WIDTH
        self.IMAGE_HEIGHT = IMAGE_HEIGHT
        self.BLUE_WIDTH = BLUE_WIDTH
        self.BLUE_HEIGHT = BLUE_HEIGHT
        self.setWindowTitle("Nhập văn bản")
        self.setMinimumSize(200, 700)
        layout = QVBoxLayout(self)

        # Hiển thị ảnh preview
        self.image_label = QLabel()
        self.predictions = face_detection(image_path)
        print(self.predictions)

        original_pixmap = QPixmap(image_path)
        scaled_pixmap = original_pixmap.scaled(
            IMAGE_WIDTH, IMAGE_HEIGHT,  
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        # Tạo một bản sao để vẽ detection boxes
        preview_pixmap = scaled_pixmap.copy()
        
        # Vẽ detection boxes chỉ trên preview_pixmap
        if self.predictions and 'predictions' in self.predictions:
            painter = QPainter(preview_pixmap)
            for pred in self.predictions['predictions']:
                # Tính toán tỷ lệ scale
                scale_x = preview_pixmap.width() / self.predictions['image']['width']
                scale_y = preview_pixmap.height() / self.predictions['image']['height']
                
                # Tính toán tọa độ đã scale
                x = pred['x'] * scale_x - (pred['width'] * scale_x / 2)
                y = pred['y'] * scale_y - (pred['height'] * scale_y / 2)
                w = pred['width'] * scale_x
                h = pred['height'] * scale_y
                
                # Vẽ rectangle với màu xanh dương nhạt
                painter.setPen(QPen(QColor("#4FC3F7"), 2))
                painter.drawRect(x, y, w, h)
                
                # Vẽ text tuổi
                font_id = QFontDatabase.addApplicationFont("./temp/fonts/ChakraPetch-Medium.ttf")
                font_families = QFontDatabase.applicationFontFamilies(font_id) if font_id != -1 else ["Arial"]
                chakra_font = font_families[0] if font_families else "Arial"
                painter.setFont(QFont(chakra_font, 14))
                age_text = f"Tuổi: {pred['class_id']} ({pred['confidence']*100:.1f}%)"
                painter.setPen(QColor("#4FC3F7"))
                painter.drawText(x, y - 5, age_text)
            painter.end()
        
        # Tính toán vị trí cắt để khuôn mặt ở trung tâm
        if self.predictions and 'predictions' in self.predictions:
            # Tính trung bình vị trí của tất cả khuôn mặt
            center_x = 0
            center_y = 0
            num_faces = len(self.predictions['predictions'])
            
            for pred in self.predictions['predictions']:
                center_x += pred['x']
                center_y += pred['y']
            
            if num_faces > 0:
                center_x /= num_faces
                center_y /= num_faces
                
                # Tính tỷ lệ scale từ ảnh gốc sang ảnh đã scale
                scale_x = scaled_pixmap.width() / self.predictions['image']['width']
                scale_y = scaled_pixmap.height() / self.predictions['image']['height']
                
                # Chuyển đổi tọa độ trung tâm sang tọa độ trên ảnh đã scale
                scaled_center_x = center_x * scale_x
                scaled_center_y = center_y * scale_y
                
                # Tính vị trí cắt để đặt khuôn mặt ở trung tâm
                x = int(scaled_center_x - self.IMAGE_WIDTH / 2)
                y = int(scaled_center_y - self.IMAGE_WIDTH / 2)
                
                # Đảm bảo vị trí cắt không vượt quá biên của ảnh
                x = max(0, min(x, scaled_pixmap.width() - self.IMAGE_WIDTH))
                y = max(0, min(y, scaled_pixmap.height() - self.IMAGE_WIDTH))
            else:
                # Nếu không có khuôn mặt, cắt ở giữa như cũ
                x = (scaled_pixmap.width() - self.IMAGE_WIDTH) // 2
                y = (scaled_pixmap.height() - self.IMAGE_WIDTH) // 2
        else:
            # Nếu chưa có kết quả detection, cắt ở giữa như cũ
            x = (scaled_pixmap.width() - self.IMAGE_WIDTH) // 2
            y = (scaled_pixmap.height() - self.IMAGE_WIDTH) // 2
        
        # Sử dụng scaled_pixmap gốc để cắt và lưu
        scaled_pixmap = scaled_pixmap.copy(x, y, self.IMAGE_WIDTH, self.IMAGE_WIDTH)
        
        # Sử dụng preview_pixmap đã vẽ detection để hiển thị
        preview_pixmap = preview_pixmap.copy(x, y, self.IMAGE_WIDTH, self.IMAGE_WIDTH)

        # Tạo pixmap mới với kích thước chuẩn cho preview
        self.preview_pixmap = QPixmap(IMAGE_WIDTH, IMAGE_HEIGHT + BLUE_HEIGHT)
        self.preview_pixmap.fill(QColor("#F5F5F5"))
        
        # Tạo pixmap mới với kích thước chuẩn cho ảnh gốc
        self.original_pixmap = QPixmap(IMAGE_WIDTH, IMAGE_HEIGHT + BLUE_HEIGHT)
        self.original_pixmap.fill(QColor("#F5F5F5"))
        
        # Vẽ lên preview_pixmap
        painter = QPainter(self.preview_pixmap)
        painter.setPen(QPen(QColor("#CCCCCC"), 2))
        painter.drawRect(0, 0, IMAGE_WIDTH, IMAGE_WIDTH)
        painter.drawPixmap(0, 0, preview_pixmap)
        
        # Kiểm tra số lượng ảnh để chọn màu
        if len(self.media_items) % 2 != 0:
            painter.fillRect(0, IMAGE_HEIGHT, IMAGE_WIDTH, BLUE_WIDTH, QColor("#80423D"))
        else:
            painter.fillRect(0, IMAGE_HEIGHT, IMAGE_WIDTH, BLUE_WIDTH, QColor("#2196F3"))
        
        # Vẽ viền trắng bên trái và phải (sau khi vẽ ảnh và nền xanh)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#FFFFFF"))  # Màu trắng
        painter.drawRect(0, 0, 2, IMAGE_HEIGHT + BLUE_HEIGHT)  # Viền trái
        painter.drawRect(IMAGE_WIDTH - 2, 0, 2, IMAGE_HEIGHT + BLUE_HEIGHT)  # Viền phải
        painter.end()
        
        # Vẽ lên original_pixmap (không có detection boxes)
        painter = QPainter(self.original_pixmap)
        painter.setPen(QPen(QColor("#CCCCCC"), 2))
        painter.drawRect(0, 0, IMAGE_WIDTH, IMAGE_WIDTH)
        painter.drawPixmap(0, 0, scaled_pixmap)
        
        # Kiểm tra số lượng ảnh để chọn màu
        if len(self.media_items) % 2 != 0:
            painter.fillRect(0, IMAGE_HEIGHT, IMAGE_WIDTH, BLUE_WIDTH, QColor("#80423D"))
        else:
            painter.fillRect(0, IMAGE_HEIGHT, IMAGE_WIDTH, BLUE_WIDTH, QColor("#2196F3"))
        
        # Vẽ viền trắng bên trái và phải (sau khi vẽ ảnh và nền xanh)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#FFFFFF"))  # Màu trắng
        painter.drawRect(0, 0, 2, IMAGE_HEIGHT + BLUE_HEIGHT)  # Viền trái
        painter.drawRect(IMAGE_WIDTH - 2, 0, 2, IMAGE_HEIGHT + BLUE_HEIGHT)  # Viền phải
        painter.end()
        
        # Hiển thị preview_pixmap
        self.image_label.setPixmap(self.preview_pixmap)
        layout.addWidget(self.image_label)

        # Thêm label và input cho năm sinh
        year_layout = QVBoxLayout()
        year_label = QLabel("Năm sinh:")
        year_label.setStyleSheet("font-weight: bold;")
        year_layout.addWidget(year_label)
        
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Nhập năm sinh...")
        self.year_input.textChanged.connect(self.update_preview)
        year_layout.addWidget(self.year_input)
        layout.addLayout(year_layout)

        # Thêm label và input cho tên
        text_layout = QVBoxLayout()
        text_label = QLabel("Tên:")
        text_label.setStyleSheet("font-weight: bold;")
        text_layout.addWidget(text_label)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Nhập văn bản cho ảnh...")
        self.text_input.textChanged.connect(self.update_preview)
        text_layout.addWidget(self.text_input)
        layout.addLayout(text_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.temp_image_path = None  # Thêm biến để lưu đường dẫn ảnh tạm

    def update_preview(self, text=None):
        # Cập nhật cả preview_pixmap và original_pixmap để giữ đồng bộ caption và năm sinh
        for pixmap_type in ['preview', 'original']:
            current_pixmap = self.preview_pixmap if pixmap_type == 'preview' else self.original_pixmap
            temp_pixmap = current_pixmap.copy()
            
            painter = QPainter(temp_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Xóa phần background cũ của caption và năm sinh
            painter.fillRect(0, self.IMAGE_HEIGHT, self.IMAGE_WIDTH, self.BLUE_HEIGHT, QColor("#F5F5F5"))
            
            # Vẽ lại background màu cho phần caption
            if len(self.media_items) % 2 != 0:
                painter.fillRect(2, self.IMAGE_HEIGHT, self.IMAGE_WIDTH - 4, self.BLUE_WIDTH, QColor("#80423D"))
            else:
                painter.fillRect(2, self.IMAGE_HEIGHT, self.IMAGE_WIDTH - 4, self.BLUE_WIDTH, QColor("#2196F3"))
            
            # Tạo và cài đặt font tùy chỉnh
            font_id = QFontDatabase.addApplicationFont("./temp/fonts/Fontspring-DEMO-multipa-bold.otf")
            font_families = QFontDatabase.applicationFontFamilies(font_id) if font_id != -1 else ["Arial"]
            default_font = font_families[0] if font_families else "Arial"

            # Vẽ caption text với shadow và màu vàng
            caption_text = self.text_input.text()
            if caption_text:
                # Tạo rect cho phần nền xanh, căn giữa theo chiều ngang
                x = (self.IMAGE_WIDTH - self.BLUE_WIDTH) // 2 
                y = self.IMAGE_HEIGHT
                blue_rect = QRect(x, y, self.BLUE_WIDTH, self.BLUE_HEIGHT)
                painter.setFont(QFont(default_font, 28))
                
                # Vẽ shadow trực tiếp từ blue_rect
                shadow_offset = 2
                shadow_color = QColor(0, 0, 0, 255)
                painter.setPen(shadow_color)
                shadow_rect = blue_rect.translated(shadow_offset, shadow_offset)
                painter.drawText(shadow_rect, Qt.AlignCenter, caption_text)
                
                # Vẽ text chính màu vàng
                if len(self.media_items) % 2 == 0:  # Nếu số lượng ảnh là chẵn
                    painter.setPen(QColor("#FCE106"))
                else:
                    painter.setPen(QColor("#FFFFFF"))
                painter.drawText(blue_rect, Qt.AlignCenter, caption_text)

            # Vẽ năm sinh
            year_text = self.year_input.text()
            if year_text:
                # Sử dụng font size 18 cho năm sinh
                painter.setFont(QFont(default_font, 18))
                
                # Tính toán kích thước container
                text_width = painter.fontMetrics().horizontalAdvance(year_text) + 30  # Padding
                container_height = 40  # Giảm chiều cao container cho phù hợp với font size nhỏ hơn
                
                # Đặt container ở dưới cùng của nền xanh
                x = (self.IMAGE_WIDTH - text_width) // 2  # Căn giữa container
                y = self.IMAGE_HEIGHT - container_height  # Cách bottom 10px
                
                # Vẽ container với viền đen và nền vàng
                path = QPainterPath()
                path.addRoundedRect(x, y, text_width, container_height, 20, 20)  # Bo góc 15px
                
                # Vẽ nền vàng
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor("#FFE500"))
                painter.drawPath(path)
                
                # Vẽ viền đen
                painter.setPen(QPen(Qt.black, 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawPath(path)

                # Vẽ text năm sinh
                painter.setPen(Qt.black)
                painter.drawText(x + 16, y + container_height - 13, year_text)

            painter.end()
            
            # Cập nhật pixmap tương ứng
            if pixmap_type == 'preview':
                self.preview_pixmap = temp_pixmap
                self.image_label.setPixmap(temp_pixmap)
            else:
                self.original_pixmap = temp_pixmap

    def accept(self):
        # Tạo thư mục temp/images nếu chưa tồn tại
        temp_dir = os.path.join("temp", "images")
        os.makedirs(temp_dir, exist_ok=True)

        # Tạo tên file mới với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_image_path = os.path.join(temp_dir, f"edited_{timestamp}.png")

        # Lưu original_pixmap (không có detection boxes)
        self.original_pixmap.save(self.temp_image_path)
        super().accept()

    def get_text(self):
        return self.text_input.text(), self.year_input.text(), self.temp_image_path
