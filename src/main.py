import pygame as pg
import random
pg.init()
WIN_WIDTH, WIN_HEIGHT = 700, 600
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Particle Simulation")
FPS = 30
SAND = (194, 178, 128)
ROCK = (128,132,135)
WATER = (0, 255, 255)
RECT_SIZE = 10

particles = []
class Particle:
    
    def __init__(self, tuple, type):
        self.x, self.y = tuple
        self.x = self.x // RECT_SIZE
        self.y = self.y // RECT_SIZE
        self.type = type
        self.rect = pg.Rect(self.x,self.y,RECT_SIZE,RECT_SIZE)
    
    def randomSide(left,right):
        side = random.randint(0,1)
        if side == 0:
            if left == False:
                return 2
            elif right == False:
                return 3
            return 0
        else:
            if right == False:
                return 3
            elif left == False:
                return 2
            return 0

    def checkSides(self, x, y):
        self.left, self.right = False, False
        for i in particles:
            # Check if left pixel under is empty
            if i.y == y + 1 and i.x == x - 1:
                self.left = True
            # Check if right pixel under is empty
            elif i.y == y + 1 and i.x == x + 1:
                self.right = True
        return Particle.randomSide(self.left, self.right)
        
    def checkColl(self, x,y):
        for particle in particles:
            # Check if pixel under is empty
            if particle.y == y + 1 and particle.x == x:
                return Particle.checkSides(self,x,y)
        return 1

    def fall(self):
        if Particle.checkColl(self,self.x, self.y) == 1 and self.y <= WIN_HEIGHT // RECT_SIZE - 2:
            self.y = self.y + 1
        if Particle.checkColl(self, self.x, self.y) == 2 and self.x >= 2:
            self.x = self.x - 1 
        if Particle.checkColl(self, self.x, self.y) == 3 and self.x <= WIN_WIDTH // RECT_SIZE - 3:
            self.x = self.x + 1  
              
            
        

class Sand(Particle):
    pass
    

class Water(Particle):

    
    def randomSide(left,right,leftUnder,rightUnder):
        side = random.randint(0,1)
        if side == 0:
            if left == False:
                return 5
            elif right == False:
                return 4
            elif leftUnder == False:
                return 2
            elif rightUnder == False:
                return 3
            return 0
        else:
            if left == False:
                return 5
            elif right == False:
                return 4
            elif rightUnder == False:
                return 3
            elif leftUnder == False:
                return 2
            return 0

    def checkSides(self, x, y):
        self.left, self.right, self.leftUnder, self.rightUnder = False, False, False, False
        for i in particles:
            # Check if left pixel under is empty
            if i.y == y + 1 and i.x == x - 1:
                self.leftUnder = True
            # Check if right pixel under is empty
            elif i.y == y + 1 and i.x == x + 1:
                self.rightUnder = True
            # Check if left pixel is empty 
            elif i.y == y and i.x == x - 1:
                print("left true")
                self.left = True
            # Check if right pixel is empty
            elif i.y == y and i.x == x + 1:
                print("right true")
                self.right = True
        return Water.randomSide(self.left, self.right, self.leftUnder, self.rightUnder)

    def fall(self):
        if Water.checkColl(self, self.x, self.y) == 1 and self.y <= WIN_HEIGHT // RECT_SIZE - 2:
            self.y = self.y + 1
        if Water.checkColl(self, self.x, self.y) == 2 and self.x >= 2:
            self.x = self.x - 1 
        if Water.checkColl(self, self.x, self.y) == 3 and self.x <= WIN_WIDTH // RECT_SIZE - 3:
            self.x = self.x + 1
        if Water.checkColl(self, self.x, self.y) == 4 and self.x >= 2:
            print("left")
            self.x = self.x - 1
        if Water.checkColl(self, self.x, self.y) == 5 and self.x <= WIN_WIDTH // RECT_SIZE - 3:
            print("right")
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
        if mouseStatus[1]:
            particles.append(Water(pg.mouse.get_pos(), "water"))
        if mouseStatus[2]:
            particles.append(Rock(pg.mouse.get_pos(), "rock"))
        for particle in particles:
            if particle.type == "sand":
                pg.draw.rect(WIN, SAND, (particle.x*RECT_SIZE, particle.y*RECT_SIZE,RECT_SIZE,RECT_SIZE))
                particle.fall()
            if particle.type == "rock":
                pg.draw.rect(WIN, ROCK, (particle.x*RECT_SIZE, particle.y*RECT_SIZE,RECT_SIZE,RECT_SIZE))
            if particle.type == "water":
                pg.draw.rect(WIN, WATER, (particle.x*RECT_SIZE, particle.y*RECT_SIZE,RECT_SIZE,RECT_SIZE))
                particle.fall()
        
        pg.display.update()
    pg.quit()



if __name__ == "__main__":
    main()