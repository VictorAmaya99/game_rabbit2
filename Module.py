import pygame
from math import sqrt
from pygame.locals import *
from config import *
import json
from random import randint

def end():
    pygame.quit()
    exit()

def display_score(start, font, color, surface): #Recibe cuatro parametros el tiempo de inicio, la fuente, el color y la superficie
    current_time = int(pygame.time.get_ticks() / 1000) - start #Muestra el tiempo desde el inicio del juego, como devuelve numeros desde el
    # mil se le divide entre 1000 y se le encierra en un int para que devuelva numeros enteros desde el 0, para eso se tiene que restar
    # con el tiempo de inicio que el jugador arranco el juego 
    score_surf = font.render(f"Time running: {current_time} sec", False, (color)) #crea la superficie para mostrar el score.
    score_rect = score_surf.get_rect(center = (400, 50)) #Crea el rectangulo del score
    surface.blit(score_surf, score_rect) # Muestra el score en la superficie
    return current_time

def display_lives(reverse, font, color, surface):
    current_time = int(pygame.time.get_ticks() / 1000) - reverse #Muestra el tiempo desde el inicio del juego, como devuelve numeros desde el
    # mil se le divide entre 1000 y se le encierra en un int para que devuelva numeros enteros desde el 0, para eso se tiene que restar
    # con el tiempo de inicio que el jugador arranco el juego 
    score_surf = font.render(f"Time running: {current_time} sec", False, (color)) #crea la superficie para mostrar el score.
    score_rect = score_surf.get_rect(topleft = (400, 70)) #Crea el rectangulo del score
    surface.blit(score_surf, score_rect) # Muestra el score en la superficie
    return current_time

def obstacle_movement(obstacle_list, surf1, surf2, surface):
    if obstacle_list: #lista vacia
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5   #velovidad los obstaculos desde la izquierda
            if obstacle_rect.bottom == 380:
                surface.blit(surf1, obstacle_rect)
            else:
                surface.blit(surf2, obstacle_rect)            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] #Para desaparecer los obstaculos cuando pasen
        # el borde izquiero, se hace una list comprehension, que ve si los obstaculos pasaron el borde para borrarlos si salen de la pantalla.
        return obstacle_list #Si hay movimiento retorna una lista
    else:
        return [] #Si no hay movimiento devuelve lista vacia

def collisions(player, obstacles):
    if obstacles: #lista vacia
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): #Cheque que cualquiera de los obstaculos collisionan con el player
                return False  #Si colisiona retorna false se vincula con game active
    return True #retorna true y el juego sigue activo
 
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos() #la posicion del mouse
        if self.rect.collidepoint(pos):#Condiciones sobre el cursor sobre el mouse
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
    def display_lives(lives, font, color, surface):
        lives_text = font.render(f"lives: {lives}", True, color)
        surface.blit(lives_text, (10,40))

def check_collision(player_rect, obstacle_rect_list):
    for obstacle_rect in obstacle_rect_list:
        if player_rect.colliderect(obstacle_rect):
            return True
    return False

def click_pause():
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                end()        
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    end()
                return None

def show_text(surface, text, font, coordinates, fond_color, background_color=BLACK):
    sup_text = font.render(text, True, fond_color, background_color)
    text_rect = sup_text.get_rect()
    text_rect.center = coordinates
    surface.blit(sup_text, text_rect)

def read_high_score():
    try:
        score_path = "./scores.json"
        with open(score_path, "r") as file:
            data = json.load(file)
            return data["high_score"]
    except FileNotFoundError:
        return 0

def update_high_score(new_score):
    score_path = "./scores.json"
    current_high_score = read_high_score()
    if new_score > current_high_score:
        with open(score_path, "w") as file:
            json.dump({"high_score": new_score}, file)

def draw_high_score(font, color, screen):
    high_score = read_high_score()
    high_score_text = font.render(f"High Score: {high_score}", False, color)
    screen.blit(high_score_text, (10, 10))

    live_surf = pygame.image.load("./src/assets/carrot_live.png").convert_alpha()
    live_surf = pygame.transform.scale(live_surf, (50,50))

def lives_movement(live_list, surf1, surface):
    if live_list: #lista vacia
        for live_rect in live_list:
            live_rect.x -= 5   #velovidad los obstaculos desde la izquierda
            if live_rect.bottom == 380:
                surface.blit(surf1, live_rect)
                     
        live_list = [live for live in live_list if live.x > -100] #Para desaparecer los obstaculos cuando pasen
        # el borde izquiero, se hace una list comprehension, que ve si los obstaculos pasaron el borde para borrarlos si salen de la pantalla.
        return live_list #Si hay movimiento retorna una lista
    else:
        return [] #Si no hay movimiento devuelve lista vacia