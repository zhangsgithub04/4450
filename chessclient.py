import socket

def main():
    host = '127.0.0.1'
    port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    player_id = client.recv(1024).decode()
    print(player_id)

    while True:
        choice = input("Enter 'LIST' to see available players, 'PLAY <opponent_id>' to start a game, or 'QUIT' to exit: ")
        client.send(choice.encode())

        if choice.upper() == "LIST":
            player_list = client.recv(1024).decode()
            print("Available players:")
            print(player_list)
        elif choice.upper().startswith("PLAY"):
            response = client.recv(1024).decode()
            print(response)
            if response == "Game started!\n":
                # Start game logic here
                pass
        elif choice.upper() == "QUIT":
            break

    client.close()

if __name__ == "__main__":
    main()
