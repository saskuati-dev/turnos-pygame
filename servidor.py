import threading
import socket

HOST = '127.0.0.1' 
PORT = 42069
clients = []

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servidor.bind((HOST, PORT))
        servidor.listen(2)
    except:
        return print("\nNão foi possivel iniciar o servidor!")
    while True:
        cliente, adr =servidor.accept()
        clients.append(cliente)
        if len(clients) == 1:
            mensagem_inicial = "PRIMEIRO"
            cliente.send(mensagem_inicial.encode())
            
        
        thread = threading.Thread(target=tratamento_mensagem, args=[cliente])
        thread.start()

def trasnmite_mensagem(msg,cliente):
    for Itemcliente in clients:
        if Itemcliente != cliente:
            try:
                if msg != '\0':
                    Itemcliente.send(msg)
                else:
                    pass
            except:
                deleta_cliente(Itemcliente)
                


def deleta_cliente(cliente):
    clients.remove(cliente)

def tratamento_mensagem(cliente):
    while True:
        try:
            msg = cliente.recv(2048)
            trasnmite_mensagem(msg, cliente)
        except:
            deleta_cliente(cliente)
            break

        
main()