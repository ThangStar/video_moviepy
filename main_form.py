# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(536, 668)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.addButton = QPushButton(self.widget_4)
        self.addButton.setObjectName(u"addButton")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.addButton.setFont(font)
        self.addButton.setStyleSheet(u"QPushButton#addButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font-size: 11pt;\n"
"}\n"
"QPushButton#addButton:hover {\n"
"    background-color: #43a047;\n"
"}\n"
"QPushButton#addButton:pressed {\n"
"    background-color: #388e3c;\n"
"}\n"
"QPushButton#add_sound {\n"
"    background-color: #2196F3;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font-size: 11pt;\n"
"}\n"
"QPushButton#add_sound:hover {\n"
"    background-color: #1e88e5;\n"
"}\n"
"QPushButton#add_sound:pressed {\n"
"    background-color: #1976d2;\n"
"}\n"
"QGroupBox {\n"
"    border: 1px solid #e8e8e8;\n"
"    border-radius: 6px;\n"
"    background-color: white;\n"
"    margin-top: 6px;\n"
"}\n"
"QGroupBox::title {\n"
"    color: #424242;\n"
"    padding: 0 8px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #424242;\n"
"}\n"
"\n"
"QProgressBar {\n"
"    border: 1px solid #e8e8e8;\n"
"    border-radius: 4px;\n"
"    text-align: center;\n"
""
                        "    background-color: #f8f8f8;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: #2196F3;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QPushButton#createVideoButton {\n"
"    background-color: #2196f3;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    font-size: 11pt;\n"
"    font-weight: bold;\n"
"    padding: 8px 15px;\n"
"    min-height: 30px;\n"
"    margin-bottom: 10px;\n"
"}\n"
"QPushButton#createVideoButton:hover {\n"
"    background-color: #1e88e5;\n"
"}\n"
"QPushButton#createVideoButton:pressed {\n"
"    background-color: #1976d2;\n"
"}\n"
"\n"
"QDoubleSpinBox {\n"
"    border: 1px solid #e8e8e8;\n"
"    border-radius: 4px;\n"
"    padding: 4px;\n"
"    background: white;\n"
"}\n"
"QDoubleSpinBox:hover {\n"
"    border-color: #2196F3;\n"
"}\n"
"QDoubleSpinBox:focus {\n"
"    border-color: #2196F3;\n"
"}\n"
"\n"
"QLabel#footer_label {\n"
"    color: #757575;\n"
"    font-size: 9pt;\n"
"    padding: 5px;\n"
"    margin-bottom: 5px;\n"
"    background-color: transparent;\n"
"}")
        self.addButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.addButton)

        self.add_sound = QPushButton(self.widget_4)
        self.add_sound.setObjectName(u"add_sound")
        self.add_sound.setFont(font)
        self.add_sound.setStyleSheet(u"QPushButton#add_sound {\n"
"    background-color: #2196F3;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font-size: 11pt;\n"
"}\n"
"QPushButton#add_sound:hover {\n"
"    background-color: #1e88e5;\n"
"}\n"
"QPushButton#add_sound:pressed {\n"
"    background-color: #1976d2;\n"
"}")
        self.add_sound.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.add_sound)


        self.verticalLayout_4.addWidget(self.widget_4)

        self.sound_status = QLabel(self.widget_3)
        self.sound_status.setObjectName(u"sound_status")
        self.sound_status.setMargin(5)

        self.verticalLayout_4.addWidget(self.sound_status)

        self.config_group = QGroupBox(self.widget_3)
        self.config_group.setObjectName(u"config_group")
        self.config_group.setFlat(False)
        self.config_layout = QVBoxLayout(self.config_group)
        self.config_layout.setSpacing(10)
        self.config_layout.setObjectName(u"config_layout")
        self.config_layout.setContentsMargins(15, 15, 15, 15)
        self.speed_layout = QHBoxLayout()
        self.speed_layout.setObjectName(u"speed_layout")
        self.speed_label = QLabel(self.config_group)
        self.speed_label.setObjectName(u"speed_label")

        self.speed_layout.addWidget(self.speed_label)

        self.speed_input = QDoubleSpinBox(self.config_group)
        self.speed_input.setObjectName(u"speed_input")
        self.speed_input.setMinimumSize(QSize(100, 0))
        self.speed_input.setMinimum(0.100000000000000)
        self.speed_input.setMaximum(10.000000000000000)
        self.speed_input.setSingleStep(0.100000000000000)
        self.speed_input.setValue(1.000000000000000)

        self.speed_layout.addWidget(self.speed_input)

        self.speed_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.speed_layout.addItem(self.speed_spacer)


        self.config_layout.addLayout(self.speed_layout)


        self.verticalLayout_4.addWidget(self.config_group)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 12, 0, 0)
        self.widget1 = QWidget(self.widget)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(self.widget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget1)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setKerning(True)
        self.label.setFont(font1)
        self.label.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.label)

        self.mediaList = QListWidget(self.widget1)
        self.mediaList.setObjectName(u"mediaList")
        self.mediaList.setStyleSheet(u"QListWidget {\n"
"    border: 1px solid #e8e8e8;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #f8f8f8;\n"
"    width: 8px;\n"
"    margin: 0px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #dadada;\n"
"    min-height: 30px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #c8c8c8;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")

        self.verticalLayout.addWidget(self.mediaList)


        self.horizontalLayout_2.addWidget(self.widget1)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.videoList = QListWidget(self.widget_2)
        self.videoList.setObjectName(u"videoList")
        self.videoList.setStyleSheet(u"QListWidget {\n"
"    border: 1px solid #e8e8e8;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #f8f8f8;\n"
"    width: 8px;\n"
"    margin: 0px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #dadada;\n"
"    min-height: 30px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #c8c8c8;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")

        self.verticalLayout_2.addWidget(self.videoList)


        self.horizontalLayout_2.addWidget(self.widget_2)


        self.verticalLayout_3.addWidget(self.widget)

        self.gro_progress = QGroupBox(Form)
        self.gro_progress.setObjectName(u"gro_progress")
        self.verticalLayout_5 = QVBoxLayout(self.gro_progress)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lbe_progress = QLabel(self.gro_progress)
        self.lbe_progress.setObjectName(u"lbe_progress")
        self.lbe_progress.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.lbe_progress)

        self.progress_video = QProgressBar(self.gro_progress)
        self.progress_video.setObjectName(u"progress_video")
        self.progress_video.setValue(50)

        self.verticalLayout_5.addWidget(self.progress_video)


        self.verticalLayout_3.addWidget(self.gro_progress)

        self.createVideoButton = QPushButton(Form)
        self.createVideoButton.setObjectName(u"createVideoButton")
        self.createVideoButton.setMinimumSize(QSize(0, 46))
        self.createVideoButton.setFont(font)
        self.createVideoButton.setStyleSheet(u"QPushButton#createVideoButton {\n"
"        background-color: #2196f3;\n"
"        color: white;\n"
"        border-radius: 6px;\n"
"        font-size: 11pt;\n"
"        font-weight: bold;\n"
"        padding: 8px 15px;\n"
"        min-height: 30px;\n"
"      }\n"
"      QPushButton#createVideoButton:hover {\n"
"        background-color: #1e88e5;\n"
"      }\n"
"      QPushButton#createVideoButton:pressed {\n"
"        background-color: #1976d2;\n"
"      }")
        icon = QIcon()
        icon.addFile(u"icons/video-camera.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.createVideoButton.setIcon(icon)
        self.createVideoButton.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.createVideoButton)

        self.footer_label = QLabel(Form)
        self.footer_label.setObjectName(u"footer_label")
        self.footer_label.setMinimumSize(QSize(0, 30))
        self.footer_label.setMaximumSize(QSize(16777215, 30))
        self.footer_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.footer_label)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"T\u1ea1o Video", None))
        self.addButton.setText(QCoreApplication.translate("Form", u"+ Th\u00eam \u1ea3nh/video", None))
        self.add_sound.setText(QCoreApplication.translate("Form", u"+ Th\u00eam nh\u1ea1c n\u1ec1n", None))
        self.sound_status.setText(QCoreApplication.translate("Form", u"Nh\u1ea1c n\u1ec1n: Ch\u01b0a c\u00f3", None))
        self.config_group.setTitle(QCoreApplication.translate("Form", u"C\u1ea5u h\u00ecnh", None))
        self.speed_label.setText(QCoreApplication.translate("Form", u"T\u1ed1c \u0111\u1ed9 video (x):", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">T\u00e0i nguy\u00ean</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt;\">Video \u0111\u00e3 xu\u1ea5t</span></p></body></html>", None))
        self.gro_progress.setTitle(QCoreApplication.translate("Form", u"Tr\u1ea1ng th\u00e1i", None))
        self.lbe_progress.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u0110ang xu\u1ea5t video..</p></body></html>", None))
        self.createVideoButton.setText(QCoreApplication.translate("Form", u"  T\u1ea0O VIDEO", None))
        self.footer_label.setText(QCoreApplication.translate("Form", u"@TSTool | version: 1.0.1", None))
    # retranslateUi

