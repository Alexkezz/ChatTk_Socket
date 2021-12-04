from tkinter import *
from PIL import ImageTk, Image
import socket
import threading

root = Tk()
root.title("Chat_Privado")
root.resizable(0, 0)
root.config(bg="grey")
 
#SOCKET-------------------------------------------------------

mi_cliente = socket.socket()
PORT = 4444 
IP = "localhost"

#FRAMES--------------------------------
f_chat = Frame(root)
f_chat.config(width=520, height=300, bg="white", border=3, relief="ridge")
 
f_message = Frame(root)
f_message.config(width=516, height=300)
 
f_portada = Frame(root)
f_portada.config(width=420, height=616, bg="white", border=3, relief="ridge")
 
f_chat.grid(row=0, column=0, pady=8, padx=(10,0))
f_chat.grid_propagate(False)
f_message.grid(row=1,column=0, pady=8, padx=(10,0))
f_message.grid_propagate(False)
f_portada.grid(row=0, column=1, padx=10, rowspan=2)
f_portada.grid_propagate(False)
#chat--------------------------------
 
chat_mensaje = Text(f_chat, font=("Calibri", 13))
chat_mensaje.grid(row=0, column=0)
scroll_message2 = Scrollbar(f_chat, command=chat_mensaje.yview)
scroll_message2.grid(row=0, column=1, sticky="nesw")
chat_mensaje.config(width=55, height=14, yscrollcommand=scroll_message2.set, state=DISABLED)


#FUNCIONES-------------------------------------------------------------------------------------


def escrbir_pantalla_mio(texto_pantalla):
    mi_cliente.send(texto_pantalla.encode())
    chat_mensaje.config(state=NORMAL)
    inp_message.delete("1.0", "end")
    chat_mensaje.insert(INSERT, "Tu >>" + texto_pantalla)
    chat_mensaje.see(END)
    chat_mensaje.config(state=DISABLED)
    

def recive_messaje():
    while True:
        try:
            mensaje = mi_cliente.recv(1024)
            mensaje = mensaje.decode()
            mostrar_mensaje_socket(mensaje)
        except OSError:
            break

first_messaje = 0

def mostrar_mensaje_socket(mss):
    global first_messaje
    chat_mensaje.config(state=NORMAL)
    if first_messaje != 0:
        chat_mensaje.insert(INSERT, "Amigo >> {}".format(mss))
    else:
        chat_mensaje.insert(INSERT, "Server >> {}".format(mss))
        first_messaje = 1
    chat_mensaje.see(END)
    chat_mensaje.config(state=DISABLED)

#MENSAJE CONT--------------------------------
 
inp_message = Text(f_message, font=("Calibri", 13))
inp_message.grid(row=0, column=0)
scroll_message = Scrollbar(f_message, command=inp_message.yview)
scroll_message.grid(row=0, column=1, sticky="nesw")
inp_message.config(width=55, height=12, yscrollcommand=scroll_message.set)
 
send_button = Button(f_message, font=("Calibri", 15), text="SEND", command=lambda:escrbir_pantalla_mio(inp_message.get("1.0", END)))
send_button.place(x=455, y=260, width=60, height=40)
 
#MENSAJE CONT--------------------------------
 
#PORTADA DERECHA--------------------------------
connection = Label(f_portada, text="CHAT CREADO PARA 2SMX", font=("Calibri", 15))
connection.place(x=85)
 
image_import = Image.open("./Hermes2.jpg")
image_import = image_import.resize((412, 555), Image.ANTIALIAS)
 
img_portada = ImageTk.PhotoImage(image_import)
lbl_img = Label(f_portada, image=img_portada)
lbl_img.place(y=65)
 
#PORTADA DERECHA--------------------------------

mi_cliente.connect((IP, PORT))
threading.Thread(target=recive_messaje).start()
root.mainloop()
