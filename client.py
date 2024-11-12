import socket
import threading
import hashlib

# Configuracion del cliente
HOST = '127.0.0.1'  # Direccion IP del servidor
PORT = 12345        # Puerto del servidor

# Configuracion del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Inicializamos la variable de clave de encriptacion en None
encryption_key = None

def receive_messages():
    """Escucha los mensajes del servidor y los muestra en pantalla."""
    global encryption_key
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.__contains__("KEY:"):
                parts = message.split(":")
                encryption_key = int(parts[1])
                received_hash = parts[2]
                print(f"Clave de cifrado recibida: {encryption_key}")
             
                
                # Generamos el hash de la clave recivida
                generated_hash = hashlib.sha256(str(encryption_key).encode()).hexdigest()
                print(f"Hash generado de la clave recibida: {generated_hash}")
                print("------------------------------------------------------------------")
                print(f"Hash recibido: {received_hash}")
                
                # Realizamos la comparacion de los hashes
                if generated_hash == received_hash:
                    print("Los hashes generados son iguales.")
                    client_socket.send("Hashes iguales".encode('utf-8'))
                else:
                    print("Los hashes generados no son iguales.")
            else:
                print(message)
        except Exception as e:
            print(f"Error al recibir el mensaje: {e}. Conexion cerrada.")
            client_socket.close()
            break

def send_message():
    """Envía un mensaje al servidor."""
    global encryption_key
    while True:
        message = input("")
        
        if message.__contains__("KEY:"):
            encryption_key = int(message.split(":")[1])
            print(f"Clave de cifrado establecida: {encryption_key}")
            
            # Generamos un el hash de la clave 
            key_hash = hashlib.sha256(str(encryption_key).encode()).hexdigest()
            
            # Enviamos la clave y su hash
            client_socket.send(f"KEY:{encryption_key}:{key_hash}".encode('utf-8'))
        elif encryption_key is None:
            client_socket.send(message.encode('utf-8'))
        else:
            encrypted_message = cifrado_cesar(encryption_key, message)
            client_socket.send(encrypted_message.encode('utf-8'))

# Iniciar hilo para recibir mensajes
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Iniciar hilo para enviar mensajes
send_thread = threading.Thread(target=send_message)
send_thread.start()

# Funcion para el  cifrado cesar
def cifrado_cesar(key, message):
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    palabra = message
    clave = key
    palabra_cifrada = ""
    
    for letra in palabra:
        if letra == " ":
            palabra_cifrada += " "
        else:
            indice_actual = alfabeto.index(letra)
            nuevo_indice = (indice_actual + clave) % 26
            palabra_cifrada += alfabeto[nuevo_indice]
    
    return palabra_cifrada