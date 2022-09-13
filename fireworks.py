import pygame
import time
import math
import random

pygame.init()
WIN=pygame.display.set_mode((700,700))

Colors=[(0,0,255),(255,0,0),(255,255,0),(255,255,255),(255,0,0),(255,128,0),(51,0,102),(204,204,255),(255,255,0),(128,0,128),(255,0,255),(192,192,192),(255,255,255,255),(255,255,0)]

class Projectile:
    VEL=1.2
    def __init__(self,x,y,angle):
        self.x=x
        self.y=y 
        self.angle=angle
        self.color=Colors[random.randint(0,len(Colors)-1)]
    
    def move(self):
        self.x+=math.sin(self.angle)*self.VEL
        self.y+=math.cos(self.angle)*self.VEL
    
    def draw(self):
        pygame.draw.rect(WIN,self.color,(self.x,self.y,3,3))

    
class Projectile_Two:
    VEL=1
    def __init__(self,x,y,direction):
        self.x=x
        self.y=y 
        self.direction=direction 
        self.fired=False 
        self.color=Colors[random.randint(0,len(Colors)-1)]

    def move(self):
        if self.direction=="left":
            self.x-=self.VEL 
        elif self.direction=='up':
            self.y-=self.VEL 
        elif self.direction=='right':
            self.x+=self.VEL 
        else:
            self.y+=self.VEL 
    
    def draw(self):
        pygame.draw.circle(WIN,self.color,(self.x,self.y),3)


class Firework:
    RADIUS=6
    VEL=3
    MAX_HEIGHT=400
    MIN_HEIGHT=100 

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.exploded=False 
        self.color=Colors[random.randint(0,len(Colors)-1)]
        self.explode_height=random.randint(self.MIN_HEIGHT,self.MAX_HEIGHT)
        self.projectiles_list=[]
        self.num_projectiles=random.randint(50,200)
        self.angle_increment=360//self.num_projectiles
        self.cur_angle=0
        self.fire_work_choice=random.randint(1,4)
        self.delay=0
        self.second_layer=[]
    
    def launch(self):
        if self.y>self.explode_height and not self.exploded:
            self.y-=self.VEL
        else:
            self.exploded=True
    
    def reset(self):
        self.y=random.randint(680,1200)
        self.color=Colors[random.randint(0,len(Colors)-1)]
        self.explode_height=random.randint(self.MIN_HEIGHT,self.MAX_HEIGHT)
        self.fire_work_choice=random.randint(1,4)

    def draw(self):
        if self.y>self.explode_height:
            pygame.draw.circle(WIN,self.color,(self.x,self.y),self.RADIUS)
        
    def explode(self):

        if self.exploded:
            if not len(self.projectiles_list):
                if self.fire_work_choice<4:
                    for i in range(self.num_projectiles):
                        new_projectile=Projectile(self.x,self.y,math.radians(self.cur_angle))
                        self.projectiles_list.append(new_projectile)
                        self.cur_angle+=self.angle_increment
                else:
                    projectile_one=Projectile_Two(self.x,self.y,"up")
                    projectile_two=Projectile_Two(self.x,self.y,"down")
                    projectile_three=Projectile_Two(self.x,self.y,"left")
                    projectile_four=Projectile_Two(self.x,self.y,"right")
                    projectile_five=Projectile_Two(self.x,self.y+12,"up")
                    projectile_six=Projectile_Two(self.x,self.y-12,"down")
                    projectile_seven=Projectile_Two(self.x+12,self.y,"left")
                    projectile_eight=Projectile_Two(self.x-12,self.y,"right")
                    self.projectiles_list=[projectile_one,projectile_two,projectile_three,projectile_four]
                    self.second_layer=[projectile_five,projectile_six,projectile_seven,projectile_eight]

                        
            else:
                for i in range(len(self.projectiles_list)):
                    projectile=self.projectiles_list[i]
                    if self.get_radius(projectile.x,projectile.y,self.x,self.y)>200:
                        self.exploded=False
                        self.reset_after_explode()
                        break
                    projectile.draw()
                    projectile.move()

                    if len(self.second_layer):
                        projectile_two=self.second_layer[i]
                        projectile_two.color=projectile.color
                        if self.get_radius(projectile_two.x,projectile_two.y,self.x,self.y)>150:
                            self.exploded=False 
                            self.reset_after_explode()
                            break
                        projectile_two.draw()
                        projectile_two.move()
                    self.delay+=1


    def reset_after_explode(self):
        self.exploded=False
        self.projectiles_list=[]
        self.second_layer=[]
        self.num_projectiles=random.randint(60,150)
        self.angle_increment=360//self.num_projectiles
        self.cur_angle=0
        self.delay=0
        self.reset()
    
    def get_radius(self,proj_x,proj_y,center_x,center_y):
        dist_x=abs(proj_x-center_x)
        dist_y=abs(proj_y-center_y)
        return math.sqrt(dist_x**2+dist_y**2)


class Launcher:
    WIDTH=20
    HEIGHT=30
    COLOR=(178,190,181)

    def __init__(self,x):
        self.x=x
        self.firework=None
    
    def draw(self):
        pygame.draw.rect(WIN,self.COLOR,(self.x,700-self.HEIGHT,self.WIDTH,self.HEIGHT))

def main():
    run=True 
    clock=pygame.time.Clock()
    launcher=Launcher(50)
    firework=Firework(launcher.x+launcher.WIDTH//2,random.randint(680,900))
    launcher_two=Launcher(150)
    firework_two=Firework(launcher_two.x+launcher_two.WIDTH//2,random.randint(680,900))
    launcher_three=Launcher(300)
    firework_three=Firework(launcher_three.x+launcher_three.WIDTH//2,random.randint(680,900))
    launcher_four=Launcher(400)
    firework_four=Firework(launcher_four.x+launcher_four.WIDTH//2,random.randint(680,900))
    launcher_five=Launcher(520)
    firework_five=Firework(launcher_five.x+launcher_five.WIDTH//2,random.randint(680,900))
    launcher_six=Launcher(620)
    firework_six=Firework(launcher_six.x+launcher_six.WIDTH//2,random.randint(680,900))
    pairs=[(launcher,firework),(launcher_two,firework_two),(launcher_three,firework_three),(launcher_four,firework_four),(launcher_five,firework_five),(launcher_six,firework_six)]
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False 
        WIN.fill((0,0,0))
        for pair in pairs:
            launcher,firework=pair
            firework.launch()
            firework.draw()
            launcher.draw()
            firework.explode()
            

        pygame.display.update()
    
    pygame.quit()



if __name__=="__main__":
    main()
