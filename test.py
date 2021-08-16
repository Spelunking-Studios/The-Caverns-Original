import pygame #game inported, all varibles in higher case

pygame.init()

BACKGROUND_COLOUR = 255, 255, 255 #bg varible

WIDTH, HEIGHT = 900, 500 #dimensions varible

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) #telling the program to make a new window with that varible

pygame.display.set_caption("Walking") #window name

SCREEN.fill(BACKGROUND_COLOUR) #telling the program to change to the bg varible

FPS = 24 #pretty self explanitory

VEL = 5 #for movement

def main():

clock = pygame.time.Clock() #time or something idk

run = True

x, y = 250, 450

CHAR = pygame.Surface((25, 25))#pygame.image.load("square.png") #Just load the image once here

while run:

pygame.time.delay(100) #wait function from scratch

SCREEN.fill(BACKGROUND_COLOUR)

def character():

SCREEN.blit(CHAR, (x, y)) #position (from top left corner)

character()

for event in pygame.event.get():

if event.type == pygame.QUIT: #so you can actually close it

run = False

keys_pressed = pygame.key.get_pressed()

if keys_pressed[pygame.K_a]:

x -= VEL

print(f"left: {x}") #print commands to check if movenent works

pygame.display.update()

pygame.quit()

if __name__ == "__main__": #Runs main

main()