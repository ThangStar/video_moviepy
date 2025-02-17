# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_video.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(468, 248)
        Dialog.setStyleSheet(u"\n"
"QLabel {\n"
"    font-size: 11pt;\n"
"}\n"
"QComboBox {\n"
"    padding: 5px;\n"
"    border: 1px solid #bdbdbd;\n"
"    border-radius: 4px;\n"
"    background-color: white;\n"
"    min-height: 25px;\n"
"    font-size: 10pt;\n"
"}\n"
"QComboBox:hover {\n"
"    border: 1px solid #2196F3;\n"
"}\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    padding-right: 10px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/down_arrow.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"QSpinBox {\n"
"    padding: 5px;\n"
"    border: 1px solid #bdbdbd;\n"
"    border-radius: 4px;\n"
"    background-color: white;\n"
"    font-size: 10pt;\n"
"}\n"
"QSpinBox:hover {\n"
"    border: 1px solid #2196F3;\n"
"}\n"
"         ")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.qualityComboBox = QComboBox(self.widget)
        self.qualityComboBox.addItem("")
        self.qualityComboBox.addItem("")
        self.qualityComboBox.addItem("")
        self.qualityComboBox.addItem("")
        self.qualityComboBox.addItem("")
        self.qualityComboBox.addItem("")
        self.qualityComboBox.addItem("")
        self.qualityComboBox.setObjectName(u"qualityComboBox")
        self.qualityComboBox.setMinimumSize(QSize(200, 37))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.qualityComboBox)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.threadsSpinBox = QSpinBox(self.widget)
        self.threadsSpinBox.setObjectName(u"threadsSpinBox")
        self.threadsSpinBox.setMinimumSize(QSize(200, 37))
        self.threadsSpinBox.setMinimum(1)
        self.threadsSpinBox.setMaximum(32)
        self.threadsSpinBox.setValue(16)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.threadsSpinBox)

        self.warningLabel = QLabel(self.widget)
        self.warningLabel.setObjectName(u"warningLabel")
        self.warningLabel.setStyleSheet(u"\n"
"QLabel {\n"
"    color: #FF5722;\n"
"    padding: 10px;\n"
"    font-size: 10pt;\n"
"}\n"
"         ")
        self.warningLabel.setAlignment(Qt.AlignCenter)
        self.warningLabel.setWordWrap(True)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.warningLabel)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget_2 = QWidget(Dialog)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancelButton = QPushButton(self.widget_2)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setMinimumSize(QSize(100, 35))
        self.cancelButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #f44336;\n"
"    color: white;\n"
"    border-radius: 4px;\n"
"    padding: 8px 15px;\n"
"    font-size: 11pt;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #d32f2f;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #b71c1c;\n"
"}")

        self.horizontalLayout.addWidget(self.cancelButton)

        self.confirmButton = QPushButton(self.widget_2)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMinimumSize(QSize(100, 35))
        self.confirmButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"    border-radius: 4px;\n"
"    padding: 8px 15px;\n"
"    font-size: 11pt;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #388E3C;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #1B5E20;\n"
"}")

        self.horizontalLayout.addWidget(self.confirmButton)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(Dialog)

        self.qualityComboBox.setCurrentIndex(6)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"C\u1ea5u h\u00ecnh Video", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"L\u1ef1a ch\u1ecdn c\u1ea5u h\u00ecnh Video", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Ch\u1ea5t l\u01b0\u1ee3ng video:", None))
        self.qualityComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"144p - Ch\u1ea5t l\u01b0\u1ee3ng th\u1ea5p nh\u1ea5t", None))
        self.qualityComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"480p - Ch\u1ea5t l\u01b0\u1ee3ng th\u01b0\u1eddng", None))
        self.qualityComboBox.setItemText(2, QCoreApplication.translate("Dialog", u"720p HD - Ch\u1ea5t l\u01b0\u1ee3ng cao", None))
        self.qualityComboBox.setItemText(3, QCoreApplication.translate("Dialog", u"1080p Full HD", None))
        self.qualityComboBox.setItemText(4, QCoreApplication.translate("Dialog", u"1440p QHD", None))
        self.qualityComboBox.setItemText(5, QCoreApplication.translate("Dialog", u"2K", None))
        self.qualityComboBox.setItemText(6, QCoreApplication.translate("Dialog", u"4K Ultra HD", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"S\u1ed1 lu\u1ed3ng x\u1eed l\u00fd:", None))
        self.warningLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>\u26a0\ufe0f C\u1ea3nh b\u00e1o: S\u1ed1 lu\u1ed3ng qu\u00e1 cao c\u00f3 th\u1ec3 khi\u1ebfn \u1ee9ng d\u1ee5ng c\u1ee7a b\u1ea1n b\u1ecb treo</p></body></html>", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"H\u1ee7y b\u1ecf", None))
        self.confirmButton.setText(QCoreApplication.translate("Dialog", u"X\u00e1c nh\u1eadn", None))
    # retranslateUi

