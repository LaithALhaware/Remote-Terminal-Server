# 🖥️🔗 Remote Terminal Server 

A lightweight Python-based server that allows remote control of a system's terminal over a secure network connection. Useful for administrative tasks, scripting, automation, and remote debugging.


## 🚀 Features

- ⚡ Remote shell access via TCP  
- 🔐 Authentication system (if implemented)  
- ⏱️ Real-time command execution  
- 📝 Logs of executed commands (optional)  
- 🌐 Cross-platform (Linux, macOS, Windows)


## 📦 Requirements

- 🐍 Python 3.7+  
- 📦 (Optional) Python standard libraries: `socket`, `threading`, or `asyncio`


## 🛠 Installation

- Open CMD 🖥️


| **Operating System** | **Steps**                                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| **Windows** 💻        | 1. Press `Windows + R` to open the "Run" dialog box. <br> 2. Type `cmd` and hit `Enter`. <br> 3. The Command Prompt (CMD) will open. <br> Alternatively, you can search for "Command Prompt" in the Start menu and click to open it. 🔍 <br> 4. To navigate to the Desktop, type `cd %USERPROFILE%\Desktop` and hit `Enter`. 📂        |
| **Linux** 🐧          | 1. Press `Ctrl + Alt + T` to open the terminal. <br> 2. Alternatively, search for "Terminal" in your applications menu. 💨 <br> 3. To navigate to the Desktop, type `cd ~/Desktop` and hit `Enter`. 📂        |


- Clone the repository or download the project files to your local machine 📂  :
```bash
git clone https://github.com/LaithALhaware/Remote-Terminal-Server.git
cd Remote-Terminal-Server
```

- Install dependencies (if any):

```bash
pip install -r requirements.txt
```

## ▶️ Usage
- Start the server :
   ```bash
   python Server_Auth.py
   ```

- Connect with client (example using telnet or custom script) :
  ```bash
   telnet SERVER_IP PORT
   ```
   Or use the included client script:

   ```bash
   python Client_Auth.py
   ```

## 🛡️ Security Notes
⚠️ This tool opens a remote shell, **so do not expose it to the internet without proper security**:
- 🔒 Add authentication
- 🔐 Use encrypted tunnels (e.g., SSH, TLS)
- 🛡️ Whitelist allowed IPs
- 👤 Run with restricted permissions


## 📝 Output Example in server_log.txt:
   ```bash
[2025-05-20 15:23:01] Server started on 0.0.0.0:4444
[2025-05-20 15:23:05] Connection from 192.168.1.12:52123
[2025-05-20 15:23:08] User Laith authenticated from 192.168.1.12
[2025-05-20 15:23:15] Executed command: ls -l
[2025-05-20 15:23:20] File uploaded: notes.txt
[2025-05-20 15:23:30] User Laith disconnected.
   ```

## 📁 Project Structure
   ```bash
   .
   ├── Server_Auth.py         # 🖥️ Main server script
   ├── Client_Auth.py         # 💻 Optional client script
   ├── README.md         # 📄 Project documentation
   └── requirements.txt  # 📦 Python dependencies
   ```

## 📝 License
This project is licensed under the **License**. See the [LICENSE.txt](LICENSE.txt) ⚖️ file for details.

---
## ❤️ Support This Project
If you find this project useful, consider supporting its development:

💰 Via PayPal: [[PayPal Link](https://www.paypal.com/ncp/payment/KC9EETJDVZQHG)]

Your support helps keep this project alive! 🚀🔥

