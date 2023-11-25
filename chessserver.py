import socket
import threading

class ChessGame:
    # ... (existing ChessGame class remains unchanged)

class ChessServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.players = {}
        self.games = []

    def handle_client(self, client, player_id):
        client.send(f"Welcome, Player {player_id}!\n".encode())
        while True:
            try:
                data = client.recv(1024).decode()
                if data.startswith("LIST"):
                    player_list = "\n".join([f"Player {pid}" for pid in self.players if pid != player_id])
                    client.send(player_list.encode())
                elif data.startswith("PLAY"):
                    opponent_id = int(data.split()[1])
                    if opponent_id in self.players and opponent_id != player_id:
                        game_players = [client, self.players[opponent_id]]
                        new_game = ChessGame(*game_players)
                        self.games.append(new_game)
                        client.send("Game started!\n".encode())
                        self.players[opponent_id].send("Game started!\n".encode())
                        break
                    else:
                        client.send("Invalid opponent selection!\n".encode())
                elif data == "QUIT":
                    break
            except:
                break

        print(f"Player {player_id} has left the game.")
        del self.players[player_id]
        client.close()

    def run(self):
        print("Server is running...")
        player_id = 1
        while True:
            client, address = self.server.accept()
            print(f"Connected to {address}")

            self.players[player_id] = client
            threading.Thread(target=self.handle_client, args=(client, player_id)).start()
            player_id += 1

if __name__ == "__main__":
    chess_server = ChessServer()
    chess_server.run()
