import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGraphicsOpacityEffect, QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QParallelAnimationGroup, QThread, pyqtSignal
import socket


class SecondPlayerWorker(QThread):
    found_second_player = pyqtSignal()

    def __init__(self, client=None):
        super().__init__()
        self.client = client

    def run(self):
        print('Waiting for second player...')
        self.keep_running = True
        while self.keep_running:
            res = self.client.recv(1024).decode()
            print(res)
            if res == 'Starting game...':
                self.found_second_player.emit()
                self.keep_running = False
            elif res == 'Server is full':
                print(res)
                self.client.close()
                sys.exit()


class GameWorker(QThread):
    player_moved = pyqtSignal(int, int, str)
    turn = pyqtSignal(bool)

    def __init__(self, client=None, moveType=None, yourTurn=None):
        super().__init__()
        self.client = client
        self.xMoves = []
        self.oMoves = []
        self.moveType = moveType
        self.yourTurn = yourTurn

    def run(self):
        self.keep_running = True
        while self.keep_running:
            res = self.client.recv(1024).decode()

            if res == 'Player left':
                print(res)
                self.client.close()
                sys.exit()

            i = int(res[0])
            j = int(res[1])
            move_type = res[2]
            if move_type == 'X':
                self.xMoves.append((i, j))
            elif move_type == 'O':
                self.oMoves.append((i, j))

            self.yourTurn = not self.yourTurn
            self.turn.emit(self.yourTurn)
            self.player_moved.emit(i, j, move_type)


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(740, 740)
        icon = QIcon('assets/icons/icon.ico')
        self.setWindowIcon(icon)

        playbackground = QPixmap("assets/pages/playscreen.png")
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

        self.waiting = QMovie("assets/pages/waiting.gif")

        self.waitingbg = QLabel(self)
        self.waitingbg.setMovie(self.waiting)
        self.waitingbg.setGeometry(0, 0, 740, 740)
        self.waitingbg.setAlignment(Qt.AlignCenter)

        self.fadeIn(self.waitingbg)
        self.waitingbg.show()
        self.waiting.start()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect(('localhost', 5000))
            response = self.client.recv(1024).decode()

            if response == 'Server is full':
                print(response)
                sys.exit()

            self.player, self.moveType = response.split(';')
            print(f'You are player {self.player}')
            print(f'Your move type is {self.moveType}')
        except Exception as e:
            if e == KeyboardInterrupt:
                print('Shutting down...')
            else:
                print('Server is offline')
            sys.exit()

        self.worker = SecondPlayerWorker(client=self.client)
        self.worker.found_second_player.connect(self.startGame)
        self.worker.found_second_player.connect(self.worker.deleteLater)
        self.worker.start()

    def startGame(self):
        self.playscreen.hide()
        self.fadeOut(self.waitingbg)
        self.waiting.stop()

        background = QPixmap("assets/pages/tictactoe.png")

        self.background = QLabel(self)
        self.background.setPixmap(background)
        self.background.setAlignment(Qt.AlignCenter)
        self.background.setGeometry(0, 0, 740, 740)
        self.fadeIn(self.background)
        self.background.show()

        self.yourTurn = True if self.player == 'P1' else False

        self.xmap = QPixmap("assets/icons/X.png")
        self.xmap = self.xmap.scaled(142, 142, Qt.KeepAspectRatioByExpanding)

        self.omap = QPixmap("assets/icons/O.png")
        self.omap = self.omap.scaled(162, 162, Qt.KeepAspectRatioByExpanding)

        for i in range(3):
            for j in range(3):
                self.button = QPushButton("", self)
                self.button.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: none; QPushButton::disabled { color: #6A00B3; }")
                self.button.setGeometry((81 + i * 190), (82 + j * 190), 186, 186)
                self.button.clicked.connect(lambda _, i=i, j=j: self.setPlay(i, j, self.moveType))
                self.button.setObjectName("E" + str(i) + str(j))
                self.button.show()

        self.game_worker = GameWorker(client=self.client, moveType=self.moveType, yourTurn=self.yourTurn)
        self.game_worker.player_moved.connect(lambda i, j, move_type: self.setPlay(i, j, move_type))
        self.game_worker.turn.connect(self.setTurn)
        self.game_worker.start()

        self.winMoves =[
            ["00","11","22"], # diagonal 1
            ["20","11","02"], # diagonal 2
            ["00", "01", "02"], # horizontal 0
            ["10", "11", "12"], # horizontal 1 
            ["20", "21", "22"], # horizontal 2    
            ["00", "10", "20"], # vertical 0
            ["01", "11", "21"], # vertical 1
            ["02", "12", "22"] # vertical 2
        ]

        if not self.game_worker.yourTurn:
            self.disableAllButtons()

    def setTurn(self):
        if not self.game_worker.yourTurn:
            self.disableAllButtons()
        else:
            self.enableNotPlayedButtons()

    def setPlay(self, i, j, moveType):
        self.currentBtn = self.findChild(QPushButton, "E" + str(i) + str(j))
        if not self.currentBtn:
            return

        if moveType == self.moveType:
            self.client.send(str(i).encode() + str(j).encode() + moveType.encode()) 

        self.fadeIn(self.currentBtn)

        # save moves-----------------------

        if moveType == "X":
            self.game_worker.xMoves.append(str(i)+str(j))
        else:
            self.game_worker.oMoves.append(str(i)+str(j))

        self.currentBtn.setIcon(QIcon(self.xmap if moveType == 'X' else self.omap))
        self.currentBtn.setIconSize(self.xmap.rect().size() if moveType == 'X' else self.omap.rect().size())

        self.disableButton(self.currentBtn)

        QTimer.singleShot(1000, self.checkGameStatus)

    def checkGameStatus(self):
        for move in self.winMoves: 
            if all(item in self.game_worker.oMoves for item in move):
                    self.endGame("O")
                    return
            elif all(item in self.game_worker.xMoves for item in move):
                    self.endGame("X")
                    return

        if len(self.game_worker.oMoves) + len(self.game_worker.xMoves) == 9:
            self.endGame("draw")

    def endGame(self, winner):
        self.disableAllButtons()

        self.winner = QLabel(self)
        self.winner.setAlignment(Qt.AlignCenter)
        self.winner.setGeometry(0, 0, 740, 740)

        if winner == "X":
            if self.moveType == "X":
                self.winner.setPixmap(QPixmap(f'assets/res/xwins{self.player}.png'))
            else:
                self.winner.setPixmap(QPixmap(f'assets/res/xwins{"P1" if self.player == "P2" else self.player}.png'))
        elif winner == "O":
            if self.moveType == "O":
                self.winner.setPixmap(QPixmap(f'assets/res/owins{self.player}.png'))
            else:
                self.winner.setPixmap(QPixmap(f'assets/res/owins{"P1" if self.player == "P2" else self.player}.png'))
        elif winner == "draw":
            self.winner.setPixmap(QPixmap("assets/res/draw.png"))

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
        self.animation.setDuration(duration)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

        self.animation.finished.connect(lambda: widget.hide())

    def disableButton(self, btn):
        btn.setObjectName("D" + btn.objectName()[1:])

    def disableAllButtons(self):
        for button in self.findChildren(QPushButton):
            button.setObjectName("D" + button.objectName()[1:])

    def enableNotPlayedButtons(self):
        for button in self.findChildren(QPushButton):
            if "D" in button.objectName():
                ij = button.objectName()[1:]
                if ij in self.game_worker.xMoves or ij in self.game_worker.oMoves:
                    continue
                button.setObjectName("E" + button.objectName()[1:])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())


