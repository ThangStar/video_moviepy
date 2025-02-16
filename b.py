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
from VideoWorker import IMAGE_WIDTH, SCREEN_HEIGHT

BLUE_WIDTH = IMAGE_WIDTH
BLUE_HEIGHT = 80
IMAGE_HEIGHT = SCREEN_HEIGHT / 2 - BLUE_HEIGHT

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
        self.setMinimumSize(200, 600)
        layout = QVBoxLayout(self)

        # Hiển thị media
        if media_path.lower().endswith((".png", ".jpg", ".jpeg")):
            label = QLabel()
            pixmap = QPixmap(media_path)
            pixmap = pixmap.scaled(
                IMAGE_WIDTH, SCREEN_HEIGHT, Qt.KeepAspectRatio, Qt.SmoothTransformation
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
        self.setMinimumSize(200, 600)
        layout = QVBoxLayout(self)

        # Hiển thị ảnh preview
        self.image_label = QLabel()
        
        original_pixmap = QPixmap(image_path)
        scaled_pixmap = original_pixmap.scaled(
            IMAGE_WIDTH, IMAGE_HEIGHT,  
            Qt.KeepAspectRatioByExpanding,  # Sử dụng expanding để cover
            Qt.SmoothTransformation
        )
        
        # Cắt ảnh để vừa khít với khung
        if scaled_pixmap.width() > IMAGE_WIDTH or scaled_pixmap.height() > IMAGE_WIDTH:
            x = (scaled_pixmap.width() - IMAGE_WIDTH) // 2
            y = (scaled_pixmap.height() - IMAGE_WIDTH) // 2
            scaled_pixmap = scaled_pixmap.copy(x, y, IMAGE_WIDTH, IMAGE_WIDTH)
        
        # Tạo pixmap mới với kích thước chuẩn
        self.pixmap = QPixmap(IMAGE_WIDTH, IMAGE_HEIGHT + BLUE_HEIGHT)
        self.pixmap.fill(QColor("#F5F5F5"))
        
        painter = QPainter(self.pixmap)
        
        # Vẽ viền xung quanh vùng ảnh
        painter.setPen(QPen(QColor("#CCCCCC"), 2))
        painter.drawRect(0, 0, IMAGE_WIDTH, IMAGE_WIDTH)
        
        # Vẽ ảnh ở vị trí (0,0)
        painter.drawPixmap(0, 0, scaled_pixmap)
        
        # Vẽ phần nền xanh
        painter.fillRect(0, IMAGE_HEIGHT, IMAGE_WIDTH, BLUE_WIDTH, QColor("#2196F3"))
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
            # Tạo rect cho phần nền xanh, căn giữa theo chiều ngang
            x = (IMAGE_WIDTH - BLUE_WIDTH) // 2
            y = IMAGE_HEIGHT
            blue_rect = QRect(x, y, BLUE_WIDTH, BLUE_HEIGHT)
            painter.setFont(QFont(default_font, 28))
            
            # Vẽ shadow trực tiếp từ blue_rect
            shadow_offset = 2
            shadow_color = QColor(0, 0, 0, 255)
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
            x = (IMAGE_WIDTH - text_width) // 2  # Căn giữa container
            y = IMAGE_HEIGHT - container_height  # Cách bottom 10px
            
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


class VideoItemWidget(QWidget):
    def __init__(self, video_name, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        # Label hiển thị tên video
        self.video_label = QLabel(video_name)
        layout.addWidget(self.video_label)

        # Thêm nút xóa
        self.delete_button = QPushButton("Xóa")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #ff1744;
            }
            QPushButton:pressed {
                background-color: #d50000;
            }
        """)
        self.delete_button.setFixedWidth(60)
        layout.addWidget(self.delete_button)


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
        self.background_music = None

        # Load tất cả video đã xuất từ thư mục exports
        self.load_exported_videos()

        # Tự động thêm 2 file ảnh ban đầu
        initial_images = []
        
        # Tự động load tất cả file .png từ thư mục temp/images/
        images_dir = "./temp/images"
        if os.path.exists(images_dir):
            for file_name in os.listdir(images_dir):
                if file_name.lower().endswith('.png'):
                    img_path = os.path.join(images_dir, file_name)
                    # Lấy tên file làm text mặc định (bỏ phần .png)
                    text = os.path.splitext(file_name)[0]
                    initial_images.append((img_path, text))

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

        # Thêm kết nối signal cho videoList
        self.ui.videoList.itemClicked.connect(self.open_exported_video)

        # Ẩn group box progress mặc định
        self.ui.gro_progress.hide()

    def load_exported_videos(self):
        exports_dir = "./temp/exports"
        # Tạo thư mục exports nếu chưa tồn tại
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)
        
        # Xóa tất cả items hiện tại
        self.ui.videoList.clear()
        
        # Lấy danh sách tất cả file .mp4 trong thư mục exports
        for file_name in os.listdir(exports_dir):
            if file_name.lower().endswith('.mp4'):
                # Tạo item và widget tùy chỉnh
                item = QListWidgetItem(self.ui.videoList)
                widget = VideoItemWidget(file_name)
                item.setSizeHint(widget.sizeHint())
                self.ui.videoList.addItem(item)
                self.ui.videoList.setItemWidget(item, widget)
                
                # Kết nối nút xóa với hàm xử lý
                widget.delete_button.clicked.connect(
                    lambda checked, fn=file_name: self.delete_video(fn)
                )

    def delete_video(self, video_name):
        video_path = os.path.join("./temp/exports", video_name)
        try:
            # Xóa file video trực tiếp
            os.remove(video_path)
            # Cập nhật lại danh sách
            self.load_exported_videos()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể xóa video. Lỗi: {str(e)}"
            )

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

        # Hiện group box progress
        self.ui.gro_progress.show()
        self.ui.progress_video.setValue(0)
        self.ui.lbe_progress.setText("Đang xuất video...")

        # Disable button và đổi style
        self.ui.createVideoButton.setEnabled(False)
        self.ui.createVideoButton.setStyleSheet("""
            QPushButton {
                background-color: #cccccc;
                color: #666666;
                border-radius: 8px;
                font-size: 13pt;
                font-weight: bold;
                padding: 10px;
                min-height: 35px;
            }
        """)

        # Tạo thư mục exports nếu chưa tồn tại
        exports_dir = "./temp/exports"
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
        # Thêm xử lý để cập nhật progress bar
        if "%" in message:
            try:
                percentage = float(message.split("%")[0].split(": ")[1])
                self.ui.progress_video.setValue(int(percentage))
                self.ui.lbe_progress.setText(f"Đang xuất video... {percentage:.1f}%")
            except:
                pass

    def on_video_finished(self, success, message, progress_item):
        if success:
            # Xóa item tiến trình cũ
            self.ui.videoList.takeItem(self.ui.videoList.row(progress_item))
            
            # Tạo item mới với widget tùy chỉnh có nút xóa
            video_name = os.path.basename(self.video_worker.save_path)
            item = QListWidgetItem(self.ui.videoList)
            widget = VideoItemWidget(video_name)
            item.setSizeHint(widget.sizeHint())
            self.ui.videoList.addItem(item)
            self.ui.videoList.setItemWidget(item, widget)
            
            # Kết nối nút xóa với hàm xử lý
            widget.delete_button.clicked.connect(
                lambda checked, fn=video_name: self.delete_video(fn)
            )
        else:
            # Xóa item tiến trình nếu có lỗi
            self.ui.videoList.takeItem(self.ui.videoList.row(progress_item))
            QMessageBox.critical(self, "Lỗi", message)
        
        # Ẩn group box progress khi hoàn thành
        self.ui.gro_progress.hide()
        
        # Enable lại button và khôi phục style
        self.ui.createVideoButton.setEnabled(True)
        self.ui.createVideoButton.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border-radius: 8px;
                font-size: 13pt;
                font-weight: bold;
                padding: 10px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)

    def add_background_music(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn tập tin âm thanh", "", "Tập tin âm thanh (*.mp3 *.wav *.ogg)"
        )

        if file_path:
            self.background_music = file_path
            file_name = os.path.basename(file_path)
            self.ui.sound_status.setText(f"Nhạc nền: {file_name}")

    def open_exported_video(self, item):
        # Lấy widget tùy chỉnh từ item
        widget = self.ui.videoList.itemWidget(item)
        if widget:
            video_name = widget.video_label.text()
            video_path = os.path.join("./temp/exports", video_name)
            
            if os.path.exists(video_path):
                # Mở video bằng ứng dụng mặc định của hệ thống
                if sys.platform.startswith('darwin'):  # macOS
                    os.system(f'open "{video_path}"')
                elif sys.platform.startswith('win32'):  # Windows
                    os.system(f'start "" "{video_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{video_path}"')
            else:
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Không tìm thấy file video. File có thể đã bị xóa hoặc di chuyển."
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
