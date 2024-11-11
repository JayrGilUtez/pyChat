import socket # para poder crear el socket
import threading # para poder crear hilos

# configuramos el servidor
HOST = '127.0.0.1'  # asignamos una direccion ip
PORT = 12345        # asignamos un puerto 

# configuramos el socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # aqui podemos elegir el numero de clientes que queramos en el chat en esta caso por defecto seran 5

# creamos una array para guardar los clientes
clients = []

# esta funcion envia el mensaje a todos los clientes excepto al que envio el mensaje
def broadcast(message, client_socket):

    for client in clients:
        if client[0] != client_socket:
            try:
                client[0].send(message)
            except:
                client[0].close()
                clients.remove(client)
                
                
# esta funcion maneja la conexion de cada cliente
def handle_client(client_socket, client_address):
    while True:
        try:
            # recibimos mensaje del cliente
            message = client_socket.recv(1024)
            if not message:
                break
            # agregamos la direccion del cliente al mensaje (para saber quien dice que cosa xd)
            message_to_send = f"Cliente {client_address[1]} dice -> {message.decode('utf-8')}".encode('utf-8')
            # enviamos el mensaje a todos los demas clientes
            broadcast(message_to_send, client_socket)
        except:
            # eliminamos de la lista de clientes a todo aquel cliente que haya obtenido algun error
            clients.remove((client_socket, client_address))
            client_socket.close()
            break
        
        
# con esta funcion permitiremos que se conecten los clientes al servidor
def receive_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida con {client_address}")
        # agregamos el cliente a la lista
        clients.append((client_socket, client_address))
        # con cada nuevo cliente se crea un nuevo hilo para poder manejar su conexion
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

# iniciamos el servidor
print("Servidor iniciado. Esperando conexiones...")
receive_connections()