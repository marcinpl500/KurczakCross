import pygame
import os
import time
import random
pygame.init()
pygame.font.init()
pygame.display.init()
clock = pygame.time.Clock()
disWidth = 960
disHeight = 600
display = pygame.display.set_mode((disWidth,disHeight))
pygame.display.set_caption("KurczakCross")
leftImg = pygame.image.load("LeftSide.png")
rightImg = pygame.image.load("RightSide.png")
kurczakImg = pygame.image.load("Kurczak.png")
auto_szerokosc = 40
auto_wysokosc = 80
kurczak_szerokosc = 35
kurczak_wysokosc = 40

class Obstacle:
     def __init__(self, img, x, y):
          self.image = pygame.image.load(img)
          self.x = x
          self.y = y
          self.rect = self.image.get_rect()

     def draw(self):
          display.blit(self.image, (self.x,self.y))

     def move(self, changeY):
          self.y+= changeY


def RenderText(Text : str, Font : pygame.font.Font):
    textSurf = Font.render(Text, True, (255,255,25))
    return textSurf, textSurf.get_rect()
    
def EntryScreen():
    x = 350
    y = 200
    w = 250
    h = 200
    intro = True
    LoadScreen()
    while intro:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        mousePosition = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()
        pygame.draw.rect(display, "blue", (x, y, w, h))
        btnFont = pygame.font.SysFont("None", 50)
        textSurface, textRectangle = RenderText("PLAY", btnFont)
        textRectangle.center = (x + (w/2), y + (h/2))
        display.blit(textSurface, textRectangle)
        pygame.display.update()
        if x+w > mousePosition[0] > x and y+h > mousePosition[1] > y:
                if mouseClick[0] == 1:
                    Countdown() 
    
def GameOver(Win : bool):
     LoadScreen()
     pygame.display.update()
     overFont = pygame.font.SysFont("None", 115)
     TextSurface, TextRectangle = None, None
     if Win:
           TextSurface, TextRectangle = RenderText("You won", overFont)
     else:
          TextSurface, TextRectangle = RenderText("You lost", overFont)
     TextRectangle.center = (disWidth / 2, disHeight / 2)
     display.blit(TextSurface, TextRectangle)
     pygame.display.update()
     time.sleep(5)
     pygame.quit()

def Kolizja(KurczakArr, SamochodC):
     if KurczakArr[1] > SamochodC.y + auto_wysokosc:
          return False
     elif KurczakArr[1] + kurczak_wysokosc < SamochodC.y:
          return False
     
     if KurczakArr[0] > SamochodC.x + auto_szerokosc:
          return False
     elif KurczakArr[0] + kurczak_szerokosc < SamochodC.x:
          return False
    
     return True

#draws the button and sets the graphics basically 
def LoadScreen():
    display.fill((132,132,130))
    display.blit(leftImg, (0,0))
    display.blit(rightImg, (730,0))
    pygame.draw.line(display, "white", (disWidth/2 - 8, 0), (disWidth/2 - 8, 600), 8)
    pygame.draw.line(display, "white", (disWidth/2 + 8, 0), (disWidth/2 + 8, 600), 8)
    return

def Chicken(x,y):
     display.blit(kurczakImg, (x,y))

#Shows the countdown and fires main loop to start game??
def Countdown():
    cnt = True
    Font = pygame.font.SysFont("None", 140)
    LoadScreen()
    while cnt:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cnt = False
        TextSurface, TextRectangle = RenderText("3", Font)
        TextRectangle.center = (disWidth / 2, disHeight / 2)
        display.blit(TextSurface, TextRectangle)
        pygame.display.update()
        time.sleep(1.5)
        LoadScreen()
        TextSurface, TextRectangle = RenderText("2", Font)
        TextRectangle.center = (disWidth / 2, disHeight / 2)
        display.blit(TextSurface, TextRectangle)
        pygame.display.update()
        time.sleep(1.5)
        LoadScreen()
        TextSurface, TextRectangle = RenderText("1", Font)
        TextRectangle.center = (disWidth / 2, disHeight / 2)
        display.blit(TextSurface, TextRectangle)
        pygame.display.update()
        time.sleep(1.5)
        LoadScreen()
        MainLoop()

currentObstacles:list[Obstacle] = []
def MainLoop():
   
    running = True
    xKurczak = 200
    yKurczak = 300    
    xZmiana = 0
    yZmiana = 0
    while running:
        samochodY = 0
        szybkoscSamochodu = 9
        samochodX = random.randint(251, 699)
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
               running = False
            elif event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LEFT:
                      xZmiana -=2
                 elif event.key == pygame.K_RIGHT:
                      xZmiana =2
                 elif event.key == pygame.K_UP:
                      yZmiana -=2
                 elif event.key == pygame.K_DOWN:
                      yZmiana =2
            elif event.type == pygame.KEYUP:
                 xZmiana = 0
                 yZmiana = 0
            elif event.type == pygame.MOUSEMOTION:
                 continue
        xKurczak+=xZmiana
        yKurczak+=yZmiana
        samochodY -= (szybkoscSamochodu/1.2)
        samochodY += szybkoscSamochodu
        LoadScreen()
        Chicken(xKurczak, yKurczak)
        if len(currentObstacles) < 4:
            imgNmb = random.randint(1,2)
            sIm = None
            if imgNmb == 1:
                sIm = "Car1.png"
            elif imgNmb == 2:
                    sIm = "Car2.png"
            nowySamochod = Obstacle(sIm, samochodX, samochodY)
            currentObstacles.append(nowySamochod)
        for samochod in currentObstacles:
                if(samochod.y >= 600):
                     samochod.y = 0 - auto_wysokosc
                     samochod.x = random.randint(260, 695)
                samochod.move(samochodY)
                samochod.draw()
                if Kolizja([xKurczak, yKurczak], samochod) == True:
                     GameOver(False)
        if xKurczak >= 730:
                    GameOver(True)    
        pygame.display.update()
        clock.tick(60)   
    pygame.quit()  
EntryScreen()