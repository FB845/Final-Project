import js
import random 

p5 = js.window

font1 = p5.loadFont('Akzidenz-grotesk-bold.ttf')

img1 = p5.loadImage('ACCD_Figure_A.png')
img2 = p5.loadImage('ACCD_Figure_B.png')

img3 = p5.loadImage('Start.png')
img4 = p5.loadImage('Start_Pressed.png')

img5 = p5.loadImage('Retry.png')

class Figure(): #the main "character" : myself
    def __init__(self):
        self.img1 = img1
        self.img2 = img2
        self.x = 150
        self.y = 250

    def draw(self):
        p5.push()
        p5.translate(self.x, self.y)
        if (p5.frameCount % 60 < 30):
            p5.image(self.img1, 0, 0, self.img1.width / 3, self.img1.height / 3)
        else:
            p5.image(self.img2, 0, 0, self.img2.width / 3, self.img2.height / 3)
        p5.pop()


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 2
        self.life = True

    def draw(self):
        if self.life == True:
          p5.push()
          p5.translate(self.x, self.y)
          p5.fill(0)
          p5.rect(0, 0, self.size, self.size * 2)
          p5.pop()

    def update(self):
        if self.life == True:
          self.y -= 2


class Event:
    def __init__(self, x=0, y=0, size=1):
        self.x = x
        self.y = y
        self.size = size
        self.size *= 4 
        self.speed = p5.random(0.5, 2)
        self.color = p5.color(p5.random(50, 150))
        self.text = random.choice(['Product Design 1', 'Product Design 2', "Product Design 3", 'Product Design 4', 'Design Lab 1', 'Design Lab 2', 'Design Lab 3', '6th term Review', '3D modeling', '3D modeling 2', '3D modeling 3', 'Prototype process 1', 'Prototype process 2', "3rd term Review", "Product Design 6", "Capstone"])
        self.life = True

    def draw(self):
        if self.life == True:
          p5.push()
          p5.translate(self.x, self.y)
          p5.fill(self.color)
          p5.rect(0, 0, self.size, self.size, 10)
          p5.fill(255)
          p5.textAlign(p5.CENTER)
          p5.textSize(self.size / 10)
          p5.text(self.text, self.size / 2, self.size / 2)  
          p5.pop()

enemies = []
visible_enemies = []

def spawn_enemy():
    max_attempts = 100
    for _ in range(max_attempts):
        size = int(random.random() * 20) + 10
        x_pos = p5.random(p5.width - (size * 2))
        y_pos = int(random.random() * -p5.height)
        
        enemy = Event(x_pos, y_pos, size)

        # Define a minimum distance between enemies

        # Check if the newly spawned enemy overlaps with any existing enemy
        overlapping = False
        for existing_enemy in enemies:
            distance = p5.dist(enemy.x, enemy.y, existing_enemy.x, existing_enemy.y)
            min_distance = enemy.size + existing_enemy.size
            if distance < min_distance:
                overlapping = True
                break

        if not overlapping:
            # If the newly spawned enemy does not overlap with any existing enemy, break the loop
            return enemy

    # If no valid position is found after the maximum attempts, return None
    return spawn_enemy()

figure = Figure()
bullets = [] #empty list for bullets

max_enemies_on_screen = 6  # 6 classes per term
total_enemies = 48 # 48 classes are required for BS majors

program_state = 'START' #initial state

tt = p5.millis()

def setup():
    p5.createCanvas(300, 300)
    p5.imageMode(p5.CENTER)
    p5.textAlign(p5.LEFT)
    p5.textFont(font1)
    p5.frameRate(60)

    for _ in range(max_enemies_on_screen):
        new_enemy = spawn_enemy()
        if new_enemy:
            enemies.append(new_enemy)

def draw():
    global figure, bullets, enemies, visible_enemies
    p5.background(255)
    global max_enemies_on_screen
    global program_state
    global tt

    if program_state == 'START':
        p5.push()
        p5.translate(25, 50)
        p5.noStroke()
        p5.fill(1)
        p5.textSize(20)
        p5.text('Survive as a product design student at ArtCenter', 0, 35, 200)
        p5.textSize(8)
        p5.text('use left or right arrow keys to control', 0, 100, 200, 150)
        p5.text('Freddie, Product Design 2024', 0,220, 225, 200)
        p5.image(img3, 55, 150, img3.width / 3, img3.height / 3)
        if p5.mouseIsPressed == True:
            p5.image(img4, 55, 150, img4.width / 3, img4.height / 3)
        p5.pop()
    elif program_state == 'PLAY':
        figure.draw()

        for bullet in bullets.copy():
            bullet.update()
            bullet.draw()

        handle_enemy_collisions()

        for enemy in enemies:
          enemy.y += enemy.speed
          enemy.draw()
          if enemy.life and enemy.y > p5.height:
            program_state = 'OVER'
          
        if p5.keyIsPressed == True:
            if p5.keyCode == p5.RIGHT_ARROW:
                if figure.x < p5.width - figure.img1.width / 4:
                    figure.x += 5
            elif p5.keyCode == p5.LEFT_ARROW:
                if figure.x > figure.img1.width / 4:
                    figure.x -= 5

            if p5.key == ' ' and p5.millis() - tt > 500: #shoot bullet when any key is pressed
              tt = p5.millis()
              bullet = Bullet(figure.x, figure.y - 10)
              bullets.append(bullet)

        over = False
        for enemy in enemies:
          if enemy.life:
            over = False
            break
          else:
            over = True
        
        if over:
          program_state = 'WIN'
  
    if program_state == 'OVER':
        p5.text('Yes, we all know ArtCenter is hard.', 35, 100)
        p5.image(img5, 90, 150, img3.width / 3, img3.height / 3 )
        
        
    if program_state == 'WIN':
        p5.text('Congrats! You survived ArtCenter!', 35, 100)
        p5.image(img5, 90, 150, img3.width / 3, img3.height / 3 )

def handle_enemy_collisions():
  for enemy in enemies:
    for bullet in bullets:
      if enemy.life and bullet.life and is_square_collision(enemy, bullet):
        enemy.life = False
        bullet.life = False
        if len(enemies) < total_enemies:
          new_enemy = spawn_enemy()
          if new_enemy:
              enemies.append(new_enemy)
        
      
def is_square_collision(square1, square2):
    x1 = square1.x
    y1 = square1.y
    side_length1 = square1.size
    x2 = square2.x
    y2 = square2.y
    side_length2 = square2.size
    if x1 > x2 + side_length2 or x1 + side_length1 < x2 or y1 > y2 + side_length2 or y1 + side_length1 < y2:
        return False
    else:
        return True


def keyPressed(event):
  pass

def keyReleased(event):
  pass
 
def mousePressed(event):
  pass

def mouseReleased(event):
    global program_state
    if program_state == 'START':
        program_state = 'PLAY'
    elif (program_state == 'OVER' or program_state == 'WIN'):
        program_state = 'START'
        
      
    
