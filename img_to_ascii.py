import cv2
import os
from PIL import Image, ImageDraw, ImageFont
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog, QRadioButton, QLabel, \
    QVBoxLayout, QComboBox, QLineEdit, QMessageBox, QGroupBox, QGridLayout, QCheckBox, QTextEdit, QDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.addWidget(self.saveInfoGroup(), 0, 0)

        self.setLayout(grid)

        self.setWindowTitle('Image to ASCII')
        self.resize(300, 150)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def saveInfoGroup(self):
        global nw, w_num
        nw = ''

        groupbox = QGroupBox('')

        btn1 = QPushButton("적용할 이미지", self)
        btn1.clicked.connect(self.openFileNameDialog)

        w_num = QLineEdit(self)
        w_num.setPlaceholderText('가로 크기 (기본 50)')
        w_num.textChanged.connect(self.nwInput)

        btn2 = QPushButton("아스키코드", self)
        btn2.clicked.connect(self.textGroup)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(w_num)
        vbox.addWidget(btn2)
        groupbox.setLayout(vbox)

        return groupbox

    def nwInput(self, text):
        global nw
        nw = text

    def openFileNameDialog(self):
        global img

        fileName, _ = QFileDialog.getOpenFileName(self, "적용할 이미지를 선택하세요.", "",
                                                  "All Files (*)")

        if fileName:
            img = cv2.imread(fileName)
            try:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except:
                QMessageBox.critical(self, 'Message', '이미지 파일만 선택해 주세요.',
                                     QMessageBox.Yes)
                return

    def textGroup(self):

        self.dialog = QDialog()
        self.dialog.setWindowTitle('결과')
        self.dialog.setWindowModality(Qt.ApplicationModal)

        try:
            h, w = img.shape
        except:
            QMessageBox.critical(self, 'Message', '이미지 파일을 선택해 주세요.',
                                 QMessageBox.Yes)
            return

        if nw == '':
            nh = int(h / w * 50)
            reImg = cv2.resize(img, (50 * 2, nh))
            self.dialog.resize(550, (nh * 10 + 150))
        else:
            try:
                nh = int(h / w * int(nw))
                reImg = cv2.resize(img, (int(nw) * 2, nh))
                self.dialog.resize((int(nw) * 10 + 50), (nh * 10 + 150))
            except:
                QMessageBox.critical(self, 'Message', '숫자만 입력해 주세요.',
                                     QMessageBox.Yes)
                w_num.setText('')
                return

        textBox = QTextEdit('')
        fontVar = QFont("Cascadia Code", 7)
        textBox.setCurrentFont(fontVar)
        box = QVBoxLayout()
        box.addWidget(textBox)

        result = ''

        CHARS = ' .,-~:;=!*#$@'

        for row in reImg:
            text = ''
            for pixel in row:
                index = int(pixel / 256 * len(CHARS))
                text += CHARS[index]

            result += text + '\n'
        print(result)
        textBox.append(result)

        self.dialog.setLayout(box)
        self.dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())