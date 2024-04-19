import pygame
import random
pygame.init()

window = pygame.display.set_mode([640, 480])
doQuit = False

x = random.randint(0, 2) * 16
y = random.randint(0, 1) * 16
print(x, y)

cropped = pygame.Surface((16, 16))
cropped.blit(pygame.image.load("assets/dirt.png"), (0, 0), (x, y, 16, 16))
cropped = pygame.transform.scale(cropped, (64, 64))

# spritesheet = pygame.image.load("assets/dirt.png")
# cropped = pygame.transform.scale(spritesheet.subsurface((x, y, 16, 16)), (64, 64))

while not doQuit:
   window.blit(cropped, (0, 0))
   pygame.display.flip()
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           doQuit = True

pygame.quit()