import socket
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))

server.listen(2)
print('Waiting for a connection...')

players = []

def threaded_client(connection, addr):
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                connection.send(str.encode('Server is shutting down'))
                break
            reply = f'{addr[0]}:{addr[1]} - {data.decode()}'
            print(reply)
            connection.sendall(str.encode(reply))
        except:
            break

    print(f'Connection to {addr} closed')
    players.remove(connection)
    connection.close()


while True:
    conn, addr = server.accept()
    players.append(conn)
    if len(players) == 1:
        print('Player 1 connected')
        conn.send(str.encode('Player 1'))
        start_new_thread(threaded_client, (conn, addr))
    elif len(players) == 2:
        print('Player 2 connected')
        conn.send(str.encode('Player 2'))
        for player in players:
            player.send(str.encode('Starting game...'))
        start_new_thread(threaded_client, (conn, addr))
    else:
        print('Server is full')
        conn.sendall(str.encode('Server is full'))
        conn.close()
