import pygame
import random
from pygame import mixer

pygame.init()
mixer.init()


screen = pygame.display.set_mode((800,600))
bg = pygame.image.load("rhythm_bg_image.png").convert()
menu_bg = pygame.image.load("main_menu2.jpg").convert()
start = pygame.image.load("start_button.png").convert()
exit = pygame.image.load("exit_button.png").convert()
life = pygame.image.load("life.png").convert()
blind = pygame.image.load("blind.png").convert()
clock = pygame.time.Clock()
random_list = [6,10,12,16,20,24,26,28,30]
game_paused = False


# Start button containing the image and the mouse position
class Start_button_class():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            #[0] = left most button, [1] = middle most button, [2] = right most button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print("Clicked")
                Main()

        screen.blit(self.image,(self.rect.x,self.rect.y))

# Exit button containing the image and the mouse position
class Exit_button_class():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            #[0] = left most button, [1] = middle most button, [2] = right most button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                pygame.quit()
                quit()
        screen.blit(self.image,(self.rect.x,self.rect.y))

class particles():
    def __init__(self):
        self.particles = []
        self.surface = pygame.image.load('star.png').convert_alpha()
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height
    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x += particle[1]#move y position(pos_y) to upwards(direction = -1)
                particle[0].y += particle[2]
                particle[3] -= 0.2 #shrinking particles
                screen.blit(self.surface,particle[0])
    def add_particles1(self):
        pos_x = 700 - (self.width / 2)
        pos_y = 150 - (self.height / 2)
        direction_x = random.randint(-3,3) 
        direction_y = random.randint(-3,3)
        lifetime = random.randint(4,10)
        particle_rect = pygame.Rect(pos_x,pos_y,self.width,self.height)
        self.particles.append([particle_rect,direction_x,direction_y,lifetime])
    def add_particles2(self):
        pos_x = 100 - (self.width / 2)
        pos_y = 150 - (self.height / 2)
        direction_x = random.randint(-3,3) 
        direction_y = random.randint(-3,3)
        lifetime = random.randint(4,10)
        particle_rect = pygame.Rect(pos_x,pos_y,self.width,self.height)
        self.particles.append([particle_rect,direction_x,direction_y,lifetime])
    def delete_particles(self):
        particles_copy = [particle for particle in self.particles if particle[3] > 0]
        self.particles = particles_copy

start_button = Start_button_class(250,200,start)
exit_button = Exit_button_class(250,350,exit)

particle1 = particles()

# creating the classes for the keys
class Key():
    def __init__ (self,x,y,default_color,color2,key):
        self.x = x
        self.y = y
        self.default_color = default_color
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x,self.y,100,40)
        self.handled = False
# making the list of keys
keys = [
    Key(100,500,(255,255,255),(255,0,0,0.3),pygame.K_a),
    Key(200,500,(255,255,255),(0,220,0,0.3),pygame.K_s),
    Key(300,500,(255,255,255),(0,0,220,0.3),pygame.K_d),
    Key(400,500,(255,255,255),(220,220,0,0.3),pygame.K_f),
    Key(500,500,(255,255,255),(255, 192, 203,0.3),pygame.K_g)
]

    

def paused():
    while True:
        screen.fill("black")
        font = pygame.font.SysFont(None,50)
        text = font.render("Paused!", True,(58, 235, 52))
        screen.blit(text,(300,250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mixer.music.unpause()
                    Main()
        pygame.display.update()

#Main Menu containing start and exit buttons with clicking feature.
def Main_Menu():
    Main_Menu_music("Main_menu_music")
    while True:
        screen.blit(menu_bg,(0,0))
        start_button.draw()
        exit_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

# Main menu music 
def Main_Menu_music(music):
    mixer.music.load(music + ".mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play()

# loading the music and the map file.
def load(map):
    rects = [] 
    mixer.music.load(map + ".mp3")
    mixer.music.play()
    mixer.music.set_volume(0.2)
    f = open(map + ".txt",'r')
    data = f.readlines()
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                rects.append(pygame.Rect(keys[x].rect.centerx - 40,y * -100,80,25))
    return rects

particle_event = pygame.USEREVENT +1
pygame.time.set_timer(particle_event,50)

def Main():
    map_rect = load("Rhythm")
    print(map_rect[5][0])
    score = 0
    life_count = 3
    run = True
    while run:
        screen.blit(bg,(0,0))
        screen.blit(life,(500,0))
        screen.blit(life,(600,0))
        screen.blit(life,(700,0))
        
        #fills black image on the life to indicate the loss of heart when the block is missed.
        
        screen.blit(blind,(700,0))
        screen.blit(blind,(600,0))

        font = pygame.font.SysFont(None,50)
        text = font.render("Score:" + str(score), True,(255, 255, 0))
        screen.blit(text,(20,20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mixer.music.pause()
                    paused()
            if event.type == particle_event:
                particle1.add_particles1()
                particle1.add_particles2()

        k = pygame.key.get_pressed()
        #highlights color to white when it's pressed.  
        for key in keys:
            if k[key.key]:
                pygame.draw.rect(screen,key.default_color,key.rect)
                key.handled = False
            if not k[key.key]:
                pygame.draw.rect(screen,key.color2,key.rect)
                key.handled = True

        #draws long rectangle and falls from (x= 0 , y =99 ) with the speed of y = 1
        #Color variant : red green blue yellow pink
        for rect in map_rect:
            if rect[0] > 99 and rect[0] < 200:
                pygame.draw.rect(screen,(205,92,92),rect)
                if rect[1] > 600:
                    score = 0
                    map_rect.remove(rect)
            if rect[0] > 199 and rect[0] < 300:
                pygame.draw.rect(screen,(0,250,154),rect)
                if rect[1] > 600:
                    score = 0
                    map_rect.remove(rect)
            if rect[0] > 299 and rect[0] < 400:
                pygame.draw.rect(screen,(0,191,255),rect)
                if rect[1] > 600:
                    score = 0
                    map_rect.remove(rect)
            if rect[0] > 399 and rect[0] < 500:
                pygame.draw.rect(screen,(255,228,181),rect)
                if rect[1] > 600:
                    score = 0
                    map_rect.remove(rect)
            if rect[0] > 499 and rect[0] < 600:
                pygame.draw.rect(screen,(255,182,193),rect)
                #poisened block implementation in progress. It merges with the life counting.
                """ if score in range(10):
                    pygame.draw.rect(screen,(0,0,0),rect)
                    #if you click the black falling object, you lose 10 points
                    if key.rect.colliderect(rect) and not key.handled:
                        score -= 2.5
                        map_rect.remove(rect)
                        key.handled = True
                        break """
            rect.y += 2.5
            #when key rectangle makes collision with button pressed, it removes the rectangle.
            for key in keys:
                if key.rect.colliderect(rect) and not key.handled:
                    score += 2
                    map_rect.remove(rect)
                    key.handled = True
                    break

        if score >= 50:
            particle1.emit()
        pygame.display.update()
        clock.tick(240)
Main_Menu()