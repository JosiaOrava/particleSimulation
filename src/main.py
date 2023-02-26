import pygame as pg
pg.init()
WIN_WIDTH, WIN_HEIGHT = 700, 600
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Particle Simulation")
FPS = 30
SAND = (194, 178, 128)
ROCK = (128,132,135)
RECT_SIZE = 7

particles = []
class Particle:
    
    def __init__(self, tuple, type):
        self.x, self.y = tuple
        self.x = self.x // RECT_SIZE
        self.y = self.y // RECT_SIZE
        self.type = type
        self.rect = pg.Rect(self.x,self.y,RECT_SIZE,RECT_SIZE)
    
    def checkSides(self, x, y):
        self.left, self.right = False, False
        for i in particles:
            # Check if left pixel under is empty
            if i.y == y + 1 and i.x == x - 1:
                self.left = True
            # Check if right pixel under is empty
            elif i.y == y + 1 and i.x == x + 1:
                self.right = True
        if self.left:
            if self.right == False:
                return 3
            return 0
        return 2
        
    def checkColl(self, x,y):
        for particle in particles:
            # Check if pixel under is empty
            if particle.y == y + 1 and particle.x == x:
                return Particle.checkSides(self,x,y)
        return 1
      
              
            
        

class Sand(Particle):

    def fall(self):
        if Sand.checkColl(self,self.x, self.y) == 1 and self.y <= WIN_HEIGHT // RECT_SIZE - 2:
            print(self.y) 
            self.y = self.y + 1
        if Sand.checkColl(self, self.x, self.y) == 2 and self.x >= 2:
            self.x = self.x - 1 
        if Sand.checkColl(self, self.x, self.y) == 3 and self.x <= WIN_WIDTH // RECT_SIZE - 3:
            self.x = self.x + 1
class Rock(Particle):
    pass

def main():
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        print(round(clock.get_fps(), 2))
        WIN.fill(0)
        pg.draw.rect(WIN, ROCK, (0, 0, WIN_WIDTH, WIN_HEIGHT), 5)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        mouseStatus = pg.mouse.get_pressed()
        if mouseStatus[0]:
            particles.append(Sand(pg.mouse.get_pos(), "sand"))
        if mouseStatus[2]:
            particles.append(Rock(pg.mouse.get_pos(), "rock"))
        for particle in particles:
            if particle.type == "sand":
                pg.draw.rect(WIN, SAND, (particle.x*RECT_SIZE, particle.y*RECT_SIZE,RECT_SIZE,RECT_SIZE))
                particle.fall()
            if particle.type == "rock":
                pg.draw.rect(WIN, ROCK, (particle.x*RECT_SIZE, particle.y*RECT_SIZE,RECT_SIZE,RECT_SIZE))
        
        pg.display.update()
    pg.quit()



if __name__ == "__main__":
    main()