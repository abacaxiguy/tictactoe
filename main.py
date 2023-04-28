import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(740, 740)
        icon = QIcon('assets/icon.ico')
        self.setWindowIcon(icon)

        playbackground = QPixmap("assets/playscreen.png")
        playbackground = playbackground.scaled(740, 740, Qt.KeepAspectRatioByExpanding)

        self.playscreen = QLabel(self)
        self.playscreen.setPixmap(playbackground)
        self.playscreen.setAlignment(Qt.AlignCenter)

        self.playbutton = QPushButton("", self)
        self.playbutton.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: none")
        self.playbutton.setGeometry(287, 401, 166, 76)
        self.playbutton.clicked.connect(self.waitPlayer)

        background = QPixmap("assets/tictactoe.png")

        self.background = QLabel(self)
        self.background.setPixmap(background)
        self.background.setAlignment(Qt.AlignCenter)
        self.background.setGeometry(0, 0, 740, 740)

        self.background.hide()

        self.waiting = QMovie("assets/waiting.gif")

        self.waitingbg = QLabel(self)
        self.waitingbg.setMovie(self.waiting)
        self.waitingbg.setGeometry(0, 0, 740, 740)
        self.waitingbg.setAlignment(Qt.AlignCenter)
        self.waitingbg.hide()

    def waitPlayer(self):
        self.fadeOut(self.playbutton)
        self.fadeOut(self.playscreen)

        self.fadeIn(self.waitingbg)
        self.waitingbg.show()
        self.waiting.start()
        
        QTimer.singleShot(5000, self.startGame)

    def startGame(self):
        self.playscreen.hide()
        self.waitingbg.hide()
        self.waiting.stop()

        # self.fadeIn(self.background)
        self.background.show()

        self.turnX = True # True = X, False = O

        self.xmap = QPixmap("assets/X.png")
        self.xmap = self.xmap.scaled(142, 142, Qt.KeepAspectRatioByExpanding)

        self.omap = QPixmap("assets/O.png")
        self.omap = self.omap.scaled(162, 162, Qt.KeepAspectRatioByExpanding)

        self.createElements()

        for i in range(3):
            for j in range(3):
                self.button = QPushButton("", self)
                self.button.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: none")
                self.button.setGeometry((89 + i * 189), (89 + j * 189), 186, 186)
                self.button.clicked.connect(lambda _, i=i, j=j: self.setPlay(i, j))
                self.button.show()

    def setPlay(self, i, j):
        for button in self.findChildren(QPushButton):
            button.hide()
            QTimer.singleShot(1000, button.show)

        self.showX(i, j) if self.turnX else self.showO(i, j)
        self.turnX = not self.turnX

    def createElements(self):
        self.x00 = QLabel(self)
        self.x00.setPixmap(self.xmap)
        self.x00.setAlignment(Qt.AlignCenter)
        self.x00.setGeometry(110, 110, 142, 142)
        self.x00.hide()

        self.x01 = QLabel(self)
        self.x01.setPixmap(self.xmap)
        self.x01.setAlignment(Qt.AlignCenter)
        self.x01.setGeometry(300, 110, 142, 142)
        self.x01.hide()

        self.x02 = QLabel(self)
        self.x02.setPixmap(self.xmap)
        self.x02.setAlignment(Qt.AlignCenter)
        self.x02.setGeometry(490, 110, 142, 142)
        self.x02.hide()

        self.x10 = QLabel(self)
        self.x10.setPixmap(self.xmap)
        self.x10.setAlignment(Qt.AlignCenter)
        self.x10.setGeometry(110, 305, 142, 142)
        self.x10.hide()

        self.x11 = QLabel(self)
        self.x11.setPixmap(self.xmap)
        self.x11.setAlignment(Qt.AlignCenter)
        self.x11.setGeometry(300, 305, 142, 142)
        self.x11.hide()

        self.x12 = QLabel(self)
        self.x12.setPixmap(self.xmap)
        self.x12.setAlignment(Qt.AlignCenter)
        self.x12.setGeometry(490, 305, 142, 142)
        self.x12.hide()

        self.x20 = QLabel(self)
        self.x20.setPixmap(self.xmap)
        self.x20.setAlignment(Qt.AlignCenter)
        self.x20.setGeometry(110, 495, 142, 142)
        self.x20.hide()

        self.x21 = QLabel(self)
        self.x21.setPixmap(self.xmap)
        self.x21.setAlignment(Qt.AlignCenter)
        self.x21.setGeometry(300, 495, 142, 142)
        self.x21.hide()

        self.x22 = QLabel(self)
        self.x22.setPixmap(self.xmap)
        self.x22.setAlignment(Qt.AlignCenter)
        self.x22.setGeometry(490, 495, 142, 142)
        self.x22.hide()

        self.o00 = QLabel(self)
        self.o00.setPixmap(self.omap)
        self.o00.setAlignment(Qt.AlignCenter)
        self.o00.setGeometry(100, 96, 162, 162)
        self.o00.hide()

        self.o01 = QLabel(self)
        self.o01.setPixmap(self.omap)
        self.o01.setAlignment(Qt.AlignCenter)
        self.o01.setGeometry(290, 96, 162, 162)
        self.o01.hide()

        self.o02 = QLabel(self)
        self.o02.setPixmap(self.omap)
        self.o02.setAlignment(Qt.AlignCenter)
        self.o02.setGeometry(480, 96, 162, 162)
        self.o02.hide()

        self.o10 = QLabel(self)
        self.o10.setPixmap(self.omap)
        self.o10.setAlignment(Qt.AlignCenter)
        self.o10.setGeometry(100, 292, 162, 162)
        self.o10.hide()

        self.o11 = QLabel(self)
        self.o11.setPixmap(self.omap)
        self.o11.setAlignment(Qt.AlignCenter)
        self.o11.setGeometry(290, 292, 162, 162)
        self.o11.hide()

        self.o12 = QLabel(self)
        self.o12.setPixmap(self.omap)
        self.o12.setAlignment(Qt.AlignCenter)
        self.o12.setGeometry(480, 292, 162, 162)
        self.o12.hide()

        self.o20 = QLabel(self)
        self.o20.setPixmap(self.omap)
        self.o20.setAlignment(Qt.AlignCenter)
        self.o20.setGeometry(100, 480, 162, 162)
        self.o20.hide()

        self.o21 = QLabel(self)
        self.o21.setPixmap(self.omap)
        self.o21.setAlignment(Qt.AlignCenter)
        self.o21.setGeometry(290, 480, 162, 162)
        self.o21.hide()

        self.o22 = QLabel(self)
        self.o22.setPixmap(self.omap)
        self.o22.setAlignment(Qt.AlignCenter)
        self.o22.setGeometry(480, 480, 162, 162)
        self.o22.hide()

    def showX(self, i, j):
        if j == 0 and i == 0: self.fadeIn(self.x00); self.x00.show()
        elif j == 0 and i == 1: self.fadeIn(self.x01); self.x01.show()
        elif j == 0 and i == 2: self.fadeIn(self.x02); self.x02.show()
        elif j == 1 and i == 0: self.fadeIn(self.x10); self.x10.show()
        elif j == 1 and i == 1: self.fadeIn(self.x11); self.x11.show()
        elif j == 1 and i == 2: self.fadeIn(self.x12); self.x12.show()
        elif j == 2 and i == 0: self.fadeIn(self.x20); self.x20.show()
        elif j == 2 and i == 1: self.fadeIn(self.x21); self.x21.show()
        elif j == 2 and i == 2: self.fadeIn(self.x22); self.x22.show()

    def showO(self, i, j):
        if j == 0 and i == 0: self.fadeIn(self.o00); self.o00.show()
        elif j == 0 and i == 1: self.fadeIn(self.o01); self.o01.show()
        elif j == 0 and i == 2: self.fadeIn(self.o02); self.o02.show()
        elif j == 1 and i == 0: self.fadeIn(self.o10); self.o10.show()
        elif j == 1 and i == 1: self.fadeIn(self.o11); self.o11.show()
        elif j == 1 and i == 2: self.fadeIn(self.o12); self.o12.show()
        elif j == 2 and i == 0: self.fadeIn(self.o20); self.o20.show()
        elif j == 2 and i == 1: self.fadeIn(self.o21); self.o21.show()
        elif j == 2 and i == 2: self.fadeIn(self.o22); self.o22.show()

    def fadeIn(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.easingCurve = QEasingCurve.OutCubic
        self.animation.setDuration(700)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def fadeOut(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.easingCurve = QEasingCurve.InCubic
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

        self.animation.finished.connect(lambda: widget.hide())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
