import random
import pygame as pg
pg.init()
#making the screen and naming the game
Screen_width = 800
Screen_length = 600
screen = pg.display.set_mode((Screen_width,Screen_length))
pg.display.set_caption("Fruit Ninja")
#organizing initialized variables
master_volume = 0.1
run = True
hold_mouse = False
previous_mouse = None
points = 0
fruits = []
trail= []
particles = []
life = []
max_trail = 10
score = 0
frenzy_mode = False
rush_mode = False
spawn_fruit = pg.USEREVENT + 1
pg.time.set_timer(spawn_fruit,2000)
decrement_time = pg.USEREVENT +2
pg.time.set_timer(decrement_time,1000)
clock = pg.time.Clock()
background = pg.image.load("assets\images\\bg2.png").convert()
background = pg.transform.scale(background,(Screen_width,Screen_length))
timer  =  60
high_score = 0
game_over = False
counter = 0
lives_distance_count = 0

#menu 
running_state = "menu"
menu_options = ["Play","Audio","Backgrounds", "Quit"]
index = 0

backgrounds = [
    pg.image.load("assets\images\\bg2.png").convert(),
    pg.image.load("assets\images\\bg3.png").convert()
]
bg_index = 0
music = {
    "normal": "assets\sounds\\bgmusic.mp3",
    "rush_mode" : "assets\sounds\\rush_mode.mp3",
    "frenzy_mode": "assets\sounds\\frenzy_mode.mp3"
    }
sounds = {
    "slice": pg.mixer.Sound("assets\sounds\steel sound.mp3"),
    "damage": pg.mixer.Sound("assets\sounds\damage.mp3"),
    "intensity_up": pg.mixer.Sound("assets\sounds\powerUp.wav"),
    "start": pg.mixer.Sound("assets\sounds\start.mp3")
}
for sfx in sounds.values():
    sfx.set_volume(master_volume)
#Using functions as per the requirements
def load_and_play(song, prev_pos= 0):
    global music
    global master_volume
    pg.mixer.music.load(song)
    pg.mixer.music.set_volume(master_volume)
    if song == music["rush_mode"]:
        pg.mixer.music.play(-1, start = prev_pos/(1000 *1.25))
    elif song == music["frenzy_mode"]:
        pg.mixer.music.play(-1, start = (prev_pos/1000) * (1.25/1.5))
    else:
        pg.mixer.music.play(-1, start = prev_pos/1000)
load_and_play(music["normal"])

def scale_image(image, width,height):
    image = pg.transform.scale(image,(width,height))
    return image

def fruit_spawn():
    fruit_x = random.randrange(100,650)
    final_x = fruit_x*0.01
    fruit_y = 600
    velocity = random.randrange(20,25)
    bomb_chance = random.randint(1,4)
    if bomb_chance == 4:
        fruit_type = pg.image.load("assets\images\\bomb.png").convert_alpha()
    else:
        fruit_num = random.randint(1,6)
        match fruit_num:
            case 1:
                fruit_type = pg.image.load("assets\images\\banana2.png").convert_alpha()
            case 2:
                fruit_type = pg.image.load("assets\images\\apple.png").convert_alpha()
            case 3 :
                fruit_type = pg.image.load("assets\images\\pineapple.png").convert_alpha()
            case 4:
                fruit_type = pg.image.load("assets\images\\pomm2.png").convert_alpha()
            case 5:
                fruit_type = pg.image.load("assets\images\\strawberry.png").convert_alpha()
            case 6:
                fruit_type = pg.image.load("assets\images\watermelon.png").convert_alpha()
    if bomb_chance != 4:
        fruit_type = scale_image(fruit_type,100,100)
        isbomb = False
    else:
        fruit_type = scale_image(fruit_type,75,100)
        isbomb = True
    if fruit_x<375:
        go_right = True
    else:
        go_right = False
    fruits.append([fruit_x,fruit_y,velocity,fruit_type,go_right,final_x,isbomb])
    
def leave_trail(screen, trail):
    for i in range(len(trail)-1):
        pg.draw.line(screen,"white",trail[i],trail[i+1],3)
    screen.blit(screen,(0,0)) #not necessary 

def score_up(score):
    score+=10
    return score

def center(txt, y):
    return txt.get_rect(center = (Screen_width/2,y))

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
def create_particles(fruitx,fruity):
    for i in range(20):
        x = particle(fruitx,fruity)
        particles.append(x)  


class lives:
    def __init__(self,x):
        self.x = x
        heart = pg.image.load("assets\images\heart.png").convert_alpha()
        self.heart = heart_scaled = scale_image(heart,50,50) # This caused a big issue, since I put it in show, the performance was horrendous, because I was loading it each time from the very beginning. This was solved by intializing it.
    def show(self, window):
        window.blit(self.heart,(self.x,0))

for i in range(3):
    pos = 30*(i+1)
    temp_life = lives(pos)
    life.append(temp_life)






#Game run
while run:
    font = pg.font.Font("assets\Fonts\OJ.otf",50)
    tiny_font = pg.font.Font("assets\Fonts\OJ.otf",30)
    if running_state == "playing":
        #screen.fill('black') unnecesary for now
        screen.blit(scale_image(backgrounds[bg_index],800,600),(0,0))
        mouse_position = pg.mouse.get_pos()
        mouse_x,mouse_y = pg.mouse.get_pos()
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
                if not fruit[6]:
                    life.pop()
            match round(fruit[5]):
                case 1:
                    fruit[0]+=random.randint(5,7)
                case 2:
                    fruit[0]+= random.randint(4,5)
                case 3:
                    fruit[0]+=random.randint(2,4)
                case 4:
                    fruit[0]-=random.randint(5,7)
                case 5:
                    fruit[0]-=random.randint(4,5)
                case 6:
                    fruit[0]-=random.randint(2,4)
            if hold_mouse and previous_mouse:
                if fruit_hitbox.clipline(previous_mouse,mouse_position):
                    if not fruit[6]:
                        create_particles(fruit[0],fruit[1])
                        pg.mixer.Sound.play(sounds["slice"]) 
                        print("fruit sliced!")
                        score = score_up(score)
                    else:
                        pg.mixer.Sound.play(sounds["damage"])
                        life.pop()
                        if len(life)!=0:
                            life.pop()
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
        for Obj in life[:]:
            Obj.show(screen)
        if hold_mouse:
            trail.append(mouse_position)
            if len(trail)>7:
                trail.pop(0)
        else:
            trail = []
        leave_trail(screen,trail)
        if timer == 0:
            game_over = True
            fruits.clear()
        if timer<=30 and timer>10 and not rush_mode:
            rush_mode = True
            pg.time.set_timer(spawn_fruit,1000)
            load_and_play(music["rush_mode"],pg.mixer.music.get_pos())
        if timer<=10 and not timer<=0 and not frenzy_mode:
            frenzy_mode = True
            pg.time.set_timer(spawn_fruit, 500)
            load_and_play(music["frenzy_mode"],pg.mixer.music.get_pos())
        if game_over:
            load_and_play(music["normal"])
            screen.fill("black")
            game_over_txt = font.render("GAME OVER", True,"red")
            game_over_txt_center = center(game_over_txt, 100)
            score_txt = font.render(f"SCORE: {score}", True, "blue")
            score_txt_center = center(score_txt, 200)
            high_score_txt = font.render(f"HIGH SCORE: {high_score}",True,"green")
            high_score_txt_center = center(high_score_txt,300)
            retry = font.render("Press SPACE to try again!", True, "white")
            retry_center = center(retry,400)
            home = tiny_font.render("Press ENTER to return to the main menu!",1,"Yellow")
            home_center = center(home,500)
            screen.blit(game_over_txt,game_over_txt_center)
            screen.blit(score_txt,score_txt_center)
            screen.blit(high_score_txt,high_score_txt_center)
            screen.blit(retry,retry_center)
            screen.blit(home,home_center)
        if timer==30:
            if counter==0:
                pg.mixer.Sound.set_volume(sounds["intensity_up"], master_volume)
                pg.mixer.Sound.play(sounds["intensity_up"])
                counter+=1
            rush_txt = font.render("RUSH MODE", True, "green")
            x_shake = random.randint(-5,5)
            y_shake = random.randint(-5,5)
            rush_txt_center = center(rush_txt,200)
            screen.blit(rush_txt,(rush_txt_center.x + x_shake, rush_txt_center.y + y_shake))
        if timer==10:
            if counter==1:
                pg.mixer.Sound.set_volume(sounds["intensity_up"],master_volume)
                pg.mixer.Sound.play(sounds["intensity_up"])
                counter+=1
            frenzy_txt = font.render("FRENZY MODE", True, "red")
            frenzy_txt_center = center(frenzy_txt,200)
            x_shake = random.randint(-5,5)
            y_shake = random.randint(-5,5)
            screen.blit(frenzy_txt,(frenzy_txt_center.x + x_shake,frenzy_txt_center.y + y_shake))
        if len(life)==0:
            game_over = True
            timer = 0
    elif running_state == "menu":
        screen.blit(scale_image(backgrounds[bg_index],800,600),(0,0))
        for i, item in enumerate(menu_options):
            if i!=index:
                color = (255,255,255)
            else:
                color = (0,255,0)
            text = font.render(item, 1, color)
            text_center = center(text,i*100+100)
            screen.blit(text,text_center)
        notes = ["UP and DOWN to manuever","ENTER to select","LEFT and RIGHT for Audio/Volume"]
        for i, item in enumerate(notes):
            note = tiny_font.render(item,1,"yellow")
            note_rect = note.get_rect()
            note_rect.bottomright = (Screen_width- 10, Screen_length-30*i)
            screen.blit(note,note_rect)
    elif running_state == "backgrounds":
        screen.blit(scale_image(backgrounds[bg_index],800,600),(0,0))
        back_home = font.render("ENTER to go back",1,"white")
        back_home_center = center(back_home,500)
        screen.blit(back_home,back_home_center)


    #Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        if running_state == "playing":
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
                life = []
                for i in range(3):
                    pos = 30*(i+1)
                    temp_life = lives(pos)
                    life.append(temp_life)
                if event.key == pg.K_SPACE:
                    pg.mixer.Sound.set_volume(sounds["start"],master_volume)
                    pg.mixer.Sound.play(sounds["start"]) 
                    game_over = False
                    counter = 0
                    score = 0
                    timer = 60
                    frenzy_mode = False
                    rush_mode = False
                    pg.time.set_timer(spawn_fruit,2000)
                if event.key == pg.K_RETURN:
                    game_over = False
                    counter = 0
                    score = 0
                    timer = 60
                    frenzy_mode = False
                    rush_mode = False
                    running_state = "menu"
                    pg.time.set_timer(spawn_fruit,2000)
        elif running_state== "menu":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    index = (index +1) %4
                elif event.key == pg.K_UP:
                    index = (index -1) %4
                elif event.key == pg.K_RETURN and index == 0:
                    running_state = "playing"
                elif index ==1 and event.key == pg.K_LEFT:
                    master_volume-=0.05
                    master_volume = max(master_volume,0) #if the player kept decreasing volume, it will become very tedious to bring it up
                    for sfx in sounds.values():
                        sfx.set_volume(master_volume)
                    pg.mixer.music.set_volume(master_volume)
                elif index ==1 and event.key == pg.K_RIGHT:
                    master_volume+=0.05
                    master_volume = min(master_volume,1) #if the player kept increasing volume, it will become very tedious to bring it down
                    for sfx in sounds.values():
                        sfx.set_volume(master_volume)
                    pg.mixer.music.set_volume(master_volume)
                elif index == 2 and event.key == pg.K_RETURN:
                    running_state = "backgrounds"
                elif index == 3 and event.key == pg.K_RETURN:
                    run = False
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    bg_index = (bg_index+1) % 2 #forgot python precedence, learned a valuable lesson haha
                    scaled = scale_image(backgrounds[bg_index],800,600)
                    screen.blit(scaled,(0,0))
                if event.key == pg.K_LEFT:
                    bg_index = (bg_index-1) % 2 
                    scaled = scale_image(backgrounds[bg_index],800,600)
                    screen.blit(scaled,(0,0))
                if event.key == pg.K_RETURN:
                    running_state = "menu"
    fps = clock.get_fps()
    print(fps)
    pg.display.flip()
    clock.tick(60)