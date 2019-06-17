import pygame

pygame.init()

SCREENWIDTH = 800
SCREENHEIGHT = 600

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

DISPLAY = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Connect 4')
clock = pygame.time.Clock()


crashed = False

while not crashed:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            crashed = True
            
        print(event)
        
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
quit()