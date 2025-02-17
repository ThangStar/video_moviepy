from PySide6.QtWidgets import QDialog
from quality_ui import Ui_Dialog

class VideoConfigDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent  # Lưu tham chiếu đến parent
        self.confirmButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def get_video_config(self):
        quality = self.qualityComboBox.currentText()
        
        # Map chất lượng video sang cấu hình xuất video
        config = {
            "144p": {"fps": 12, "bitrate": "100k", "crf": 55, "width": 200, "height": 124},
            "480p": {"fps": 30, "bitrate": "1000k", "crf": 26, "width": 854, "height": 480},
            "720p": {"fps": 30, "bitrate": "2000k", "crf": 23, "width": 1280, "height": 720},
            "1080p": {"fps": 30, "bitrate": "4000k", "crf": 20, "width": 1920, "height": 1080},
            "1440p": {"fps": 30, "bitrate": "6000k", "crf": 18, "width": 2560, "height": 1440},
            "2K": {"fps": 30, "bitrate": "8000k", "crf": 16, "width": 2048, "height": 1080},
            "4K": {"fps": 30, "bitrate": "12000k", "crf": 14, "width": 3840, "height": 2160}
        }
        
        # Lấy cấu hình tương ứng với chất lượng được chọn
        width = config.get(quality.split()[0], config["720p"])["width"]
        height = config.get(quality.split()[0], config["720p"])["height"]
        return {
            "fps": 30,
            "bitrate": "2000k",
            "crf": 23,
            "width": width,
            "height": height,
            "threads": self.threadsSpinBox.value()
        }
