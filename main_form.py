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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1024, 768)
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
        self.addButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font-size: 11pt;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #45a049;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #3d8b40;\n"
"}")
        self.addButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.addButton)

        self.add_sound = QPushButton(self.widget_4)
        self.add_sound.setObjectName(u"add_sound")
        self.add_sound.setFont(font)
        self.add_sound.setStyleSheet(u"QPushButton {\n"
"    background-color: #2196F3;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 8px 15px;\n"
"    font-size: 11pt;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #1976D2;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #1565C0;\n"
"}")
        self.add_sound.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.add_sound)


        self.verticalLayout_4.addWidget(self.widget_4)

        self.sound_status = QLabel(self.widget_3)
        self.sound_status.setObjectName(u"sound_status")

        self.verticalLayout_4.addWidget(self.sound_status)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 12, 0, 0)
        self.widget1 = QWidget(self.widget)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setMinimumSize(QSize(300, 0))
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

        self.verticalLayout_2.addWidget(self.videoList)


        self.horizontalLayout_2.addWidget(self.widget_2)


        self.verticalLayout_3.addWidget(self.widget)

        self.createVideoButton = QPushButton(Form)
        self.createVideoButton.setObjectName(u"createVideoButton")
        self.createVideoButton.setMinimumSize(QSize(0, 65))
        self.createVideoButton.setStyleSheet(u"QPushButton {\n"
"        background-color: #2196f3;\n"
"        color: white;\n"
"        border-radius: 8px;\n"
"        font-size: 13pt;\n"
"        font-weight: bold;\n"
"        padding: 10px;\n"
"        min-height: 45px;\n"
"      }\n"
"      QPushButton:hover {\n"
"        background-color: #1976d2;\n"
"        transition: background-color 0.3s;\n"
"      }\n"
"      QPushButton:pressed {\n"
"        background-color: #0d47a1;\n"
"      }")

        self.verticalLayout_3.addWidget(self.createVideoButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"T\u1ea1o Video", None))
        self.addButton.setText(QCoreApplication.translate("Form", u"+ Th\u00eam \u1ea3nh/video", None))
        self.add_sound.setText(QCoreApplication.translate("Form", u"+ Th\u00eam nh\u1ea1c n\u1ec1n", None))
        self.sound_status.setText(QCoreApplication.translate("Form", u"Nh\u1ea1c n\u1ec1n: Ch\u01b0a c\u00f3", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">T\u00e0i nguy\u00ean</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt;\">Video \u0111\u00e3 xu\u1ea5t</span></p></body></html>", None))
        self.createVideoButton.setText(QCoreApplication.translate("Form", u"T\u1ea0O VIDEO", None))
    # retranslateUi

