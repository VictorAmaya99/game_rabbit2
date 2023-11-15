import pygame
from sys import exit
from config import *
from pygame.locals import *
from random import randint
from Module import *
import json

#Inicializa modulos de pygame:
pygame.init()

#Configuracion de la pantalla principal
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("rabbit runner")
clock = pygame.time.Clock()

#Fuente:
test_font = pygame.font.Font("./src/assets/ShortBaby-Mg2w.ttf", 30)  
game_active = False
start_time = 0  #Se crea una variable para indicar cuando se inicia el juego que por defecto inicia en 0.
reverse_time = 5

score = 0 #Se crea una variable para mostrar el score que inicia en 0
score_path = "./scores.json"

reverse = 0
collision = True
lives = 3
collision_cooldown_start = 0
playing_music = True


#set sonido game over:
game_over_sound = pygame.mixer.Sound("./src/assets/game_over.mp3")
ouch_sound = pygame.mixer.Sound("./src/assets/ouch1.mp3")

#Musica de fondo:
pygame.mixer.music.load("./src/assets/melody.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

#crear fondo:
ground = pygame.transform.scale(pygame.image.load("./src/assets/ground.png"), SCREEN_SIZE)

#Imagen play:
play_img = pygame.image.load("./src/assets/play.png").convert_alpha()

#Obstaculos:
snake_surf = pygame.image.load("./src/assets/snake.png").convert_alpha()
snake_surf = pygame.transform.scale(snake_surf, SNAKE_SIZE)

hawk_surf = pygame.image.load("./src/assets/hawk.png").convert_alpha()
hawk_surf = pygame.transform.scale(hawk_surf, HAWK_SIZE)

#Imagen para contar las vidas usadas
carrot_img = pygame.image.load("./src/assets/carrot.png").convert_alpha()
carrot_img = pygame.transform.scale(carrot_img, (30, 30))

obstacle_rect_list = []

#Rabbit player
rabbit_l = pygame.image.load("./src/assets/conejo.png").convert_alpha()
rabbit_l = pygame.transform.scale(rabbit_l, RABBIT_SIZE) 
rabbit_r = pygame.image.load("./src/assets/conejo2.png").convert_alpha()
rabbit_r = pygame.transform.scale(rabbit_r, RABBIT_SIZE) 
#rabbit_rect = rabbit_surf.get_rect(bottomleft = (10, 390))
rabbit = rabbit_l
rabbit_rect = rabbit_l.get_rect(bottomleft = (10, 390))
rabbit_gravity = 0

#Pantalla de inicio
rabbit_face = pygame.image.load("./src/assets/rabbit_face.png").convert_alpha()
rabbit_face = pygame.transform.scale(rabbit_face, RABBIT_FACE_SIZE)
rabbit_face_rect = rabbit_face.get_rect(center = (400, 200))

game_name = test_font.render("Jumping Rabbit", False, GREY)
game_name_rect = game_name.get_rect(center = (400, 100))


live_surf = pygame.image.load("./src/assets/carrot_live.png").convert_alpha()
live_surf = pygame.transform.scale(live_surf, LIVE_SIZE)

extra_lives = []


#Timer: Crear un evento propio
obstacle_timer = pygame.USEREVENT + 1 #como pygame tiene eventos propios se pone +1 para evitar que el evento creado tenga conflicto con éstos
pygame.time.set_timer(obstacle_timer, 1500) #asi se llama al evento user, determinando el tiempo en que recorren los obstaculos

extra_live_timer = pygame.USEREVENT + 2
pygame.time.set_timer(extra_live_timer, LIVE_SPAWN_TIME)

start_button = Button(180, 170, play_img, 0.5)

is_running = True

try: 
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                
            keys = pygame.key.get_pressed()   

            if game_active:        

                if keys [pygame.K_LEFT]:
                    if rabbit_rect.left > DISPLAY_LEFT:
                        rabbit_rect.x -= RABBIT_SPEED
                        rabbit = rabbit_r

                if keys [pygame.K_RIGHT]:
                    if rabbit_rect.right < DISPLAY_RIGTH:
                        rabbit_rect.x += RABBIT_SPEED
                        rabbit = rabbit_l
                
                if event.type == pygame.MOUSEBUTTONDOWN and rabbit_rect.bottom >= 390:
                    if rabbit_rect.collidepoint(event.pos):
                        rabbit_gravity = -20

                if event.type == pygame.KEYDOWN and rabbit_rect.bottom >= 390:
                    if event.key == pygame.K_SPACE:
                        rabbit_gravity = -20
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000) #Si el juego se inicia el tiempo de inicio empieza en 0
                    reverse_time = int(pygame.time.get_ticks() / 1000)

            if event.type == obstacle_timer and game_active: #Si el evento es usado y el juego activo
                if randint(0,2): #Se usa randit como enunciado que devolvera 0 o 1, osea false o true
                    obstacle_rect_list.append(snake_surf.get_rect(bottomright = (randint(900, 1100), 380)))
                else:
                    obstacle_rect_list.append(hawk_surf.get_rect(bottomright = (randint(900, 1100), 220)))

            if event.type == extra_live_timer and game_active:
                if randint(0,100) < LIVE_SPAWN_CHANCE:
                    extra_lives.append(live_surf.get_rect(bottomright = (randint(900, 1100), randint(100,300))))
            
        
            #Para pausar la musica:
            if event.type == pygame.KEYDOWN and event.key == K_m:
                if playing_music:
                        pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                    playing_music = not playing_music

            # #Pausar el juego:
            if event.type == KEYDOWN and event.key == K_p:
                if playing_music:
                    pygame.mixer.music.pause()
                show_text(screen, "Pause", test_font, CENTER, GREY, LIGHT_PINK)
                pygame.display.flip()
                click_pause()    
                if playing_music:
                    pygame.mixer.music.unpause()
                    
        #parte del juego
        if game_active:
            
            screen.fill(CUSTOM)
            screen.blit(ground,ORIGIN)
            score = display_score(start_time, test_font, BLACK, screen) #Se llama a la funcion para mostrar el score
            #reverse = display_lives(reverse_time, test_font, BLACK, screen)
                

            #Conejo
            rabbit_gravity += 1
            rabbit_rect.y += rabbit_gravity
            if rabbit_rect.bottom >= 390:
                rabbit_rect.bottom = 390
            
            screen.blit(rabbit, rabbit_rect)

            #obstacle movement: la lista de obstaculos se le sobreescribe la funcion de movimiento de obstaculos, asi continuamente
            # se actualiza la lista.
            obstacle_rect_list = obstacle_movement(obstacle_rect_list, snake_surf, hawk_surf, screen)
            extra_lives = lives_movement(extra_lives, live_surf, screen)
                
            #Colision:
            # if collision: 
            #     game_active = collisions(rabbit_rect, obstacle_rect_list)#Se sobre escrive el game_active con la funcion para que esta funcione
            #     #                     # si colisiona es false y vuelve a la intro para recomenzar el juego.

            if collision and pygame.time.get_ticks() - collision_cooldown_start > COLLISION_COOLDOWN:
                for obstacle_rect in obstacle_rect_list:
                    if rabbit_rect.colliderect(obstacle_rect):
                        lives -= 1
                        obstacle_rect_list.remove(obstacle_rect)
                        collision_cooldown_start = pygame.time.get_ticks()
                        ouch_sound.play()

                        if lives <= 0:
                            game_active = False
                            game_over_sound.play()
                            update_high_score(score)
                            lives = 3  # Restablecer vidas al reiniciar el juego

            
            for live_rect in extra_lives:
                screen.blit(live_surf, live_rect)
                if rabbit_rect.colliderect(live_rect):
                    extra_lives.remove(live_rect)
                    lives += 1  # Aumenta las vidas cuando el conejo recoge una vida extra
        
            # Dibujar el contador de vidas
            for i in range(lives):
                screen.blit(carrot_img, (10 + i * 40, 10))

        #Intro
        else:
            screen.fill(CUSTOM2)
            screen.blit(rabbit_face, rabbit_face_rect)
            obstacle_rect_list.clear() #Cuando el juego se acaba, esto hace que la lista se quede vacia
            extra_lives.clear()
            rabbit_rect.midbottom = (80, 300) #Se ubica al jugador en el mismo lugar cada vez que e juego se reinicia
            # y la gravedad tambien deberá reiniciar en 0
            rabbit_gravity = 0 

            score_message = test_font.render(f"Your time score is : {score} sec", False, GREY) #mensaje que muestra el score hecho
            score_message_rect = score_message.get_rect(center = (400,330))
            screen.blit(game_name, game_name_rect)        

            # Dibujar puntaje más alto en la pantalla principal
            draw_high_score(test_font, LIGHT_BLUE, screen)
            
                
            if score == 0:                            
                    if start_button.draw(screen):
                        game_active = True
                            
            else:
                if collision:
                    screen.blit(score_message, score_message_rect) # Si no es 0 se muesta el score
                                
        pygame.display.update()
        clock.tick(FPS)
except Exception as e:
    print(f"Se produjo un error: ")
end()  