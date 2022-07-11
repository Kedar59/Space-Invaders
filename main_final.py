import sys
import pygame
import time
import random
import mysql.connector as sql
m=sql.connect(host="localhost",user="root",password="MosH@1211")
cursor=m.cursor()
pygame.font.init()
width=1300
height=720
win=pygame.display.set_mode((1300,720))
pygame.display.set_caption("SPACE INVADERS")
red_ship=pygame.image.load("ship_red.png")
yellow_ship=pygame.image.load("ship_yellow.png")
blue_ship=pygame.image.load("ship_blue.png")
green_ship=pygame.image.load("ship_green.png")
red_laser=pygame.image.load("laser_red.png")
yellow_laser=pygame.image.load("laser_yellow.png")
green_laser=pygame.image.load("laser_green.png")
blue_laser=pygame.image.load("laser_blue.png")
bck=pygame.transform.scale(pygame.image.load("bck.png"),(width,height))
invulnerability=0

display_width = 1300
display_height = 720
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
blue=(0,255,255)
bright_blue=(0,0,255)
green=(0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

clock = pygame.time.Clock()
def terminate():
    pygame.quit()
    sys.exit()

def crash(curr_score):    
    cursor.execute("use game")
    d='''select * from score'''
    cursor.execute(d)
    p=cursor.fetchall()
    for i in p:
        if (text==i[0] and i[1]<curr_score):
            cursor.execute("update score set highscore={} where name='{}'".format(curr_score,text))
            m.commit()
    cursor.execute('select MAX(highscore) AS m_score from score')
    res=cursor.fetchall()
    for i in res:
        m_score=i[0]
    
    cursor.execute(d)
    p=cursor.fetchall()
    for i in p:
        if (text==i[0]):
            pb_score=i[1]
    
   
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.fill(blue)
        button("Retry",600,450,200,60,green,bright_green,main)
        button("Quit !!",600,550,200,60,red,bright_red,terminate)
        if(curr_score<pb_score):
            largeText = pygame.font.Font('freesansbold.ttf',40)
            TextSurf, TextRect = text_objects("{}'s personal best was:{} and current score is {}".format(text,pb_score,curr_score), largeText)
            TextRect.center = ((display_width/2),(display_height/4))
            win.blit(TextSurf, TextRect)
        else:
            largeText = pygame.font.Font('freesansbold.ttf',40)
            TextSurf, TextRect = text_objects("{}'s new personal best is:{}".format(text,pb_score), largeText)
            TextRect.center = ((display_width/2),(display_height/4))
            win.blit(TextSurf, TextRect)
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = text_objects("Highest score is {}".format(m_score), largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        win.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(300)
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(win, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    win.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    win.blit(TextSurf, TextRect)
    pygame.display.update()

def button_text(text,cordinate_x,cordinate_y):
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects(text, smallText)
        textRect.center = ( cordinate_x,cordinate_y )
        win.blit(textSurf, textRect)

def login():
    largeText1 = pygame.font.Font('freesansbold.ttf',20)
    intro=True
    global text
    text=""
    k=0
    global password
    password=""
    while intro:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    k+=1
                if k==0:
                    if event.key==pygame.K_BACKSPACE:
                        text=text[:-1]
                    else:
                        text+=event.unicode
                else:
                    if event.key==pygame.K_BACKSPACE:
                        password=password[:-1]
                    else:
                        password+=event.unicode
        win.fill(blue)
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Welcome back Commander !!", largeText)
        TextRect.center = ((display_width/2),(display_height/5))
        win.blit(TextSurf, TextRect)
        
        text_surface=largeText1.render("Enter username: ",True,black)
        win.blit(text_surface,(60,250))
        text_surface=largeText1.render(text,True,red)
        win.blit(text_surface,(250,250))
        

        text_surface=largeText1.render("Enter password: ",True,black)
        win.blit(text_surface,(60,300))
        text_surface=largeText1.render(password,True,red)
        win.blit(text_surface,(240,300))

        button("BEGIN BATTLE !!",600,550,200,60,green,bright_green,login2)

        pygame.display.update()
        clock.tick(300)
def login2():
    cursor.execute("use game")
    d='''select * from score'''
    cursor.execute(d)
    p=cursor.fetchall()
    l_username=[]
    for i in p:
        l_username.append(i[0])
    if text not in l_username:
        largeText1 = pygame.font.Font('freesansbold.ttf',40)
        text_surface=largeText1.render("Username doesnt exist!!",True,red)
        win.blit(text_surface,(420,450))
        pygame.display.update()
        time.sleep(2)
        login()
    
    for i in p:
        if(i[0]==text and i[2]!=password):
            largeText1 = pygame.font.Font('freesansbold.ttf',40)
            text_surface=largeText1.render("WRONG PASSWORD TRY AGAIN !!",True,red)
            win.blit(text_surface,(420,450))
            pygame.display.update()
            time.sleep(2)
            login()


        if(i[0]==text and i[2]==password):
            main()
def Sign_up():

    largeText1 = pygame.font.Font('freesansbold.ttf',20)
    intro=True
    global text
    text=""
    k=0
    global password
    password=""
    while intro:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    k+=1
                if k==0:
                    if event.key==pygame.K_BACKSPACE:
                        text=text[:-1]
                    else:
                        text+=event.unicode
                else:
                    if event.key==pygame.K_BACKSPACE:
                        password=password[:-1]
                    else:
                        password+=event.unicode
        win.fill(blue)   
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Welcome Commander !!", largeText)
        TextRect.center = ((display_width/2),(display_height/5))
        win.blit(TextSurf, TextRect)
        
        text_surface=largeText1.render("Enter username: ",True,black)
        win.blit(text_surface,(60,250))
        text_surface=largeText1.render(text,True,red)
        win.blit(text_surface,(250,250))
        

        text_surface=largeText1.render("Enter password: ",True,black)
        win.blit(text_surface,(60,300))
        text_surface=largeText1.render(password,True,red)
        win.blit(text_surface,(240,300))

        button("BEGIN BATTLE !!",600,550,200,60,green,bright_green,sign_up2)
        pygame.display.update()
        clock.tick(300)
    
def sign_up2():
    try:
        c="CREATE DATABASE IF NOT EXISTS game"
        cursor.execute(c)
        cursor.execute("use game")
        cursor.execute("create table if not exists score(name char(20) unique,highscore integer,password char(20))")
        cursor.execute("insert into score values('{}',0,'{}')".format(text,password))
        m.commit()
    except:
        largeText1 = pygame.font.Font('freesansbold.ttf',40)
        text_surface=largeText1.render("Name already exist!!",True,red)
        win.blit(text_surface,(480,450))
        pygame.display.update()
        time.sleep(2)
        Sign_up()
    main()
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        win.fill(blue)
        largeText = pygame.font.Font('freesansbold.ttf',80)
        TextSurf, TextRect = text_objects("SPACE INVADERS", largeText)
        TextRect.center = ((display_width/2),(display_height/4))
        win.blit(TextSurf, TextRect)
        
        pygame.draw.rect(win, green,(300,450,100,50))
        pygame.draw.rect(win, red,(950,450,100,50))
        button("LOGIN",300,450,100,50,green,bright_green,login)
        button("SIGN UP",950,450,100,50,red,bright_red,Sign_up) 
        pygame.display.update()
        clock.tick(300)
def collide(obj1,obj2):
    offset_x=(obj2.x-obj1.x)
    offset_y=(obj2.y-obj1.y)
    return(obj1.mask.overlap(obj2.mask,(offset_x,offset_y))!=None)
class ship:
    COOLDOWN = 30  

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down= 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.Collide(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down>= self.COOLDOWN:
            self.cool_down= 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def shoot(self):
        if self.cool_down== 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down = 1

        
class Enemy(ship):
    colour={"red":(red_ship,red_laser),"blue":(blue_ship,blue_laser),"green":(green_ship,green_laser)}
    def __init__(self, x, y,colour, health=100):
        super().__init__(x, y, health)
        self.ship_img,self.laser_img=self.colour[colour]
        self.mask=pygame.mask.from_surface(self.ship_img)
    def move(self,vel):
        self.y+=vel
    def shoot(self):
        if self.cool_down== 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down=1

class player(ship):
   
    def __init__(self, x, y, health=100,score=0,k_count=0):
        super().__init__(x, y, health)
        self.ship_img = yellow_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score=score
        self.k_count=k_count
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.Collide(obj):
                        objs.remove(obj)
                        self.k_count+=1
                        self.score+=5 
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def health_bar(self):
        pygame.draw.rect(win,(255,0,0),(self.x,self.y+yellow_ship.get_height()+10,yellow_ship.get_width(),10))
        pygame.draw.rect(win,(0,255,0),(self.x,self.y+yellow_ship.get_height()+10,yellow_ship.get_width()*(self.health/100),10))
    
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.y += vel
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    def Collide(self, obj):
        return collide(self, obj)

def main():
   
    laser_vel=4
    lost=False
    wavelength=5
    enemies=[]
    level=0
    lives=10
    run=True
    vel=5
    enemy_vel=2
    fps=300
    clock=pygame.time.Clock()
    font=pygame.font.SysFont("comicsans",30)
    main_ship=player(600,585)
   
    def unpause():
        global pause
        pause=False
    def paused():
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
            win.fill(blue)
            largeText = pygame.font.Font('freesansbold.ttf',80)
            TextSurf, TextRect = text_objects("PAUSED", largeText)
            TextRect.center = ((display_width/2),(display_height/4))
            win.blit(TextSurf, TextRect)
        
            pygame.draw.rect(win, green,(300,450,100,50))
            pygame.draw.rect(win, red,(950,450,100,50))
            button("Resume",300,450,100,50,green,bright_green,unpause)
            button("Quit",950,450,100,50,red,bright_red,terminate) 
            pygame.display.update()
            clock.tick(300)
    def draw():
        global invulnerability
        
        win.blit(bck,(0,0))
        lives_label=font.render("Lives: {}".format(lives),1,(255,255,255))
        level_label=font.render("Level: {}".format(level),1,(255,255,255))
        score_label=font.render("Score: {}".format(main_ship.score),1,(255,255,255))
        kill_counter_label=font.render("Kill Count: {}".format(main_ship.k_count),1,(255,255,255))
        win.blit(lives_label,(5,5))
        win.blit(level_label,(width-level_label.get_width()-5,5))
        win.blit(score_label,(width*0.45,5))
        win.blit(kill_counter_label,(5,height-kill_counter_label.get_height()))
        for enemy in enemies:
            enemy.draw(win)
        
        if(invulnerability<60*9):
            main_ship.health=100
            invulnerability+=1
            pygame.draw.circle(win, (0, 255, 0),[main_ship.x+52, main_ship.y+60], yellow_ship.get_width()-10, 3)
        
        main_ship.health_bar()
        main_ship.draw(win)
        if lost==True:
            lost_label=font.render("You Lost!!",1,(255,255,255))
            win.blit(lost_label,(width/2-lost_label.get_width()/2,350))
            pygame.display.update()
            time.sleep(3)
            crash(main_ship.score)
        pygame.display.update()

    while run:
        global pause
        clock.tick(fps)
        
        if(lives<=0 or main_ship.health<=0):
           lost = True
        draw()
        if(len(enemies)==0):
            level+=1
            wavelength+=5
            for i in range(wavelength):
                enemy=Enemy(random.randrange(10,width-100),random.randrange(-1000,-500),random.choice(["red","blue","green"]))
                enemies.append(enemy)
            if(level>1):
                main_ship.score+=50
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and main_ship.x-vel>0:   
            main_ship.x-=vel
        if keys[pygame.K_s] and main_ship.y+vel+yellow_ship.get_height()+40<height:
            main_ship.y+=vel
        if(keys[pygame.K_w] and main_ship.y-vel>0):
            main_ship.y-=vel
        if(keys[pygame.K_d]) and main_ship.x+vel+yellow_ship.get_width()<width:
            main_ship.x+=vel
        if keys[pygame.K_SPACE]:
            main_ship.shoot()
        if keys[pygame.K_p]:
            pause=True
            paused()
        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,main_ship)
            if(random.randrange(0,1*120)==1):
                enemy.shoot()
            if(collide(main_ship,enemy)):
                enemies.remove(enemy)
                main_ship.health-=10
                
            elif(enemy.y+enemy.ship_img.get_height()>height):
                lives-=1
                enemies.remove(enemy)
        main_ship.move_lasers(-laser_vel, enemies)
        pygame.display.update()
        clock.tick(300)      

game_intro()
