import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGraphicsOpacityEffect, QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QParallelAnimationGroup

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

    def waitPlayer(self):
        self.fadeOut(self.playscreen)
        self.playbutton.setEnabled(False)

        self.waiting = QMovie("assets/waiting.gif")

        self.waitingbg = QLabel(self)
        self.waitingbg.setMovie(self.waiting)
        self.waitingbg.setGeometry(0, 0, 740, 740)
        self.waitingbg.setAlignment(Qt.AlignCenter)

        self.fadeIn(self.waitingbg)
        self.waitingbg.show()
        self.waiting.start()

        # fake waiting
        QTimer.singleShot(0, self.startGame)

    def startGame(self):
        self.playscreen.hide()
        self.fadeOut(self.waitingbg)
        self.waiting.stop()

        background = QPixmap("assets/tictactoe.png")

        self.background = QLabel(self)
        self.background.setPixmap(background)
        self.background.setAlignment(Qt.AlignCenter)
        self.background.setGeometry(0, 0, 740, 740)
        self.fadeIn(self.background)
        self.background.show()

        self.turnX = True # True = X, False = O

        self.xmap = QPixmap("assets/X.png")
        self.xmap = self.xmap.scaled(142, 142, Qt.KeepAspectRatioByExpanding)

        self.omap = QPixmap("assets/O.png")
        self.omap = self.omap.scaled(162, 162, Qt.KeepAspectRatioByExpanding)

        for i in range(3):
            for j in range(3):
                self.button = QPushButton("", self)
                self.button.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: none; QPushButton::disabled { color: #6A00B3; }")
                self.button.setGeometry((81 + i * 190), (82 + j * 190), 186, 186)
                self.button.clicked.connect(lambda _, i=i, j=j: self.setPlay(i, j))
                self.button.setObjectName("E" + str(i) + str(j))
                self.button.show()
        
        self.xMoves = []
        self.oMoves = []
        self.winMoves =[
            ["00","11","22"], # diagonal 1
            ["20","11","02"], # diagonal 2
            ["00", "01", "02"], # horizontal 0
            ["10", "11", "12"], # horizontal 1 
            ["20", "21", "22"], # horizontal 2    
            ["00", "10", "20"], # vertical 0
            ["01", "11", 21], # vertical 1
            ["02", "12", "22"] # vertical 2
        ]

    def setPlay(self, i, j):
        self.currentBtn = self.findChild(QPushButton, "E" + str(i) + str(j))
        if not self.currentBtn: return

        self.fadeIn(self.currentBtn)

        # save moves-----------------------
        if self.turnX:
            self.xMoves.append(str(i)+str(j))

        else:
            self.oMoves.append(str(i)+str(j))

        self.currentBtn.setIcon(QIcon(self.xmap if self.turnX else self.omap))
        self.currentBtn.setIconSize(self.xmap.rect().size() if self.turnX else self.omap.rect().size())

        self.disableButton(self.currentBtn)

        for button in self.findChildren(QPushButton):
            if "E" in button.objectName():
                button.hide()
                QTimer.singleShot(1000, button.show)

        QTimer.singleShot(1000, self.checkGameStatus)

        self.turnX = not self.turnX

    def checkGameStatus(self):
        for move in self.winMoves: 
            if all(item in self.oMoves for item in move):
                    self.endGame("o")
                    return
            elif all(item in self.xMoves for item in move):
                    self.endGame("x")
                    return

        if len(self.oMoves) + len(self.xMoves) == 9:
            self.endGame("draw")

    def endGame(self, winner):
        self.disableAllButtons()

        self.winner = QLabel(self)
        self.winner.setAlignment(Qt.AlignCenter)
        self.winner.setGeometry(0, 0, 740, 740)

        if winner == "x":
            self.winner.setPixmap(QPixmap("assets/xwins.png"))
        elif winner == "o":
            self.winner.setPixmap(QPixmap("assets/owins.png"))
        elif winner == "draw":
            self.winner.setPixmap(QPixmap("assets/draw.png"))

        self.fadeIn(self.winner, 1500)
        self.winner.show()

        self.blurAllBackground()

    def blurAllBackground(self):
        group = QParallelAnimationGroup(self)

        self.effect = QGraphicsBlurEffect()
        self.background.setGraphicsEffect(self.effect)

        bganimation = QPropertyAnimation(self.effect, b"blurRadius")
        bganimation.setDuration(1500)
        bganimation.setStartValue(0)
        bganimation.setEndValue(5)
        group.addAnimation(bganimation)

        
        for button in self.findChildren(QPushButton):
            if "D" in button.objectName():
                self.effect = QGraphicsBlurEffect()
                button.setGraphicsEffect(self.effect)

                animation = QPropertyAnimation(self.effect, b"blurRadius")
                animation.setDuration(1500)
                animation.setStartValue(0)
                animation.setEndValue(5)
                group.addAnimation(animation)

        group.start()

    def fadeIn(self, widget, duration=700):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.easingCurve = QEasingCurve.OutCubic
        self.animation.setDuration(duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def fadeOut(self, widget, duration=1000):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.easingCurve = QEasingCurve.InCubic
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

        self.animation.finished.connect(lambda: widget.hide())

    def disableButton(self, btn):
        btn.setObjectName("D" + btn.objectName()[1:])

    def disableAllButtons(self):
        for button in self.findChildren(QPushButton):
            button.setObjectName("D" + button.objectName()[1:])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())


