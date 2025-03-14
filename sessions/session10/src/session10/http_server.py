import socket
import logging

# logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("server.log"),  
        logging.StreamHandler()
    ]
)
HOST, PORT = '127.0.0.1', 8080

def handle_request(request_data):
    try:
        request_line = request_data.split('\n', 1)[0]
        method, path, _ = request_line.split()

        logging.info(f"Received {method} request for {path}")

        if path == '/':
            return handle_root(request_line, path)
        elif path == '/about':
            return handle_about()
        else:
            logging.warning(f"Path not found: {path}")
            return handle_not_found()
    except Exception as e:
        logging.error(f"Error handling request: {e}")
        return handle_server_error()

# Endpoints w/ 404 if unsupported path
def handle_root(request_line, path):
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "\r\n"
        "<html><body><h1>Home!</h1>"
        f"<h2>Request line: {request_line}</h2>"
        f"<h2>Path: {path}</h2>"
        "</body></html>"
    )

def handle_about():
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "\r\n"
        "<html><body><h1>About me</h1></body></html>"
    )

def handle_not_found():
    return (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "\r\n"
        "<html><body><h1>404 Not Found</h1><p>The requested page was not found.</p></body></html>"
    )

def handle_server_error():
    return (
        "HTTP/1.1 500 Internal Server Error\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "\r\n"
        "<html><body><h1>500 Internal Server Error</h1><p>Something went wrong on the server.</p></body></html>"
    )

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Allow immediate reuse of address after program exit
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))
    # Listen for incoming connections
    server_socket.listen(1)
    logging.info(f"Serving HTTP on {HOST} port {PORT} ...")

    while True:
        # Accept a new client connection
        client_connection, client_address = server_socket.accept()
        with client_connection:
            try:
                request_data = client_connection.recv(1024).decode('utf-8')
                logging.debug(f"Received raw request data: {request_data}")

                http_response = handle_request(request_data)
                client_connection.sendall(http_response.encode('utf-8'))
                logging.info(f"Sent response to {client_address}")
            except Exception as e:
                logging.error(f"Error processing request from {client_address}: {e}")
                http_response = handle_server_error()
                client_connection.sendall(http_response.encode('utf-8'))