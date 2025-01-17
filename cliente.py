import threading
import socket
import pygame
import sys
from button import *
from players import *
from pygame.locals import*
from sys import *
from spritesheet import SpriteSheet, Origin


HOST = '127.0.0.1' 
PORT = 42069 


player1 = Jogador()
player2 = Jogador()
turno= False
j1vivo = True
j2vivo = True

pygame.init()
pygame.mixer.init()
musica_fundo = pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play(-1)
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1600/2, 900/2
screen = pygame.display.set_mode((width, height))
animacao = SpriteSheet("fundo2.png", 4, 2)
quantidade_frame = animacao.sprite_count() - 1
fonte = pygame.font.Font(None, 40)
frame_atual = 0

button = Button(0, 395, 100, 50, (204, 169, 221), "Dano:10", (0, 0, 0), -10)
button1 = Button(110, 395, 100, 50, (204, 169, 221), "Dano:20", (0, 0, 0), -20)
button2 = Button(220, 395, 100, 50, (204, 169, 221), "Dano:30", (0, 0, 0), -30)
button3 = Button(330, 395, 100, 50, (204, 169, 221), "Vida:+15", (0, 0, 0), -10)
button4 = Button(440, 395, 100, 50, (204, 169, 221), "Mana:+10", (0, 0, 0), 0)

def main():
    global status1, status2, retangulo_mana1, retangulo_mana2, retangulo_vida1, retangulo_vida2, j1vivo, j2vivo
    

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
    except:
        return print("\nNão foi possivel se conectar com o servidor, desculpe!\n")

    print("\nConectado")

    thread1 = threading.Thread(target=recebe_mensagem, args=[cliente])
    thread1.start()

    while True:
        global frame_atual
        screen.fill((0, 0, 0))
        fonte = pygame.font.Font(None, 36)
        status1 = str(player1)
        status1 = status1.split('||')
        status2 = str(player2)  
        status2 = status2.split('||')
        if status1[0] == ' vida:0 ':
            status1[0] = 'DERROTA'
            status2[0] = 'VITORIA'
            j1vivo = False
        if status2[0] == ' vida:0 ':
            status2[0] = 'DERROTA'
            status1[0] = 'VITORIA'
            j2vivo = False
        
        superficie_vida1 = fonte.render(status1[0], True, (223, 54, 57))
        retangulo_vida1 = superficie_vida1.get_rect()
        retangulo_vida1.center = (50, 10)
        superficie_mana1 = fonte.render(status1[1], True, (71, 217, 254))
        retangulo_mana1 = superficie_mana1.get_rect()
        retangulo_mana1.center = (50, 40)

        superficie_vida2 = fonte.render(status2[0], True, (223, 54, 57))
        retangulo_vida2 = superficie_vida2.get_rect()
        retangulo_vida2.center = (750, 10)
        superficie_mana2 = fonte.render(status2[1], True, (71, 217, 254))
        retangulo_mana2 = superficie_mana2.get_rect()
        retangulo_mana2.center = (750, 40)

        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_button = None
                    
                    if button.is_clicked(mouse_pos):
                        clicked_button = button
                    elif button1.is_clicked(mouse_pos):
                        clicked_button = button1
                    elif button2.is_clicked(mouse_pos):
                        clicked_button = button2
                    elif button3.is_clicked(mouse_pos):
                        clicked_button = button3
                    elif button4.is_clicked(mouse_pos):
                        clicked_button = button4
                    
                    if clicked_button and turno and j2vivo and j1vivo and (int(player1.getMana()) >= (int(clicked_button.mana_cost*-1))):
                        trata_comando(clicked_button.text, player1, player2)
                        manda_mensagem(cliente, clicked_button.text)

        thread3 =   threading.Thread(target=atualiza)   
        thread3.start       
                            
        if frame_atual >= quantidade_frame:
            frame_atual = 0
        else:
            frame_atual += 0.1

        
        animacao.blit(screen, int(frame_atual), (width / 2, height / 2), Origin.Center)
        
        button.draw(screen)
        button1.draw(screen)
        button2.draw(screen)
        button3.draw(screen)
        button4.draw(screen)
        pygame.display.get_surface().blit(superficie_vida1, retangulo_vida1)
        pygame.display.get_surface().blit(superficie_mana1, retangulo_mana1)
        pygame.display.get_surface().blit(superficie_vida2, retangulo_vida2)
        pygame.display.get_surface().blit(superficie_mana2, retangulo_mana2)

        pygame.display.flip()
        fpsClock.tick(fps)

def recebe_mensagem(cliente):
    while True:
        try:
            global turno, player1, player2
            msg = cliente.recv(2048).decode('utf-8')
            print(msg)
            if msg == "PRIMEIRO":
                turno = True
            msg = msg.split(" ")
            
            if len(msg) > 1:
                    turno = True
                    trata_comando(msg[1], player2, player1)

        except:
            print("Não foi possivel permanecer conectado ao servidor, desculpe\n")
            cliente.close()
            break

def manda_mensagem(cliente, msg):
    try:
        global turno
        if turno:
            cliente.send(f'SEU_TURNO {msg}'.encode('utf-8'))
            turno = False

    except:
        return

def trata_comando(comandoBotao, atacou, levou): 
    match comandoBotao:
        case 'Dano:10': 
            atacou.golpe_1(levou)
        case 'Dano:20': 
            atacou.golpe_2(levou)
        case 'Dano:30': 
            atacou.golpe_3(levou)
        case 'Vida:+15': 
            atacou.curar(levou)
        case 'Mana:+10': 
            atacou.cura_mana(levou)

        
    
def atualiza():
    global status2, status1

    status1 = str(player1)
    status1 = status1.split('||')
    status2 = str(player2)
    status2 = status2.split('||')

    
    superficie_vida1 = fonte.render(status1[0], True, (223, 54, 57))
    superficie_mana1 = fonte.render(status1[1], True, (71, 217, 254))
    superficie_vida2 = fonte.render(status2[0], True, (223, 54, 57))
    superficie_mana2 = fonte.render(status2[1], True, (71, 217, 254))

    
    screen.blit(superficie_vida1, retangulo_vida1)
    screen.blit(superficie_mana1, retangulo_mana1)
    screen.blit(superficie_vida2, retangulo_vida2)
    screen.blit(superficie_mana2, retangulo_mana2)

    
    pygame.display.update()


player1 = Jogador()
player2 = Jogador()




main()

