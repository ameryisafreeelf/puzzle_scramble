import pygame

WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

x, y = 100.0, 250.0
size = 50
speed = 200

running = True
while running:

    if x >= WIDTH:
        running = False

    dt = clock.tick(60)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    x += speed * dt

    screen.fill((20, 20, 30))  # wipe the previous frame
    pygame.draw.rect(screen, 
                     (255, 200, 0),
                     (x, y, size, size))
    pygame.display.flip()  # show what you drew

pygame.quit()
