import socket
import os
import sys
from gpt4all import GPT4All


HOST = "127.0.0.1"   # localhost
PORT = 5050          # port number



def suppress_stderr():
    sys.stderr.flush()
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    os.dup2(devnull, 2)
    os.close(devnull)
    return old_stderr


def restore_stderr(old_stderr):
    sys.stderr.flush()
    os.dup2(old_stderr, 2)
    os.close(old_stderr)



model_path = r"C:\Users\Rafael\AppData\Local\nomic.ai\GPT4All\Llama-3.2-3B-Instruct-Q4_0.gguf"

if not os.path.exists(model_path):
    print(f" Model file not found at: {model_path}")
    sys.exit(1)

print(" Starting server...")
print(" Loading model, please wait...")

try:
    # suppress warnings only during load
    old_stderr = suppress_stderr()
    model = GPT4All(model_path,allow_download=False)
    restore_stderr(old_stderr)
except Exception as e:
    print(" Failed to load model:", e)
    sys.exit(1)

print(" Chatbot model loaded successfully!\n")



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((HOST, PORT))
except OSError as e:
    print(f" Failed to bind to {HOST}:{PORT} — {e}")
    sys.exit(1)

server_socket.listen(1)
print(f"  Server running on {HOST}:{PORT} — waiting for client...\n")



conn, addr = server_socket.accept()
print(f" Connected to client: {addr}\n")



while True:
    try:
        data = conn.recv(1024).decode()
        if not data or data.lower() in ["exit", "quit"]:
            print(" Client disconnected.")
            break

        print(f"User: {data}")
        prompt = f"Answer this in one line, without any links or markdown: {data}"
        response = model.generate(prompt, max_tokens=200)
        conn.send(response.encode())
        print(f"Bot: {response}\n")

    except ConnectionResetError:
        print("  Client connection lost.")
        break
    except Exception as e:
        print(f"  Error during processing: {e}")
        break



conn.close()
server_socket.close()
print(" Server shut down.")
