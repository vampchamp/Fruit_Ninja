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
fruits_gm2 = []
trail= []
particles = []
life = []
font = pg.font.Font("assets\Fonts\OJ.otf",50)
tiny_font = pg.font.Font("assets\Fonts\OJ.otf",30)
victory_screen = pg.image.load("assets\images\Victory.png").convert_alpha()
max_trail = 10
score = 0
once = True
frenzy_mode = False
rush_mode = False
spawn_fruit = pg.USEREVENT + 1
pg.time.set_timer(spawn_fruit,2000) 
#this event sets off every 2000 milliseconds

decrement_time = pg.USEREVENT +2
pg.time.set_timer(decrement_time,1000) 
#this event sets off every 1000 millisecond. you get the gist

spawn_fruit_gm2 = pg.USEREVENT +3
pg.time.set_timer(spawn_fruit_gm2,2000)
clock = pg.time.Clock() 
#we initialize the clock here so we can adjust the framerate.

background = pg.image.load("assets\images\\bg2.png").convert_alpha()
background = pg.transform.scale(background,(Screen_width,Screen_length)) 
#the background image dimensions are much larger than the window, so we scaled it to fit to the scren dimensions

timer  =  60
high_score = 0
high_score_alert = 0
game_over = False
counter = 0
lives_distance_count = 0
notes = ["UP and DOWN to manuever","ENTER to select","LEFT and RIGHT for Audio/Volume"] 
gamemodes = ["normal","ALERT"]
gamemode_index = 0
gamemode = "normal"
starting_pos = {
    "bottom_left": (0,Screen_length),
    "bottom_middle": (Screen_width/2,Screen_length),
    "bottom_right": (Screen_width,Screen_length),
    "middle_right": (Screen_width,Screen_length/2),
    "top_right": (Screen_width,0),
    "top_middle": (Screen_width/2,0),
    "top_left": (0,0),
    "middle_left": (0,Screen_length/2)
                }
#these are starting positions for the gamemode "ALERT", fruits can ONLY come from these positions.

from_to = {
    "bottom_left":"top_right",
    "bottom_middle": "top_middle",
    "bottom_right":"top_left",
    "middle_right": "middle_left",
    "top_right": "bottom_left",
    "top_middle": "bottom_middle",
    "top_left": "bottom_right",
    "middle_left": "middle_right"
}
#setting the position to opposites

#menu 
running_state = "menu"
menu_options = ["Play","Gamemode","Audio","Backgrounds", "Quit"]
index = 0

backgrounds = [
    pg.image.load("assets\images\\bg2.png").convert(),
    pg.image.load("assets\images\\bg3.png").convert()
]
bg_index = 0
#the bg_index will help us switch backgrounds since the background being displayed depends on the index

music = {
    "normal": "assets\sounds\\bgmusic.mp3",
    "rush_mode" : "assets\sounds\\rush_mode.mp3",
    "frenzy_mode": "assets\sounds\\frenzy_mode.mp3"
    }
#in the normal gamemode, there are 3 gamemodes, each one has a different song

sounds = {
    "slice": pg.mixer.Sound("assets\sounds\steel sound.mp3"),
    "damage": pg.mixer.Sound("assets\sounds\damage.mp3"),
    "intensity_up": pg.mixer.Sound("assets\sounds\powerUp.wav"),
    "start": pg.mixer.Sound("assets\sounds\start.mp3"),
    "sucess": pg.mixer.Sound("assets\sounds\success.mp3"),
    "healup": pg.mixer.Sound("assets\sounds\healup.mp3")
}
#simple sfx


for sfx in sounds.values():
    sfx.set_volume(master_volume)
#it would be very tedious to go over each sfx and change its volume, so we made a master volume that decreases or increases all sounds.

#Using functions as per the requirements
def load_and_play(song, prev_pos= 0):
    global master_volume
    pg.mixer.music.load(song)
    pg.mixer.music.set_volume(master_volume)
    if song == music["rush_mode"]:
        pg.mixer.music.play(-1, start = prev_pos/(1000 *1.25))
    elif song == music["frenzy_mode"]:
        pg.mixer.music.play(-1, start = (prev_pos/1000) * (1.25/1.5))
    else:
        pg.mixer.music.play(-1, start = prev_pos/1000)
# instead of manually loading and playing the songs, this provides us with a convinient function for playing and syncing songs.
# we set the master_volume to global so that the songs volume is equal to that of the master volume. 

load_and_play(music["normal"])

def scale_image(image, width,height):
    image = pg.transform.scale(image,(width,height))
    return image
# this function was made because it was just more intuitive for us.

def fruit_spawn():
    fruit_x = random.randrange(100,650)
    final_x = fruit_x*0.01
    fruit_y = 600
    velocity = random.randrange(20,25)
    bomb_chance = random.randint(1,4)
    star_fruit_chance = random.randint(1,12)
    if bomb_chance == 4:
        fruit_type = pg.image.load("assets\images\\bomb.png").convert_alpha()
    elif star_fruit_chance == 12:
        fruit_type = pg.image.load("assets\images\starfruit.png").convert_alpha()
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
    if bomb_chance == 4: #bomb takes priority, it doesnt matter if star_fruit_chance == 12, a bomb trumps a star_fruit.
        fruit_type = scale_image(fruit_type,75,100)
        isbomb = True
        isstarfruit = False
    elif star_fruit_chance == 12: #star fruits can grant a player up to 5 lives. each star fruit succesfully sliced through gives +1 heart.
        fruit_type = scale_image(fruit_type,100,100)
        isstarfruit = True
        isbomb = False
    else:
        fruit_type = scale_image(fruit_type,100,100)
        isbomb = False
        isstarfruit = False
    if fruit_x<375:
        go_right = True
    else:
        go_right = False
    fruits.append([fruit_x,fruit_y,velocity,fruit_type,go_right,final_x,isbomb,isstarfruit])
#the fruit spawn is one of the most crucial functions in the game. it sets the spawn position for the "fruit"(which can also be a bomb)
#,the speed, the type of "fruit", the direction of the "fruit", scales based on dimensions, and adds an isbomb truth value element.
    
def leave_trail(screen, trail):
    for i in range(len(trail)-1):
        pg.draw.line(screen,"white",trail[i],trail[i+1],3)
    screen.blit(screen,(0,0)) #not necessary 
#the maximum length of the list trail is 7, this ensures it is not too long. this is not stated here, but rather in the line 325 however it is important to know this.
#we append 7 different positions and draw them almost simultaneously, simulating a trail behind the mouse.

def score_up(score):
    score+=10
    return score
#self explanatory

def center(txt, y):
    return txt.get_rect(center = (Screen_width/2,y))
#hides the calculations and replaces it with a more intuitive function

def fruit_spawn_gm2():
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
    place1 = random.choice(list(starting_pos.keys())) #took the keys from starting_pos. put them in a list. and chose a random starting pos.
    x,y = starting_pos[place1]
    to = from_to[place1]
    x_to, y_to = starting_pos[to]
    distance_x = x_to - x
    distance_y = y_to - y
    distance = (distance_x**2 + distance_y**2)**0.5
    frame_rate = 60
    show_time = 1.5
    velocity = (distance +750) / (frame_rate *show_time)
    vel_x = distance_x/distance *velocity
    vel_y = distance_y/distance*velocity
    fruits_gm2.append([x,y,vel_x,vel_y,fruit_type,isbomb])
"""
gm2 stands for gamemode2... AKA: "ALERT". the logic here is different than the normal gamemode in that the velocity is constant. start and end positions were chosen
through graphs. speed was calculated based on how far away the end point is. the fruit should show up on the screen the amount of time put in the show_time variable. 
1.5 seconds. the pythagorean theorem was used here to calculate the distance. And the formula speed = distance/time was implemented in our code.
"""

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
        heart_scaled = scale_image(heart,50,50) # This caused a big issue, since I put it in show, the performance was horrendous, because I was loading it each time from the very beginning. This was solved by intializing it.
        self.heart = heart_scaled
    def show(self, window):
        window.blit(self.heart,(self.x,0))

for i in range(3):
    pos = 30*(i+1)
    temp_life = lives(pos)
    life.append(temp_life)

victory_screen = scale_image(victory_screen,Screen_width,Screen_length)

#Game run
while run:
    if running_state == "playing" and gamemode == "normal": 
        screen.blit(scale_image(backgrounds[bg_index],800,600),(0,0))
        mouse_position = pg.mouse.get_pos()
        for fruit in fruits[:]: #shallow copy of list
            if not fruit[6]: #fruit[6] refers to the isbomb variable. to make matters more fair, we decided to make the hitbox of the fruit bigger and the bomb smaller!
                fruit_hitbox =  pg.Rect(fruit[0],fruit[1],90,90)
            else:
                fruit_hitbox =  pg.Rect(fruit[0],fruit[1],75,75)
            fruit[1] -=fruit[2] #fruit[2] is the fruits velocity, first it goes up, we do that by subtracting the y position of the fruit by the velocity
            fruit[2] -= 0.5 #here we change the velocity so that it gradually slows down and eventually changes directions from up to down.
            if fruit[4]:
                angle = (-pg.time.get_ticks() / 10) % 360  #this simply changes the direction of rotation based on starting x - position
            else:
                angle = (pg.time.get_ticks() / 10) % 360
            fruit_rotated = pg.transform.rotate(fruit[3],angle)
            fruit_instance_new = fruit_rotated.get_rect(center = fruit_hitbox.center)
            screen.blit(fruit_rotated,fruit_instance_new) #rotation in pygame is not as simple as using the rotation function then putting the x and y. it must first be centered
            if fruit[1]>= 600:
                fruits.remove(fruit)
                if not fruit[6] and not fruit[7] and len(life)!= 0: #if its not a bomb and not a starfruit and in the rare case where you slice a bomb and a fruit falls at the same time, it checks if there are any lives to remove
                    life.pop()   #remove a life
            match round(fruit[5]):
                case 1:
                    fruit[0]+=random.randint(500,700)*0.01
                case 2:
                    fruit[0]+= random.randint(400,500)*0.01
                case 3:
                    fruit[0]+=random.randint(200,400)*0.01
                case 4:
                    fruit[0]-=random.randint(500,700)*0.01
                case 5:
                    fruit[0]-=random.randint(400,500)*0.01
                case 6:
                    fruit[0]-=random.randint(200,400)*0.01
                #based on starting position, this decided how far the "fruit" can go. This is to prevent the "fruit" from going out of bounds.
            if hold_mouse and previous_mouse:
                if fruit_hitbox.clipline(previous_mouse,mouse_position): #simulating slicing
                    if not fruit[6] and not fruit[7]: #if its not a bomb and its not a star fruit
                        create_particles(fruit[0],fruit[1])
                        pg.mixer.Sound.play(sounds["slice"]) 
                        print("fruit sliced!")
                        score = score_up(score)
                    elif fruit[7] and not fruit[6]: # if its a star fruit but not a bomb (since bomb takes priority as we said)
                        create_particles(fruit[0],fruit[1])
                        pg.mixer.Sound.play(sounds["slice"]) 
                        print("fruit sliced!")
                        score = score_up(score)
                        if len(life)<5 and not game_over:
                            temp = lives(len(life)*30 +30)
                            life.append(temp)
                            pg.mixer.Sound.play(sounds["healup"]) 
                    else: #if its a bomb
                        pg.mixer.Sound.play(sounds["damage"])
                        if len(life)!= 0:
                            life.pop()  #sometimes you can strike two bombs at once, this leads to an error. so its better to check the list before removing the next one.
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
            #the list starts out as empty. However, when a fruit is sliced, the x and y position of where the fruit was 
            #sliced go to the create_particles function and creates 20 different instances of particles. this makes all particles scatter starting from those x and y pos.
            Obj.show(screen)
            if Obj.timeout == 0:
                particles.remove(Obj)
                #we dont want the particles to last too long, every time we show then, the timeout decrements by one until it eventually reaches 0.
        for Obj in life[:]:
            Obj.show(screen) #showing hearts
        if hold_mouse:
            trail.append(mouse_position)
            if len(trail)>7:
                trail.pop(0) #pop the oldest position.
        else:
            trail = []
        leave_trail(screen,trail)
        if timer == 0:
            game_over = True
            fruits.clear() 
            #we dont want fruits staying after the game is over. 
            #if we didnt clear, the game would run fine, but you would still be able to slice fruits even in the game over screen.
        if timer<=30 and timer>10 and not rush_mode:
            rush_mode = True
            pg.time.set_timer(spawn_fruit,1000)
            load_and_play(music["rush_mode"],pg.mixer.music.get_pos())
        if timer<=10 and not timer<=0 and not frenzy_mode:
            frenzy_mode = True
            pg.time.set_timer(spawn_fruit, 500)
            load_and_play(music["frenzy_mode"],pg.mixer.music.get_pos())
        if game_over and len(life)==0:
            #simple text loading
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
        if game_over and len(life)!=0:
            load_and_play(music["normal"])
            screen.blit(victory_screen,(0,0))
            if once:
                pg.mixer.Sound.set_volume(sounds["intensity_up"],master_volume)
                pg.mixer.Sound.play(sounds["intensity_up"])
                once = False
            game_over_txt = font.render("WHAT A CHAMP!", True,"green")
            game_over_txt_center = center(game_over_txt, 50)
            score_txt = font.render(f"SCORE: {score}     HIGH SCORE: {high_score}", True, "gold")
            score_txt_center = center(score_txt, 150)
            retry = font.render("Press SPACE to try again!", True, "white")
            retry_center = center(retry,500)
            home = tiny_font.render("Press ENTER to return to the main menu!",1,"Yellow")
            home_center = center(home,550)
            screen.blit(game_over_txt,game_over_txt_center)
            screen.blit(score_txt,score_txt_center)
            screen.blit(retry,retry_center)
            screen.blit(home,home_center)
        if timer==30:
            if counter==0:
                pg.mixer.Sound.set_volume(sounds["intensity_up"], master_volume)
                pg.mixer.Sound.play(sounds["intensity_up"])
                counter+=1 
                #why use a counter? you might think. Because if we dont use a counter, the game will keep playing the same sound from the begnning for a full second.
                #since the fps is 60, we are looping over the run loop 60 times, playing the same sound 60 times! we only want to play it once.
            rush_txt = font.render("RUSH MODE", True, "green")
            x_shake = random.randint(-5,5)
            y_shake = random.randint(-5,5)
            rush_txt_center = center(rush_txt,200)
            screen.blit(rush_txt,(rush_txt_center.x + x_shake, rush_txt_center.y + y_shake))
            #simple shaking animation for text. originally we thought to make it fade but this fits the vibe better.
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
            #same thing as before
        if len(life)==0:
            game_over = True
            timer = 0
            #self explanatory
    elif running_state == "menu":
        screen.blit(scale_image(backgrounds[bg_index],800,600),(0,0))
        for i, item in enumerate(menu_options): #gives us index and contents of list at that index
            if i!=index:
                color = (255,255,255) #white
            else:
                color = (0,255,0) #green
            text = font.render(item, 1, color)
            text_center = center(text,i*75+100) # we dont want them to stack so mutliply the position at i by 75.
            screen.blit(text,text_center)
        for i, item in enumerate(notes):
            note = tiny_font.render(item,1,"yellow")
            note_rect = note.get_rect()
            note_rect.bottomright = (Screen_width- 10, Screen_length-30*i)
            screen.blit(note,note_rect)
        mode = tiny_font.render(gamemode, 1, "blue")
        mode_center = center(text,50)
        screen.blit(mode,mode_center)
        #same logic
    elif running_state == "backgrounds":
        screen.blit(scale_image(backgrounds[bg_index],800,600),(0,0))
        back_home = font.render("ENTER to go back",1,"white")
        maneuvering = tiny_font.render("Left arrow and Right arrow to switch!", 1, "yellow")
        maneuvering_center = center(maneuvering,100)
        back_home_center = center(back_home,500)
        screen.blit(back_home,back_home_center)
        screen.blit(maneuvering,maneuvering_center)
        #UI for backgrounds
    elif running_state == "playing" and gamemode == "ALERT": #Gamemode ALERT
        screen.blit(scale_image(backgrounds[bg_index],800,600),(0,0))
        mouse_position = pg.mouse.get_pos()
        for fruit in fruits_gm2[:]: #shallow copy of list
            fruit[0] +=fruit[2] #x + velocity of x
            fruit[1] +=fruit[3] #y + velocity of y
            if not fruit[5]:
                fruit_hitbox =  pg.Rect(fruit[0],fruit[1],90,90) 
            else:
                fruit_hitbox =  pg.Rect(fruit[0],fruit[1],75,75)
            screen.blit(fruit[4],(fruit[0],fruit[1]))
            if (fruit[0]>Screen_width or fruit[0]<0) and (fruit[1]>Screen_length or fruit[1]<0): #this is simply saying "if its not in the screen, remove it"
                fruits_gm2.remove(fruit)
            if hold_mouse and previous_mouse:
                if fruit_hitbox.clipline(previous_mouse,mouse_position):
                    if not fruit[5]: #if not a bomb 
                        create_particles(fruit[0],fruit[1])
                        pg.mixer.Sound.play(sounds["slice"]) 
                        print("fruit sliced!")
                        score = score_up(score)
                    else: #if its a bomb
                        pg.mixer.Sound.play(sounds["damage"])
                        timer = 0
                        game_over = True
                    fruits_gm2.remove(fruit)
        if score>high_score_alert:
            high_score_alert = score
        time = font.render(f"{timer}", 1, "black")
        screen.blit(time,(700,0))
        text = font.render(f"score: {score}",1,"black")
        screen.blit(text,(250,0))
        previous_mouse = mouse_position if hold_mouse else None
        for Obj in particles[:]:
            Obj.scatter()
            Obj.show(screen) #everytime we show it we decrease the timeout by one until it eventually reaches 0
            if Obj.timeout == 0:
                particles.remove(Obj)
        if hold_mouse:
            trail.append(mouse_position)
            if len(trail)>7: 
                trail.pop(0) #we dont want the trail to to be too long
        else:
            trail = [] #when you let go the trail disapears
        leave_trail(screen,trail)
        if timer == 0:
            game_over = True
            fruits.clear()
        if game_over:
            load_and_play(music["normal"]) #resetting music so that if it were in rush or frenzy mode it wouldnt carry if we restart
            screen.fill("black")
            game_over_txt = font.render("GAME OVER", True,"red")
            game_over_txt_center = center(game_over_txt, 100)
            score_txt = font.render(f"SCORE: {score}", True, "blue")
            score_txt_center = center(score_txt, 200)
            high_score_txt = font.render(f"HIGH SCORE: {high_score_alert}",True,"green")
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
            #simple text rendering


            
    #Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
            #this is CRUCIAL event. without this you wouldnt be able to close the game by the x icon on the top right. except by pressing the quit button we made.
        if running_state == "playing" and gamemode == "normal":
            if event.type == pg.MOUSEBUTTONDOWN:
                hold_mouse = True
                #if youre holding down ur mouse, hold_mouse is set to true.
            if event.type == pg.MOUSEBUTTONUP:
                hold_mouse = False
                #if you are not, then its false.
            if event.type == spawn_fruit and not game_over: #it would be unreasonable to spawn fruits if the game is over.
                spawn_amount = random.randint(1,3) 
                for i in range(spawn_amount):
                    fruit_spawn()
                    #spawn 1 to 3 fruits. depending on spawn amount
            if event.type == decrement_time:
                if not game_over:
                    timer-=1
            if event.type == pg.KEYDOWN and game_over:
                life = []
                #reset lives, we dont want them to stack.
                for i in range(3):
                    pos = 30*(i+1)
                    temp_life = lives(pos)
                    life.append(temp_life)
                if event.key == pg.K_SPACE:
                    pg.mixer.Sound.set_volume(sounds["start"],master_volume)
                    pg.mixer.Sound.play(sounds["start"]) 
                    game_over = False
                    counter = 0
                    once = True
                    score = 0
                    timer = 60
                    frenzy_mode = False
                    rush_mode = False
                    pg.time.set_timer(spawn_fruit,2000)
                    #restart the game if you pres space
                if event.key == pg.K_RETURN:
                    game_over = False
                    counter = 0
                    score = 0
                    once = True
                    timer = 60
                    frenzy_mode = False
                    rush_mode = False
                    running_state = "menu"
                    pg.time.set_timer(spawn_fruit,2000)
                    #go back to menu if you press Enter
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    fruits.clear()
                    life = []
                    for i in range(3):
                        pos = 30*(i+1)
                        temp_life = lives(pos)
                        life.append(temp_life)
                        game_over = False
                    counter = 0
                    score = 0
                    once = True
                    timer = 60
                    frenzy_mode = False
                    rush_mode = False
                    running_state = "menu"
                    pg.time.set_timer(spawn_fruit,2000)

        elif running_state == "menu":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    index = (index +1) %5
                elif event.key == pg.K_UP:
                    index = (index -1) %5
                elif event.key == pg.K_RETURN and index == 0:
                    running_state = "playing"
                elif event.key == pg.K_RETURN and index == 1:
                    gamemode_index = (gamemode_index+1) % 2
                    gamemode = gamemodes[gamemode_index]
                elif index ==2 and event.key == pg.K_LEFT:
                    master_volume-=0.05
                    master_volume = max(master_volume,0) #if the player kept decreasing volume, it will become very tedious to bring it up
                    for sfx in sounds.values():
                        sfx.set_volume(master_volume)
                    pg.mixer.music.set_volume(master_volume)
                elif index ==2 and event.key == pg.K_RIGHT:
                    master_volume+=0.05
                    master_volume = min(master_volume,1) #if the player kept increasing volume, it will become very tedious to bring it down
                    for sfx in sounds.values():
                        sfx.set_volume(master_volume)
                    pg.mixer.music.set_volume(master_volume)
                elif index == 3 and event.key == pg.K_RETURN:
                    running_state = "backgrounds"
                elif index == 4 and event.key == pg.K_RETURN:
                    run = False
        elif running_state == "playing" and gamemode == "ALERT": #very similiar logic to the one before
            if event.type == pg.MOUSEBUTTONDOWN:
                hold_mouse = True
            if event.type == pg.MOUSEBUTTONUP:
                hold_mouse = False
            if event.type == spawn_fruit_gm2 and not game_over:
                spawn_amount = random.randint(1,3)
                for i in range(spawn_amount):
                    fruit_spawn_gm2()
            if event.type == decrement_time:
                if not game_over:
                    timer-=1
            if event.type == pg.KEYDOWN and game_over:
                if event.key == pg.K_SPACE:
                    pg.mixer.Sound.set_volume(sounds["start"],master_volume)
                    pg.mixer.Sound.play(sounds["start"]) 
                    game_over = False
                    score = 0
                    timer = 60
                    pg.time.set_timer(spawn_fruit,2000)
                if event.key == pg.K_RETURN:
                    game_over = False
                    score = 0
                    timer = 60
                    running_state = "menu"
                    pg.time.set_timer(spawn_fruit,2000)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    fruits_gm2.clear()
                    score = 0
                    timer = 60
                    running_state = "menu"
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    bg_index = (bg_index+1) % 2 
                    scaled = scale_image(backgrounds[bg_index],800,600)
                    screen.blit(scaled,(0,0))
                if event.key == pg.K_LEFT:
                    bg_index = (bg_index-1) % 2 
                    scaled = scale_image(backgrounds[bg_index],800,600)
                    screen.blit(scaled,(0,0))
                if event.key == pg.K_RETURN:
                    running_state = "menu"
    fps = clock.get_fps() #you can check your fps in the terminal. it should be between 55 and 60. no less.
    print(fps)
    pg.display.flip() #update the screen
    clock.tick(60) #set fps to 60