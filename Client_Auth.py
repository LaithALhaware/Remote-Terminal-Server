import socket
import threading
import time
import sys

# ANSI escape codes for colors
GREEN_BOLD = "\033[1;32m"
BLUE_BOLD = "\033[1;34m"
RESET = "\033[0m"

# Get server IP and port from user
HOST = input("Enter server IP: ").strip()
PORT = int(input("Enter server PORT: ").strip())

# Spinner animation
loading = True
def spinner():
    while loading:
        for char in "|/-\\":
            sys.stdout.write(f"\rConnecting... {char}")
            sys.stdout.flush()
            time.sleep(0.1)

spinner_thread = threading.Thread(target=spinner)
spinner_thread.start()

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    loading = False
    spinner_thread.join()
    print("\rConnected successfully!  \nTo disconnect and close Add a command 'exit', 'quit', 'disconnect' ")
except Exception as e:
    loading = False
    spinner_thread.join()
    print(f"\rConnection failed: {e}")
    exit()

def send_msg(sock, msg):
    sock.sendall(msg.encode() + b"<END>")

def recv_msg(sock):
    data = b""
    while not data.endswith(b"<END>"):
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data[:-5].decode()

# Authentication
print(client.recv(1024).decode(), end='')
username = input()
send_msg(client, username)

print(client.recv(1024).decode(), end='')
password = input()
send_msg(client, password)

response = recv_msg(client)
if "failed" in response.lower():
    print(response)
    client.close()
    exit()

if "[DIR]" in response:
    print(response.split("[DIR]")[0].strip())
    current_dir = response.split("[DIR]")[-1].strip()
else:
    print(response.strip())
    current_dir = "~"

# Main loop
while True:
    prompt = f"{GREEN_BOLD}{HOST}{RESET}:{BLUE_BOLD}{current_dir}{RESET}$ "
    cmd = input(prompt).strip()

    # Disconnect command
    if cmd.lower() in ["exit", "quit", "disconnect", "!disconnect now"]:
        send_msg(client, "exit")
        print("Disconnected from server.")
        client.close()
        break

    # Download
    elif cmd.lower().startswith("download "):
        client.sendall(cmd.encode() + b"<END>")
        filename = cmd.split(" ", 1)[1]
        with open("downloaded_" + filename, 'wb') as f:
            while True:
                chunk = client.recv(1024)
                if b"<FILEEND>" in chunk:
                    chunk = chunk.replace(b"<FILEEND>", b"")
                    f.write(chunk)
                    break
                f.write(chunk)
        print("Download complete.")

    # Upload
    elif cmd.lower().startswith("upload "):
        filename = cmd.split(" ", 1)[1]
        try:
            client.sendall(cmd.encode() + b"<END>")
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    client.sendall(chunk)
                client.sendall(b"<FILEEND>")
            response = recv_msg(client)
            print(response.split("[DIR]")[0].strip())
            current_dir = response.split("[DIR]")[-1].strip()
        except Exception as e:
            print(f"Upload failed: {e}")

    # Regular commands
    else:
        send_msg(client, cmd)
        response = recv_msg(client)
        if "[DIR]" in response:
            output, current_dir = response.rsplit("[DIR]", 1)
            print(output.strip())
            current_dir = current_dir.strip()
        else:
            print(response.strip())
