import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("❌ Tic Tac Toe ⭕")
        self.setFixedSize(740, 740)
        icon = QIcon('assets/icon.ico')
        self.setWindowIcon(icon)

        pixmap = QPixmap("assets/tictactoe.png")
        pixmap = pixmap.scaled(740, 740, Qt.KeepAspectRatioByExpanding)

        self.background = QLabel(self)
        self.background.setPixmap(pixmap)
        self.background.setAlignment(Qt.AlignCenter)

        self.turn = "X"

        self.xmap = QPixmap("assets/X.png")
        self.xmap = self.xmap.scaled(142, 142, Qt.KeepAspectRatioByExpanding)

        self.omap = QPixmap("assets/O.png")
        self.omap = self.omap.scaled(162, 162, Qt.KeepAspectRatioByExpanding)

        self.createElements()

        for i in range(3):
            for j in range(3):
                self.button = QPushButton("", self)
                self.button.setGeometry((90 + i * 200), (90 + j * 200), 162, 162)
                self.button.setStyleSheet("border: none;")
                self.button.clicked.connect(lambda _, i=i, j=j: self.setPlay(i, j))


    def setPlay(self, i, j):
        if self.turn == "X":
            if j == 0 and i == 0: self.x00.show()
            elif j == 0 and i == 1: self.x01.show()
            elif j == 0 and i == 2: self.x02.show()
            elif j == 1 and i == 0: self.x10.show()
            elif j == 1 and i == 1: self.x11.show()
            elif j == 1 and i == 2: self.x12.show()
            elif j == 2 and i == 0: self.x20.show()
            elif j == 2 and i == 1: self.x21.show()
            elif j == 2 and i == 2: self.x22.show()
            self.turn = "O"
        else:
            if j == 0 and i == 0: self.o00.show()
            elif j == 0 and i == 1: self.o01.show()
            elif j == 0 and i == 2: self.o02.show()
            elif j == 1 and i == 0: self.o10.show()
            elif j == 1 and i == 1: self.o11.show()
            elif j == 1 and i == 2: self.o12.show()
            elif j == 2 and i == 0: self.o20.show()
            elif j == 2 and i == 1: self.o21.show()
            elif j == 2 and i == 2: self.o22.show()
            self.turn = "X"

    def createElements(self):
        self.x00 = QLabel(self)
        self.x00.setPixmap(self.xmap)
        self.x00.setAlignment(Qt.AlignCenter)
        self.x00.setGeometry(47 * 2, 55 * 2, 142, 142)
        self.x00.hide()

        self.x01 = QLabel(self)
        self.x01.setPixmap(self.xmap)
        self.x01.setAlignment(Qt.AlignCenter)
        self.x01.setGeometry(147 * 2, 55 * 2, 142, 142)
        self.x01.hide()

        self.x02 = QLabel(self)
        self.x02.setPixmap(self.xmap)
        self.x02.setAlignment(Qt.AlignCenter)
        self.x02.setGeometry(247 * 2, 55 * 2, 142, 142)
        self.x02.hide()

        self.x10 = QLabel(self)
        self.x10.setPixmap(self.xmap)
        self.x10.setAlignment(Qt.AlignCenter)
        self.x10.setGeometry(47 * 2, 155 * 2, 142, 142)
        self.x10.hide()

        self.x11 = QLabel(self)
        self.x11.setPixmap(self.xmap)
        self.x11.setAlignment(Qt.AlignCenter)
        self.x11.setGeometry(147 * 2, 150 * 2, 142, 142)
        self.x11.hide()

        self.x12 = QLabel(self)
        self.x12.setPixmap(self.xmap)
        self.x12.setAlignment(Qt.AlignCenter)
        self.x12.setGeometry(247 * 2, 150 * 2, 142, 142)
        self.x12.hide()

        self.x20 = QLabel(self)
        self.x20.setPixmap(self.xmap)
        self.x20.setAlignment(Qt.AlignCenter)
        self.x20.setGeometry(47 * 2, 250 * 2, 142, 142)
        self.x20.hide()

        self.x21 = QLabel(self)
        self.x21.setPixmap(self.xmap)
        self.x21.setAlignment(Qt.AlignCenter)
        self.x21.setGeometry(147 * 2, 250 * 2, 142, 142)
        self.x21.hide()

        self.x22 = QLabel(self)
        self.x22.setPixmap(self.xmap)
        self.x22.setAlignment(Qt.AlignCenter)
        self.x22.setGeometry(247 * 2, 250 * 2, 142, 142)
        self.x22.hide()

        self.o00 = QLabel(self)
        self.o00.setPixmap(self.omap)
        self.o00.setAlignment(Qt.AlignCenter)
        self.o00.setGeometry(45 * 2, 45 * 2, 162, 162)
        self.o00.hide()

        self.o01 = QLabel(self)
        self.o01.setPixmap(self.omap)
        self.o01.setAlignment(Qt.AlignCenter)
        self.o01.setGeometry(145 * 2, 45 * 2, 162, 162)
        self.o01.hide()

        self.o02 = QLabel(self)
        self.o02.setPixmap(self.omap)
        self.o02.setAlignment(Qt.AlignCenter)
        self.o02.setGeometry(245 * 2, 45 * 2, 162, 162)
        self.o02.hide()

        self.o10 = QLabel(self)
        self.o10.setPixmap(self.omap)
        self.o10.setAlignment(Qt.AlignCenter)
        self.o10.setGeometry(45 * 2, 145 * 2, 162, 162)
        self.o10.hide()

        self.o11 = QLabel(self)
        self.o11.setPixmap(self.omap)
        self.o11.setAlignment(Qt.AlignCenter)
        self.o11.setGeometry(145 * 2, 145 * 2, 162, 162)
        self.o11.hide()

        self.o12 = QLabel(self)
        self.o12.setPixmap(self.omap)
        self.o12.setAlignment(Qt.AlignCenter)
        self.o12.setGeometry(245 * 2, 145 * 2, 162, 162)
        self.o12.hide()

        self.o20 = QLabel(self)
        self.o20.setPixmap(self.omap)
        self.o20.setAlignment(Qt.AlignCenter)
        self.o20.setGeometry(45 * 2, 245 * 2, 162, 162)
        self.o20.hide()

        self.o21 = QLabel(self)
        self.o21.setPixmap(self.omap)
        self.o21.setAlignment(Qt.AlignCenter)
        self.o21.setGeometry(145 * 2, 245 * 2, 162, 162)
        self.o21.hide()

        self.o22 = QLabel(self)
        self.o22.setPixmap(self.omap)
        self.o22.setAlignment(Qt.AlignCenter)
        self.o22.setGeometry(245 * 2, 245 * 2, 162, 162)
        self.o22.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
