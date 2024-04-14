import pygame

# Omar Initialize pygame
pygame.init()
# Omar setting the width and the height
width=1280
height=720
# Omar Setup the display window with a width & height
screen = pygame.display.set_mode((width, height))
#Omar, creating a dictionary that store the players and their number of turns and thier scores
players = {
  "Omar": [52,820],
  "Alex": [63,760],
  "Wilson": [54,700]
}
#Omar,creating the list thay store the keys to deal with index instaed of string
plylist=list(players.keys())

#Omar,creating a function that represent the result  with specific height called y(y axis pos)

def result(list, dic,i,y,screen): #maximum 7 players at one time
    pygame.draw.line(screen, pygame.Color("white"), (0, y), (width, y), 50)
    add_text(str(i+1),screen,0,y+bodyheight//2-25)
    add_text(str(list[i]),screen,width/4-100,y+bodyheight//2-25)
    add_text(str(dic[list[i]][0]),screen,width/2-100,y+bodyheight//2-25)
    add_text(str(dic[list[i]][1]),screen,width-100,y+bodyheight//2-25)



# Omar,Create a title font with size and type
title_font = pygame.font.SysFont("Arial", 75)

# Omar, Create a surface that hold the title
title_surface = title_font.render('Results', True, (255, 255, 255))
#Omar, getting the width of the title so we can put the title exactly on the middle point of the width screen
widthtitle= title_font.size("Results")[0]
#Create a body text for the results
body_font=pygame.font.SysFont("Arial", 25)
#create a function to add a text into a surface
bodyheight = body_font.size("Body")[1]
#Omar, function to add a text with a specific poistion
def add_text(self,screen,wid,hig):

    body_surface = body_font.render(str(self), True, (0, 0, 0))
    screen.blit(body_surface, (wid, hig))
#to run the loop with constant rate of frame
clock = pygame.time.Clock()
# Run the loop until the user closes the window

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the screen with a brown background color

    screen.fill((102, 61, 14))
    #variable x equal to 0
    x=0

    # Blit the title surface onto the screen
    screen.blit(title_surface, (width//2-widthtitle//2 , height//32))
    # adding subtitles
    add_text("Rank", screen, 0, 125)
    add_text("Name", screen, width//4-100, 125)
    add_text("Number of Turns", screen, width // 2 - 100-body_font.size("Number of Turns")[0]//2, 125)
    add_text("Score", screen, width-100-body_font.size("S")[0],125)
    for i in range(len(plylist)): #for loop to print the result for each player

        result(plylist,players,i,200+x,screen)
        x += 75 #the difference between each result and result is 75
    # Flip the display
    pygame.display.flip()
    clock.tick(60)
# Quit from pygame
pygame.quit()
