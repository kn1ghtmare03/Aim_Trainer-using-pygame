import math
import random
import time
import pygame
pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT = 800,600
WIN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("AIM(bot) TRAINING")

TARGET_INCREMENT =  400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0,25,40)

LIVES = 3 
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)



class Target:
    MAXSIZE = 30
    GROWTHRATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0 
        self.grow = True

    def update_size(self):
        if self.size + self.GROWTHRATE >= self.MAXSIZE:
            self.grow = False
        if self.grow:
            self.size += self.GROWTHRATE
        else:
            self.size -= self.GROWTHRATE
    
    def draw_target(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.size)
        pygame.draw.circle(win,self.SECOND_COLOR,(self.x,self.y),self.size*0.8)
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.size*0.6)
        pygame.draw.circle(win,self.SECOND_COLOR,(self.x,self.y),self.size*0.4)

    def collide(self,x,y):
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance <= self.size 


def draw(win,targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw_target(win)
    


def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000)/100)
    seconds = int(round(secs % 60 ,1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}:{milli}"


def draw_top_bar(win, elapsed_time,targets_pressed, misses):
    pygame.draw.rect(win, "grey" , (0,0 , SCREEN_WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}",1,"black")
    speed = round(targets_pressed/ elapsed_time ,1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s",1,"black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}",1,"black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}",1,"black")

    win.blit(time_label , (5,5))
    win.blit(speed_label,(200,5))
    win.blit(hits_label,(450,5))
    win.blit(lives_label,(650,5))

def end_screen(win , elapsed_time , targets_pressed , clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}",1,"white")
    speed = round(targets_pressed/ elapsed_time ,1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s",1,"white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}",1,"white")
    try:
        accuracy = round(targets_pressed / clicks * 100, 1)
    except ZeroDivisionError as e:
        accuracy = 0.0
    accuracy_label = LABEL_FONT.render(f"Accuracy :{accuracy}",1,"white")
    win.blit(time_label , (get_middle(time_label),100))
    win.blit(speed_label,(get_middle(speed_label),200))
    win.blit(hits_label,(get_middle(hits_label),300))
    win.blit(accuracy_label,(get_middle(accuracy_label),400))

    pygame.display.update()
    runner = True
    while runner:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or  event.type ==  pygame.KEYDOWN:
                quit()


def get_middle(surface):
    return SCREEN_WIDTH /2 - surface.get_width()/2



def main():
    runner = True
    targets = []
    clock = pygame.time.Clock()
    pygame.time.set_timer(TARGET_EVENT,TARGET_INCREMENT)
    targets_pressed = 0
    clicks = 0
    misses = 0  
    start_time = time.time()

    while runner:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
                break
                
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING,SCREEN_WIDTH-TARGET_PADDING)
                y = random.randint(TARGET_PADDING +TOP_BAR_HEIGHT,SCREEN_HEIGHT-TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        
        for target in targets:
            target.update_size()
        
            if target.size <= 0:
                targets.remove(target)
                misses += 1
            
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
        if misses >= LIVES:
            end_screen(WIN,elapsed_time,targets_pressed,clicks)

        
        draw(WIN, targets)
        draw_top_bar(WIN,elapsed_time,targets_pressed,misses)
        pygame.display.update() 

    pygame.quit()

if __name__ == "__main__":
    main()

