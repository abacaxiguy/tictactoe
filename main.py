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
        self.playbutton.setEnabled(False)

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

        for i in range(3):
            for j in range(3):
                self.button = QPushButton("", self)
                self.button.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: none")
                self.button.setGeometry((81 + i * 189), (82 + j * 190), 186, 186)
                self.button.clicked.connect(lambda _, i=i, j=j: self.setPlay(i, j))
                self.button.show()

    def setPlay(self, i, j):
        for button in self.findChildren(QPushButton):
            button.hide()
            QTimer.singleShot(1000, button.show)

        self.element = QLabel(self)
        self.element.setPixmap(self.xmap if self.turnX else self.omap)
        self.element.setAlignment(Qt.AlignCenter)
        self.element.setGeometry((104 + i * 189), (110 + j * 190), 142, 142) if self.turnX else self.element.setGeometry((94 + i * 188), (96 + j * 189), 162, 162)

        self.fadeIn(self.element)
        self.element.show()

        self.turnX = not self.turnX

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
