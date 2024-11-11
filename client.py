import socket # para poder crear el socket
import threading # para poder crear varios hilos

# configuramos el cliente
HOST = '127.0.0.1'  # asignamos una direccion ip al servidor
PORT = 12345        # asignamos un puerto

# configuramos el socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# inicializamos la variable de clave de encriptacion en None 
encryption_key = None

# funcion para recibir mensajes
def receive_messages():
    global encryption_key
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("KEY:"):
                encryption_key = int(message.split(":")[1])
                print(f"Clave de cifrado recibida: {encryption_key}")
            else:
                print(message)
        except:
            print("Error al recibir el mensaje. Conexion cerrada.")
            client_socket.close()
            break
        
        
# funcion para enviar mensajes
def send_message():
    global encryption_key
    while True:
        message = input("")
        
        if message.startswith("KEY:"):
            encryption_key = int(message.split(":")[1])
            print(f"Clave de cifrado establecida: {encryption_key}")
            client_socket.send(message.encode('utf-8'))
        elif encryption_key is None:
            client_socket.send(message.encode('utf-8'))
        else:
            encrypted_message = cifrado_cesar(encryption_key, message)
            client_socket.send(encrypted_message.encode('utf-8'))

# iniciamos un hilo para reciver mensajes
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# iniciamos un hilo para enviar mensajes
send_thread = threading.Thread(target=send_message)
send_thread.start()

# funcion de cifrado (la reutilice del ejercicio pasado xd)
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