import socket
import os
import subprocess
import datetime
import time

LOG_FILE = "server_log.txt"

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def send_msg(conn, msg):
    conn.sendall(msg.encode() + b"<END>")

def recv_msg(conn):
    data = b""
    while not data.endswith(b"<END>"):
        data += conn.recv(1024)
    return data[:-5].decode()

def handle_client(conn, addr, USERNAME, PASSWORD):
    log_event(f"Connection from {addr[0]}:{addr[1]}")
    
    conn.send(b"Username: ")
    username = recv_msg(conn)
    conn.send(b"Password: ")
    password = recv_msg(conn)

    if username != USERNAME or password != PASSWORD:
        send_msg(conn, "Authentication failed.")
        log_event(f"Authentication failed for {username} from {addr[0]}")
        conn.close()
        return

    send_msg(conn, f"Authenticated.\n[DIR]{os.getcwd()}")
    log_event(f"User {username} authenticated from {addr[0]}")

    while True:
        command = recv_msg(conn).strip()

        if command.lower() in ['exit', 'quit']:
            log_event(f"User {username} disconnected.")
            break

        elif command.startswith("cd "):
            try:
                os.chdir(command[3:])
                send_msg(conn, f"[DIR]{os.getcwd()}")
                log_event(f"User {username} changed directory to {os.getcwd()}")
            except Exception as e:
                send_msg(conn, f"Error: {e}\n[DIR]{os.getcwd()}")
                log_event(f"Error changing directory: {e}")

        elif command.startswith("download "):
            path = command[9:].strip()
            if os.path.isfile(path):
                try:
                    with open(path, 'rb') as f:
                        conn.sendall(f.read() + b"<FILEEND>")
                    log_event(f"File sent: {path}")
                except Exception as e:
                    conn.send(f"Error reading file: {e}".encode() + b"<FILEEND>")
                    log_event(f"Error reading file {path}: {e}")
            else:
                conn.send(b"File not found<FILEEND>")
                log_event(f"File not found: {path}")

        elif command.startswith("upload "):
            path = command[7:].strip()
            try:
                with open(path, 'wb') as f:
                    while True:
                        chunk = conn.recv(1024)
                        if b"<FILEEND>" in chunk:
                            chunk = chunk.replace(b"<FILEEND>", b"")
                            f.write(chunk)
                            break
                        f.write(chunk)
                send_msg(conn, f"Upload complete.\n[DIR]{os.getcwd()}")
                log_event(f"File uploaded: {path}")
            except Exception as e:
                send_msg(conn, f"Upload failed: {e}")
                log_event(f"Upload failed for {path}: {e}")

        else:
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                send_msg(conn, output.decode() + f"\n[DIR]{os.getcwd()}")
                log_event(f"Executed command: {command}")
            except subprocess.CalledProcessError as e:
                send_msg(conn, e.output.decode() + f"\n[DIR]{os.getcwd()}")
                log_event(f"Command failed: {command} | Error: {e.output.decode()}")

    conn.close()

def get_valid_port():
    while True:
        try:
            port = int(input("Enter port to listen on: "))
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('0.0.0.0', port))
            test_socket.close()
            return port
        except Exception as e:
            print(f"Port unavailable: {e}. Please choose another port.")

if __name__ == "__main__":
    USERNAME = input("Set a username: ")
    PASSWORD = input("Set a password: ")
    PORT = get_valid_port()
    HOST = '0.0.0.0'

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind((HOST, PORT))
                server.listen(1)
                print(f"[+] Listening on {HOST}:{PORT}")
                log_event(f"Server started on {HOST}:{PORT}")

                conn, addr = server.accept()
                print(f"[+] Connection from {addr}")
                handle_client(conn, addr, USERNAME, PASSWORD)
        except Exception as e:
            log_event(f"Server error: {e}")
            print(f"[!] Server crashed: {e}. Restarting in 5 seconds...")
            time.sleep(5)  # Wait before retrying
