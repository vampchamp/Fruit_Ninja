import random
import pygame as pg
pg.init()
#making the screen and naming the game
Screen_width = 800
Screen_length = 600
screen = pg.display.set_mode((Screen_width,Screen_length))
pg.display.set_caption("Fruit Ninja")
#organizing initialized variables
run = True
hold_mouse = False
previous_mouse = None
points = 0
fruits = []
trail= []
particles = []
max_trail = 10
score = 0
frenzy_mode = False
rush_mode = False
game_start = pg.mixer.Sound("assets\sounds\start.mp3")
spawn_fruit = pg.USEREVENT + 1
if not frenzy_mode:
    pg.time.set_timer(spawn_fruit,2000)
else:
    pg.time.set_timer(spawn_fruit,1000)
decrement_time = pg.USEREVENT +2
pg.time.set_timer(decrement_time,1000)
clock = pg.time.Clock()
background = pg.image.load("assets\images\\background2.jpg").convert()
background = pg.transform.scale(background,(Screen_width,Screen_length))
timer  =  60
high_score = 0
game_over = False
#adding background music
pg.mixer.music.load("assets\sounds\\bgmusic.mp3")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1)
#Using functions as per the requirements
def scale_image(image, width,height):
    image = pg.transform.scale(image,(width,height))
    return image

def fruit_spawn():
    fruit_x = random.randrange(100,650)
    final_x = fruit_x*0.01
    fruit_y = 600
    velocity = random.randrange(20,25)
    fruit_num = random.randint(1,4)
    match fruit_num:
        case 1:
            fruit_type = pg.image.load("assets\images\\banana2.png").convert_alpha()
        case 2:
            fruit_type = pg.image.load("assets\images\\apple.png").convert_alpha()
        case 3 :
            fruit_type = pg.image.load("assets\images\\pineapple.png").convert_alpha()
        case 4:
            fruit_type = pg.image.load("assets\images\\bomb.png").convert_alpha()
    if fruit_num != 4:
        fruit_type = scale_image(fruit_type,100,100)
        bomb = False
    else:
        fruit_type = scale_image(fruit_type,75,100)
        bomb = True
    if fruit_x<375:
        go_right = True
    else:
        go_right = False
    fruits.append([fruit_x,fruit_y,velocity,fruit_type,go_right,final_x,bomb])
    
def leave_trail(screen, trail):
    for i in range(len(trail)-1):
        pg.draw.line(screen,"white",trail[i],trail[i+1],3)
    screen.blit(screen,(0,0))

def score_up(score):
    score+=10
    return score



class particle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xVel = random.randrange(-3,3)*5
        self.yVel = random.randrange(-10,10)*5
        self.timeout = 20
    def scatter(self):
        self.timeout -= 1
        if self.timeout>0:
            self.x+=self.xVel
            self.y+=self.yVel
    def show(self,window):
        pg.draw.circle(window,"red",(self.x,self.y),5)
#can we consider this multiple functions?

def create_particles(fruitx,fruity):
    for i in range(20):
        x = particle(fruitx,fruity)
        particles.append(x)  


while run:
    #screen.fill('black') unnecesary for now
    screen.blit(background,(0,0))
    mouse_position = pg.mouse.get_pos()
    mouse_x,mouse_y = pg.mouse.get_pos()
    font = pg.font.Font("F:\Cloud\OneDrive\Desktop\Fruity\\assets\Fonts\\OJ.otf",50)
    # screen.blit(cursor,(mouse_x -cursor.get_width()//2,mouse_y-cursor.get_height()//2)) non original code
    for fruit in fruits[:]: #shallow copy of list
        if not fruit[6]:
            fruit_hitbox =  pg.Rect(fruit[0],fruit[1],90,90)
        else:
            fruit_hitbox =  pg.Rect(fruit[0],fruit[1],75,75)
        fruit[1] -=fruit[2]
        fruit[2] -= 0.5
        if fruit[4]:
            angle = (-pg.time.get_ticks() / 10) % 360  #pg.time.get_ticks()?
        else:
            angle = (pg.time.get_ticks() / 10) % 360
        fruit_rotated = pg.transform.rotate(fruit[3],angle)
        fruit_instance_new = fruit_rotated.get_rect(center = fruit_hitbox.center)
        screen.blit(fruit_rotated,fruit_instance_new.topleft)
        if fruit[1]>= 600:
            fruits.remove(fruit)
        match round(fruit[5]):
            case 1:
                fruit[0]+=6
            case 2:
                fruit[0]+=5
            case 3:
                fruit[0]+=2.5
            case 4:
                fruit[0]-=6
            case 5:
                fruit[0]-=5
            case 6:
                fruit[0]-=2.5
        if hold_mouse and previous_mouse:
            if fruit_hitbox.clipline(previous_mouse,mouse_position):
                if not fruit[6]:
                    slice = pg.mixer.Sound("assets\sounds\steel sound.mp3")
                    create_particles(fruit[0],fruit[1])
                    pg.mixer.Sound.set_volume(slice,0.2)
                    pg.mixer.Sound.play(slice) 
                    print("fruit sliced!")
                    score = score_up(score)
                else:
                    damage = pg.mixer.Sound("assets\sounds\damage.mp3")
                    pg.mixer.Sound.set_volume(damage,0.2)
                    pg.mixer.Sound.play(damage)
                    game_over = True
                    timer = 0
                fruits.remove(fruit)
    if score>high_score:
        high_score = score
    time = font.render(f"{timer}", 1, "black")
    screen.blit(time,(700,0))
    text = font.render(f"score: {score}",1,"black")
    screen.blit(text,(250,0))
    previous_mouse = mouse_position if hold_mouse else None
    for Obj in particles[:]:
        Obj.scatter()
        Obj.show(screen)
        if Obj.timeout == 0:
            particles.remove(Obj)
    if hold_mouse:
        trail.append(mouse_position)
        if len(trail)>7:
            trail.pop(0)
    else:
        trail = []
    leave_trail(screen,trail)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        if event.type == pg.MOUSEBUTTONDOWN:
            hold_mouse = True
        if event.type == pg.MOUSEBUTTONUP:
            hold_mouse = False
        if event.type == spawn_fruit and not game_over:
            spawn_amount = random.randint(1,3)
            for i in range(spawn_amount):
                fruit_spawn()
        if event.type == decrement_time:
            if not game_over:
                timer-=1
        if event.type == pg.KEYDOWN and game_over:
            if event.key == pg.K_SPACE:
                pg.mixer.Sound.play(game_start) 
                game_over = False
                score = 0
                timer = 60
                frenzy_mode = False
                rush_mode = False
                pg.time.set_timer(spawn_fruit,2000)
    if timer == 0:
        game_over = True
        fruits.clear()
    if timer<=10 and not timer<=0 and not frenzy_mode:
        frenzy_mode = True
        pg.time.set_timer(spawn_fruit, 500)
    if timer<=30 and timer>10 and not rush_mode:
        rush_mode = True
        pg.time.set_timer(spawn_fruit,1000)
    if game_over:
        screen.fill("black")
        game_over_txt = font.render("GAME OVER", True,"red")
        score_txt = font.render(f"SCORE: {score}", True, "blue")
        high_score_txt = font.render(f"HIGH SCORE: {high_score}",True,"green")
        retry = font.render("Press SPACE to try again!", True, "white")
        screen.blit(game_over_txt,(250,0))
        screen.blit(score_txt,(300,200))
        screen.blit(high_score_txt,(250,300))
        screen.blit(retry,(50,400))
    pg.display.flip()
    clock.tick(60)