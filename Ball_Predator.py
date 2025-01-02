import pygame
import sys
import random
from math import *
import sqlite3
from sqlite3 import Error




# προσπάθεια εγκαθίδρυσης σύνδεσης με τη βάση δεδομένων
try:
 
 conn = sqlite3.connect('pythonDB.db') # έφτιαξα pythonDB.db γιατί για κάποιο λόγο με την sqlite3 δεν μου έτρεχε το query δημιουργίας
 # πίνακα με δύο παραμέτρους(το id είναι περιττό αλλα το έβαλα για να να τρέχει και να φτιαχτεί ένας πίνακας για να κάνει τη δουλειά του και να κρατάει τα σκορ στο πεδίο score)
 c = conn.cursor()
 print("Connection to Python.db successfully")
     
except Error as e:
        print(f"The error '{e}' occured, no connection ith Python.db")
        
    #μέδοθος για τη δημιουργία του πίνακα της βάσης ο οποίος θα κρατάει τα σκορ    
def create_table():
   try: 
       
    c.execute('CREATE TABLE IF NOT EXISTS Scores (id INTEGER PRIMARY KEY AUTOINCREMENT, score INTEGER)')
    
    c.execute("INSERT INTO Scores (id, score) VALUES(?, ?)", (0,0))
    
    print("Scores table created successfully")
     
   except Error as e:
        print(f"The error '{e}' occured, table Scores not created")
    
   conn.commit()
    
    #μέθοδος εισαγωγής σκορ στον πίνακα της βάσης δεδομένων
def data_entry(v1,v2):
  try:  
   cu = conn.cursor() 
   print("Connection cursor successfully")
     
  except Error as e:
        print(f"The error '{e}' occured")
        
  result=cu.execute("SELECT MAX(id) AS maximum FROM Scores") 
  result = cu.fetchall() 
   
  for i in result: 
    maximum = (max(i) )
    v1=maximum+1
    try:
     c.execute("INSERT INTO Scores (id, score) VALUES(?, ?)", (v1,v2))
     
     print("Score registered successfully in python.db")
     
    except Error as e:
        print(f"The error '{e}' occured, score not register")
    
    conn.commit()
    
 # μέθοδος εύρεσης του best score στη βάση δεδομένων
def best_score_with_data_base():
      
    conn = sqlite3.connect('pythonDB.db')
    c = conn.cursor() 
    
    c.execute("SELECT MAX(score) AS maximum FROM Scores") 
    result = c.fetchall() 
      
     
   
       
        
    for i in result: 
     maximum = (i[0]) 
     return maximum


create_table()


 

#----------------------------------------------------------------------------------------------------------------------------------




pygame.init()

#ορισμός μεγέθους παραθύρου και captιοn σ' αυτό
win = pygame.display.set_mode((888,780))
pygame.display.set_caption("'Ball Predator' By Anestis Kourdis")

#φόρτωση εικόνων σε μεταβλητές
try:
    
 bg5 = pygame.image.load("predator.jfif")   
 bg = pygame.image.load("br1.png")
 bg2 = pygame.image.load("br2.png")
 bg3 = pygame.image.load("br3.png")
 bg4 = pygame.image.load("br4.png")
 

 print("level images files loaded successfully")
     
except Error as e:
 print(f"The error '{e}' occured on load level image")
 
 
 #φόρτωση ήχων σε μεταβλητές και για να παίζει η μουσική μέσω του pygame.mixer
try:

  pygame.mixer.music.load("sound.mp3")
  pygame.mixer.music.play(800)  


  blow_sound = pygame.mixer.Sound("blowsup.wav")
  beep_sound =pygame.mixer.Sound("beep.mp3")
  nextlevelSound =pygame.mixer.Sound("nextlevelSound.mp3")
  gameoverSound =pygame.mixer.Sound("gameoverSound.mp3")

  clock_sound = pygame.mixer.Sound("alarm.mp3")
  bonus_sound = pygame.mixer.Sound("bonus.mp3")
  
  print("sound files loaded successfully")
     
except Error as e:
        print(f"The error '{e}' occured, on load sound files")
  
  
#αρχικοποιήσεις μεταβλητών και λιστών του παιχνιδιού
margin = 70
lowerBound = 70

width = 940
height = 780

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


score = 0
txt=1

levelCounter=1
counter=120
blackBallCounter=2
game_over=False
ending=False
game_state = "start_menu"



best_scores=[]

#ορισμός χρωμάτων για να υπάρχει παλέτα 

# Colors
black=(0,0,0)
black2=(30,30,30)
white = (230, 230, 230)
red = (220, 68, 55)
red2=(255,82,70)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)
lime=(0,255,0)
saddlebrown=(130,62,13)

#ορισμός γραμματοσειρών και μεγέθους τους
font = pygame.font.SysFont("Snap ITC", 25)
font2 = pygame.font.SysFont("comicsansms", 30)
font3 = pygame.font.SysFont("Snap ITC", 45)

leveltext = font2.render("Level  " + str(txt), True, yellow)
display.blit(leveltext, (740, height - lowerBound + 10))
 

#--------------------------------------------------------------------------------------------------------------

# Κλάση Ball
class Ball:
    def __init__(self, speed):    
        self.a = 75
        self.b = 75
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.color = random.choice([lime, purple, orange, yellow, blue,saddlebrown])
        
    
     
    # μέθοδος για την κίνηση της κάθε μπάλας στην οθόνη
    def move(self):    
        direction = random.choice(self.probPool)

        if direction == -1:
            self.angle += -10
        elif direction == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height/80:
                self.x -= self.speed*cos(radians(self.angle)) 
            else:
                self.createBall()
        if self.y + self.b < 0 or self.y > height + 30:
            self.createBall()




# μέθοδος που σχεδιάζει μια μπάλα  
    def show(self):
       
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
    
    
        
 # μέθοδος που ελέγχει εάν μια μπάλα έχει χτυπηθεί 
    def burst(self):    
        global score
        global blackBallCounter
        pos = pygame.mouse.get_pos()
       
        if shootOnBall(self.x, self.y, self.a, self.b, pos):
           
             if self.color==black2: 
                 blow_sound.play() 
                 beep_sound.play()
                 blackBallCounter=blackBallCounter-1
                 score -= 1
             if self.color==(white): 
                 blow_sound.play() 
                 bonus_sound.play()
                 score += 14
                 
             score += 1
             blow_sound.play() 
             
             
            
             self.createBall()

    # μέθοδος που αναπαράγει μπάλες(reset μπάλας)
    def createBall(self):    
        self.a = 75
        self.b = 75
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound 
        self.angle = 90
        self.speed -= 0.0002
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.color = random.choice([black2,lime, purple, orange, white, blue,red])       
                   
        
balls = []
noBalls = 30

for i in range(noBalls):
    obj = Ball(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
    
    obj.speed=-5
    balls.append(obj)

 
   
      #μέθοδος που ελέγχει εάν το σκόπευτρο βρίσκεται πάνω στην μπάλα
def shootOnBall(x, y, a, b, pos):
    
       
       if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
       else:
        return False
     
#μέθοδος που δημιουργεί το σκόπευτρο πάνω στον δείκτη του ποντικιου και του δίνει αντίστοιχο χρώμα ανάλογα με το αν βρίσκεται ή όχι πάνω στη μπάλα
def Mouse_Point():
    
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = black
    for i in range(noBalls):
        if shootOnBall(balls[i].x, balls[i].y, balls[i].a, balls[i].b, pos)  :
            color = red2
        
    
    pygame.draw.line(display, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)

  
#μέθοδος που δημιουργεί μαύρο πλαίσιο για το κείμενο του σκορ
def Caption_for_scores():
      
      pygame.draw.rect(display,black , (0, height - lowerBound, width, lowerBound))
      
      #μέθοδος για τον έλεγχο και την αλλαγή ένδειξης πίστας και για το αν είναι σπασμένη κάποια μαύρη μπάλα ωστε να μειωθούν οι ζωές
def show_Score_Level_BlackBallsBursted():
      global levelCounter
      
      scoreText = font.render("SCORE : " + str(score), True, white)
      display.blit(scoreText, (40, height - lowerBound + 10))
      
       
          
      if counter>=90:
       
       leveltext = font2.render("Level 1", True, yellow)
       display.blit(leveltext, (740, height - lowerBound + 10)) 
       
          
      if counter<90 and counter>=60:
       
       leveltext = font2.render("Level 2", True, yellow)
       display.blit(leveltext, (740, height - lowerBound + 10)) 
       
      if counter<60 and counter>=30:
      
       leveltext = font2.render("Level 3", True, yellow)
       display.blit(leveltext, (740, height - lowerBound + 10)) 
      
      if counter<30 and counter>=1:
        
        leveltext = font2.render("Level 4", True, yellow)
        display.blit(leveltext, (740, height - lowerBound + 10)) 
        
      
      if blackBallCounter==2:
          
         blackBalls = font3.render("Lives : Q Q", True, red)
         display.blit(blackBalls, (350, height - lowerBound + 10)) 
         
      if blackBallCounter==1:
          
         blackBalls = font3.render("Lives : Q", True, red)
         display.blit(blackBalls, (350, height - lowerBound + 10))   
           
      if blackBallCounter==0:
          
         blackBalls = font3.render("Lives :  ", True, red)
         display.blit(blackBalls, (350, height - lowerBound + 10))   
         
         
  #μέθοδος για την αλλαγή σκηνής-αλλαγή πίστας      
def level():
   
    

    if counter>90 :
     
       display.blit(bg, (0, 0))
      
    if counter<90 and counter>=60:
        
       display.blit(bg2, (0, 0))
       
    if counter<60 and counter>=30:
        
        display.blit(bg3, (0, 0))
    
    if counter<30 and counter>=1:
        
        display.blit(bg4, (0, 0))    
        
   
     

    #για το κλείσιμο της εφαρμογής
def close():
    
     pygame.quit()
     sys.exit()
     
   #μέθοδος για την έναρξη ήχου προειδοποίησης οτι ο χρόνος κοντεύει να λήξει  
def clock_():
    
 if counter<10 and counter>1:
    clock_sound.play(1)   
       
    
    #μέθοδος για τη δημιουργία και τη θέση του start menu ως προς τις προτροπές για τον παίκτη 
def draw_start_menu():
    
    display.fill((0, 0, 0))
    display.blit(bg5, (0, 0)) 
    
    font2 = pygame.font.SysFont('Arial', 28)
    font3 = pygame.font.SysFont('Snap ITC', 45)
    
    
   
    start_button = font2.render('Press SPACE to Start New Game', True, (255, 255, 255))
    highsc=best_score_with_data_base()
    highscores_= font3.render("Best Score : "+str(highsc), True, (yellow))
    
    
   
    display.blit(start_button, (width/1.8 - start_button.get_width()/2, height/1.1 + start_button.get_height()/2))
    display.blit(highscores_, (width/2 - start_button.get_width()/2, height/1.2 + start_button.get_height()/2))
    
    pygame.display.update()  
    

     #μέθοδος δημιουργίας της διεπιφάνειας του game over ως προς τις προτροπές για τον παίκτη, την ενδειξη game over και το σκορ που πέτυχε
def draw_game_over_screen():
    
   display.fill((0, 0, 0))
   font = pygame.font.SysFont('Snap ITC', 50)
   font2 = pygame.font.SysFont('Arial', 40)
   title = font.render('Game Over', True, (blue)) 
   restart_button = font2.render('R - Restart', True, (255, 255, 255))
   quit_button = font2.render('Q - Quit', True, (255, 255, 255))
   last_scor = font2.render('Your Score : '+str(last_score), True, (185, 89, 152))
   
   display.blit(title, (width/2 - title.get_width()/2, height/2.2 - title.get_height()/3))
   display.blit(restart_button, (width/2 - restart_button.get_width()/2, height/1.9 + restart_button.get_height()))
   display.blit(quit_button, (width/2 - quit_button.get_width()/2, height/2 + quit_button.get_height()/2))
   display.blit(last_scor, (width/2 - last_scor.get_width()/2, height/1.3 + last_scor.get_height()/2))
   
   pygame.display.update()     
   
   
   
   #μέθοδος για τη δημιουργία της διεπιφάνειας επιτυχημένης ολοκλήρωσης του παιχνιδιού
def draw_ending_screen():
  
   display.fill((0, 0, 0))
   font = pygame.font.SysFont('Snap ITC', 60)
   font2 = pygame.font.SysFont('Arial', 50)
   title = font.render('The time has passed !!!', True, (orange)) 
   restart_button = font2.render('R - Restart', True, (255, 255, 255))
   quit_button = font2.render('Q - Quit', True, (255, 255, 255))
   last_scor = font2.render('Your Score : '+str(last_score), True, (185, 89, 152))
   
   display.blit(title, (width/2 - title.get_width()/2, height/2.2 - title.get_height()/3))
   display.blit(restart_button, (width/2 - restart_button.get_width()/2, height/1.9 + restart_button.get_height()))
   display.blit(quit_button, (width/2 - quit_button.get_width()/2, height/2 + quit_button.get_height()/2))
   display.blit(last_scor, (width/2 - last_scor.get_width()/2, height/1.3 + last_scor.get_height()/2))
   
   pygame.display.update()     
   
   
#μέθοδος για την καταχώρηση του σκορ σε αρχείο κειμένου
def append_Score_lines_to_file(file_path, lines_to_append):
    try:
        with open(file_path, 'a') as file:
            file.write('\n'.join(lines_to_append) + '\n')
        print('Score succesfully registered in '+ str({file_path}))
    except Exception as e:
        print(" Score register Error: "+str({e}))        
             
 #μέθοδος για την εύρεση του καλύτερου σκορ μέσω αρχείου κειμένου    
def highscore_with_textFile():
   file_highscore = open('scores.txt' , 'r')
   scores = []
   Rank=[]
   for line in file_highscore.readlines():
      score_info = line.split()
      scores.append((int (score_info[0])))

   scores.sort(key = lambda x:x, reverse = True)
   
   for score in scores[:3]:
   
      Rank.append(score)
   
   #return best score
   return Rank[0]
           
#-------------------------------------------------------------------------------------------------------------------

# μέθοδος - το Loop του παιχνιδιού
def game():
    
        global counter
        global score
        run = True  
        game_state = "start_menu"  #μεταβλητή για να ελέγχουμε την κατάσταση του παιχνιδιου(αν είναι start menu , gameover κλπ)
        global levelCounter
        global blackBallCounter
        global game_over
        global last_score
        global ending
        global file  
        
    
         
        #text file best score δεν χρησιμοποιήται- καλείται η μέθοδος στο παρόν παιχνίδι, γιατί χρησιμοποιούμε βάση δεδομένων(το έκανα ενδεικτικά)
        # highscore()
        
        
        #data base best score operation 
        best_score_with_data_base()
        
        
        while run:
            
            clock_()
            level()
         
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                 close()
                 
            if game_state == "start_menu":
                

                 pygame.mixer.music.stop()  
                 draw_start_menu()
                 keys = pygame.key.get_pressed()
                 if keys[pygame.K_SPACE]:
                     
                  for i in range(noBalls):
                   balls[i].speed=-5   
                   balls[i].y=height-lowerBound
                   
                   
                   
                  pygame.mixer.music.load("sound.mp3")   
                  pygame.mixer.music.play() 
                  game_state = "game"
                  game_over = False
                  ending=False
                  
                 
            elif game_state == "game":
             
             if event.type == pygame.MOUSEBUTTONDOWN:
                   
                    
                    for i in range(noBalls):
                     balls[i].burst()    
             for i in range(noBalls):
                balls[i].speed-=0.01
                balls[i].show()
                
             
             
             Mouse_Point()
             Caption_for_scores()
             show_Score_Level_BlackBallsBursted()
             
             
             if (blackBallCounter==-1 or blackBallCounter<=-2): 
              game_over = True
              game_state = "game_over"
              blackBallCounter=2
              last_score=score
              
              file_path = 'scores.txt'
              lines_to_append = [str(last_score)]
              
              #save score with text file operation
              append_Score_lines_to_file(file_path, lines_to_append)
              
              #save score with data base operation
              n=0
              data_entry(n,last_score)
              
              
              pygame.mixer.music.stop()
              clock_sound.stop()
              pygame.mixer.music.load("gameoverSound.mp3")   
              pygame.mixer.music.play() 
              
              
             if (counter<1):
            
              ending = True
              game_state = "ending"
              counter=-1
              blackBallCounter=2
              
              file_path = 'scores.txt'
              lines_to_append = [str(last_score)]
              
              #αποθήκευση score με text file operation
              append_Score_lines_to_file(file_path, lines_to_append)
              
              #αποθήκευση score με data base operation
              n=0
              data_entry(n,last_score)
              
              
              pygame.mixer.music.stop()
              clock_sound.stop()
              pygame.mixer.music.load("ending.mp3")   
              pygame.mixer.music.play()   
               
              
             for i in range(noBalls):
                balls[i].move()   
               
                leveltext = font2.render("Level ", True, yellow)
                display.blit(leveltext, (740, height - lowerBound + 10)) 
                myfont=pygame.font.Font(None,50)
                text=myfont.render("TIME: "+str(int(counter)),1,(0,0,0))
                
                
                
            
             win.blit(text,(10,5))
             counter=counter-0.1
             last_score=score
             
            
             
            
             pygame.display.update()
             clock.tick(60)
             win.blit(bg, (0, 0)) 
             
             
            
            if game_state == "ending":
                
               draw_ending_screen()
               keys = pygame.key.get_pressed()
               
            if keys[pygame.K_r]:
                
               game_state = "start_menu"
               counter=120
               score=0
               clock_sound.stop()
               
            if keys[pygame.K_q]:
              pygame.quit()
              quit()
                
                  
            if game_state == "game_over":
                
             draw_game_over_screen()
             keys = pygame.key.get_pressed()
             
            if keys[pygame.K_r]:
             game_state = "start_menu"
             counter=120
             last_score=score
             score=0
             
             clock_sound.stop()
             
             
            if keys[pygame.K_q]:
              pygame.quit()
              quit()
            
                  
           
           
                       
game() 
pygame.quit()