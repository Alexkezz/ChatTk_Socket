import socket
import threading

mi_servidor = socket.socket()
PORT = 4444
IP = "localhost"
mi_servidor.bind((IP, PORT))
mi_servidor.listen(100)

lista_clientes = []

def inicio_cliente(conn, addr):
    conn.send("Te has connectado al chat de 2SMXA\n".encode())

    while True:
        try:
            respuesta = conn.recv(1024)
            if respuesta:
                respuesta = respuesta.decode()
                print("{} >> {}".format(addr, respuesta))
                broadcast(conn, respuesta)
            else:
                removeclients(conn)
        except:
            continue

def broadcast(conexion, messaje):
    for clientes in lista_clientes:
        if clientes != conexion:
            try:
                clientes.send(messaje.encode())
            except:
                clientes.close()
                removeclients(clientes)

def removeclients(connection):
    if connection in lista_clientes:
        del lista_clientes[connection]

while True:
    conx, addrs = mi_servidor.accept()
    print("Este usuario {} se ha connectado!".format(addrs[0]))
    lista_clientes.append(conx)
    threading.Thread(target=inicio_cliente, args=(conx, addrs)).start()

conx.close()
mi_servidor.close()
