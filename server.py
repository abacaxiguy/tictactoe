import socket
from _thread import *
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))

server.listen(2)
print('Waiting for a connection...')

players = []
moveTypePlayer1 = ''

def threaded_client(connection, addr):
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                connection.sendall(str.encode('Server is shutting down'))
                break
            reply = f'{data.decode()}'
            for player in players:
                player.sendall(str.encode(reply))
        except:
            break

    print(f'Connection to {addr} closed')
    players.remove(connection)
    for player in players:
        player.sendall(str.encode('Player left'))
    connection.close()


while True:
    conn, addr = server.accept()
    players.append(conn)

    if len(players) == 1:
        print('Player 1 connected')
        conn.sendall(str.encode('P1'))
        moveType = random.choice(['X', 'O'])
        print(f'Player 1 is {moveType}')
        conn.sendall(str.encode(moveType))
        moveTypePlayer1 = moveType
        start_new_thread(threaded_client, (conn, addr))
    elif len(players) == 2:
        print('Player 2 connected')
        conn.sendall(str.encode('P2'))
        print(f'Player 2 is {"X" if moveTypePlayer1 == "O" else "O"}')
        conn.sendall(str.encode('X') if moveTypePlayer1 == 'O' else str.encode('O'))
        print('Starting game...')
        for player in players:
            player.sendall(str.encode('Starting game...'))
        start_new_thread(threaded_client, (conn, addr))
    else:
        print('Server is full')
        conn.sendall(str.encode('Server is full'))
        conn.close()
