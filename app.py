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


class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.drawing_image = None
        self.last_point = None
        self.drawing = False
        self.brush_size = 3
        self.brush_color = QColor(0, 0, 0)  # Màu đen


class MediaPreviewDialog(QDialog):
    def __init__(self, media_path, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xem trước media")
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout(self)

        # Hiển thị media
        if media_path.lower().endswith((".png", ".jpg", ".jpeg")):
            label = QLabel()
            pixmap = QPixmap(media_path)
            pixmap = pixmap.scaled(
                780, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            label.setPixmap(pixmap)
            layout.addWidget(label)
        else:  # Video
            video_widget = QVideoWidget()
            self.media_player = QMediaPlayer()
            self.media_player.setVideoOutput(video_widget)
            self.media_player.setSource(QUrl.fromLocalFile(media_path))
            layout.addWidget(video_widget)
            self.media_player.play()

        # Hiển thị text
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 14pt; padding: 10px;")
        text_label.setWordWrap(True)
        layout.addWidget(text_label)


class MediaItemWidget(QWidget):
    def __init__(self, media_path, text, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Widget hiển thị media
        self.media_widget = QLabel()
        if media_path.lower().endswith((".png", ".jpg", ".jpeg")):
            pixmap = QPixmap(media_path)
            # Giảm kích thước của ảnh thumbnail
            pixmap = pixmap.scaled(
                160, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.media_widget.setPixmap(pixmap)
        else:  # Video
            # Tạo một pixmap mặc định cho video với kích thước nhỏ hơn
            video_pixmap = QPixmap(160, 120)
            video_pixmap.fill(QColor("#f0f0f0"))
            painter = QPainter(video_pixmap)

            # Điều chỉnh vị trí của biểu tượng play
            painter.setPen(QPen(QColor("#666666"), 2))
            painter.setBrush(QColor("#666666"))
            points = [
                QPoint(65, 45),  # Đỉnh trái
                QPoint(105, 60),  # Đỉnh phải
                QPoint(65, 75),  # Đỉnh dưới
            ]
            painter.drawPolygon(points)
            painter.end()

            self.media_widget.setPixmap(video_pixmap)

        self.media_widget.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.media_widget)

        # Widget hiển thị text với font size nhỏ hơn
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("font-size: 9pt; color: #333;")
        layout.addWidget(text_label)

        # Thiết lập style cho widget
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 6px;
                margin: 5px;  /* Thêm margin để tránh items chạm nhau */
            }
            QWidget:hover {
                border: 1px solid #2196f3;
            }
        """)
        # Giảm kích thước cố định của widget
        self.setFixedSize(180, 180)  # Đảm bảo kích thước nhỏ hơn grid size


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListView.IconMode)
        self.setSpacing(15)  # Khoảng cách giữa các items
        self.setResizeMode(QListView.Adjust)
        self.setWrapping(True)
        self.setMovement(QListView.Static)
        self.setMinimumHeight(300)
        
        # Thêm các thuộc tính mới để fix lỗi đè item
        self.setUniformItemSizes(True)  # Đảm bảo các item có kích thước đồng nhất
        self.setGridSize(QSize(200, 200))  # Đặt kích thước grid lớn hơn item size
        self.setFlow(QListView.LeftToRight)  # Sắp xếp từ trái sang phải
        self.setHorizontalScrollMode(QListView.ScrollPerPixel)
        self.setVerticalScrollMode(QListView.ScrollPerPixel)


class TextInputDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nhập văn bản")
        self.setMinimumSize(400, 500)
        layout = QVBoxLayout(self)

        # Hiển thị ảnh preview
        self.image_label = QLabel()
        
        # Đọc và scale ảnh gốc thành 340x340 với chế độ cover
        original_pixmap = QPixmap(image_path)
        scaled_pixmap = original_pixmap.scaled(
            340, 340, 
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        
        # Cắt ảnh để vừa khít với khung 340x340
        if scaled_pixmap.width() > 340 or scaled_pixmap.height() > 340:
            x = (scaled_pixmap.width() - 340) // 2 if scaled_pixmap.width() > 340 else 0
            y = (scaled_pixmap.height() - 340) // 2 if scaled_pixmap.height() > 340 else 0
            scaled_pixmap = scaled_pixmap.copy(x, y, 340, 340)
        
        # Tạo pixmap mới với kích thước 340x440 (thêm 100px cho phần nền xanh)
        self.pixmap = QPixmap(340, 440)
        self.pixmap.fill(Qt.white)  # Đặt nền trắng
        
        # Vẽ ảnh và nền xanh
        painter = QPainter(self.pixmap)
        # Vẽ ảnh đã scale
        painter.drawPixmap(
            (340 - scaled_pixmap.width()) // 2, 
            0, 
            scaled_pixmap
        )
        # Vẽ nền xanh với chiều cao 100px
        painter.fillRect(0, 340, 340, 100, QColor("#2196F3"))
        painter.end()
        
        self.image_label.setPixmap(self.pixmap)
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
        # Tạo bản sao của pixmap gốc
        temp_pixmap = self.pixmap.copy()
        painter = QPainter(temp_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Tạo và cài đặt font tùy chỉnh
        font_id = QFontDatabase.addApplicationFont("./temp/fonts/Fontspring-DEMO-multipa-bold.otf")
        font_families = QFontDatabase.applicationFontFamilies(font_id) if font_id != -1 else ["Arial"]
        default_font = font_families[0] if font_families else "Arial"

        # Vẽ caption text với shadow và màu vàng
        caption_text = self.text_input.text()
        if caption_text:
            # Tạo rect chỉ cho phần nền xanh
            blue_rect = QRect(10, 340, 320, 100)  # Margin 10px từ mỗi bên
            painter.setFont(QFont(default_font, 28))
            
            # Vẽ shadow với độ mờ cao hơn (alpha tăng từ 180 lên 240)
            shadow_offset = 2
            shadow_color = QColor(0, 0, 0, 255)  # Tăng alpha từ 180 lên 240
            painter.setPen(shadow_color)
            shadow_rect = blue_rect.translated(shadow_offset, shadow_offset)
            painter.drawText(shadow_rect, Qt.AlignCenter, caption_text)
            
            # Vẽ text chính màu vàng
            painter.setPen(QColor("#FCE106"))
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
            x = (340 - text_width) // 2  # Căn giữa container
            y = 340 - container_height  # Cách bottom 10px
            
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
        self.image_label.setPixmap(temp_pixmap)

    def accept(self):
        # Tạo thư mục temp/images nếu chưa tồn tại
        temp_dir = os.path.join("temp", "images")
        os.makedirs(temp_dir, exist_ok=True)

        # Tạo tên file mới với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_image_path = os.path.join(temp_dir, f"edited_{timestamp}.png")

        # Lưu ảnh đã chỉnh sửa
        self.image_label.pixmap().save(self.temp_image_path)
        super().accept()

    def get_text(self):
        return self.text_input.text(), self.year_input.text(), self.temp_image_path


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Thay thế QListWidget mặc định bằng CustomListWidget
        self.media_list = CustomListWidget()
        layout = self.ui.widget1.layout()
        layout.replaceWidget(self.ui.mediaList, self.media_list)
        self.ui.mediaList.deleteLater()
        self.ui.mediaList = self.media_list

        # Thiết lập style cho cửa sổ chính
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)

        # Khởi tạo danh sách media
        self.media_items = []
        self.background_music = None  # Thêm biến để lưu đường dẫn nhạc nền

        # Tự động thêm 2 file ảnh ban đầu
        initial_images = [
            ("3.png", "test1"),
            ("4.png", "test2"),
            ("temp\images\edited_20250214_092949.png", "test3"),
            ("temp\images\edited_20250214_092949.png", "test3"),
            ("temp\images\edited_20250214_092949.png", "test3"),
            ("temp\images\edited_20250214_092949.png", "test3"),
            ("temp\images\edited_20250214_092949.png", "test3"),
            ("temp\images\edited_20250214_092949.png", "test3"),
            ("temp\images\edited_20250214_092949.png", "test3"),
            ("temp\images\edited_20250214_092949.png", "test3"),
        ]
        
        for img_path, text in initial_images:
            if os.path.exists(img_path):
                # Tạo custom widget cho item
                item_widget = MediaItemWidget(img_path, text)
                item = QListWidgetItem(self.ui.mediaList)
                item.setSizeHint(item_widget.sizeHint())
                self.ui.mediaList.addItem(item)
                self.ui.mediaList.setItemWidget(item, item_widget)
                self.media_items.append((img_path, text))

        # Kết nối các signals
        self.ui.addButton.clicked.connect(self.add_media_item)
        self.ui.createVideoButton.clicked.connect(self.create_video)
        self.ui.mediaList.itemClicked.connect(self.show_media_preview)
        self.ui.add_sound.clicked.connect(self.add_background_music)

    def add_media_item(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn tập tin media",
            "",
            "Tập tin media (*.png *.jpg *.jpeg *.mp4 *.avi *.mov)",
        )

        if file_path:
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                dialog = TextInputDialog(file_path, self)
                if dialog.exec() == QDialog.Accepted:
                    text, year, edited_image_path = dialog.get_text()
                    display_text = f"{year}\n{text}" if year else text
                    # Sử dụng ảnh đã chỉnh sửa thay vì ảnh gốc
                    item_widget = MediaItemWidget(edited_image_path, display_text)
                    item = QListWidgetItem(self.ui.mediaList)
                    item.setSizeHint(item_widget.sizeHint())
                    self.ui.mediaList.addItem(item)
                    self.ui.mediaList.setItemWidget(item, item_widget)
                    # Lưu đường dẫn ảnh đã chỉnh sửa vào danh sách
                    self.media_items.append((edited_image_path, display_text))
            else:
                # Xử lý cho video như cũ
                text, ok = QInputDialog.getText(
                    self, "Thêm văn bản", "Nhập văn bản cho media này:"
                )
                if ok:
                    item_widget = MediaItemWidget(file_path, text)
                    item = QListWidgetItem(self.ui.mediaList)
                    item.setSizeHint(item_widget.sizeHint())
                    self.ui.mediaList.addItem(item)
                    self.ui.mediaList.setItemWidget(item, item_widget)
                    self.media_items.append((file_path, text))

    def show_media_preview(self, item):
        index = self.ui.mediaList.row(item)
        if index < len(self.media_items):
            media_path, text = self.media_items[index]
            dialog = MediaPreviewDialog(media_path, text, self)
            dialog.exec()

    def create_video(self):
        if not self.media_items:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng thêm một số mục media trước!")
            return

        # Tạo thư mục exports nếu chưa tồn tại
        exports_dir = "exports"
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)

        # Tạo tên file tự động với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(exports_dir, f"video_{timestamp}.mp4")

        # Thêm item vào list để hiển thị tiến trình
        progress_item = QListWidgetItem("Đang xử lý...")
        self.ui.videoList.addItem(progress_item)

        # Tạo và chạy worker
        self.video_worker = VideoWorker(self.media_items, save_path, self.background_music)
        self.video_worker.progress.connect(lambda msg: self.update_progress(msg, progress_item))
        self.video_worker.finished.connect(
            lambda success, msg: self.on_video_finished(success, msg, progress_item)
        )
        self.video_worker.start()

    def update_progress(self, message, item):
        item.setText(message)

    def on_video_finished(self, success, message, progress_item):
        if success:
            # Thay thế item tiến trình bằng tên file video
            progress_item.setText(os.path.basename(self.video_worker.save_path))
        else:
            # Xóa item tiến trình nếu có lỗi
            self.ui.videoList.takeItem(self.ui.videoList.row(progress_item))
            QMessageBox.critical(self, "Lỗi", message)

    def add_background_music(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn tập tin âm thanh", "", "Tập tin âm thanh (*.mp3 *.wav *.ogg)"
        )

        if file_path:
            self.background_music = file_path
            file_name = os.path.basename(file_path)
            self.ui.sound_status.setText(f"Nhạc nền: {file_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
