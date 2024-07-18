# tạo nhiều enemy

import threading
import turtle
import winsound
import pygame
import random

maxX = 300
maxY = 300
#************
enemyStep = 0.1

playerStep = 0.1
playerAngle = 0.1


screen = turtle.Screen()
screen.setup(maxX*2,maxY*2)
screen.title("Game minh hoa thu vien turtle")
screen.bgcolor("lightblue")
#screen.bgpic("bg.gif")
#screen.addshape("tank30.gif")
screen.tracer(0)

# Khởi tạo pygame
pygame.init()

running = True

# Create PLAYER
player = turtle.Turtle()
#player.shape("tank30.gif")
player.setheading(90)
player.shape("turtle")
player.penup()

player.goto(0,-maxY+50)
#player.speed(1)



# Quản lý enemy
enemyList =[]

# Create ENEMY
colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
def createEnemy():
    enemy = turtle.Turtle()
    enemy.shape("arrow")
    enemy.shapesize(stretch_wid=2, stretch_len=2)
    enemy.color(random.choice(colors))
    enemy.setheading(-90)
    enemy.penup()
    enemy.goto(random.randint(-300,300),random.randint(200,300))
    enemyList.append(enemy)


def deleteEnemy(enemy):
    enemy.hideturtle()
    enemy.clear()
    enemyList.remove(enemy)
    del enemy


for enemyNum in range(5):
    createEnemy()


def enemyMove(enemy):
    enemy.setheading(270)
    enemy.forward(enemyStep)


#******************************************************
bulletList = []
def createBullet():
    bullet = turtle.Turtle()
    bullet.shape("triangle")
    bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
    bullet.color("red")
    bullet.penup()

    bullet.goto(player.xcor(), player.ycor())
    playerDirection = player.heading()
    bullet.setheading(playerDirection)

    bulletList.append(bullet)

def deleteBullet(bullet):
    bullet.hideturtle()
    bullet.clear()
    try:
        bulletList.remove(bullet)
    except Exception:
        print("Bullet is out of range")
              
    del bullet

bulletSpeed = 1
def bulletMove(bullet):
    bullet.forward(bulletSpeed)

# player.begin_fill()
# player.forward(100)
# player.circle(100)
# player.backward(200)
# player.circle(100)
# player.end_fill()
# Phát nhạc nền không đồng bộ
def startSound():
    pygame.mixer.music.load("sound/loop1.wav")
    pygame.mixer.music.play(-1) # -1 để lặp lại liên tục

def stopSound():
    pygame.mixer.music.stop()


# bắn súng
def fire():
    #player.clear() 
    #player.write("Fire",True,align="center",font=18)
    if len(bulletList)<10:
        createBullet()

        pygame.mixer.Sound("sound/shoot1.wav").play()



# theo dõi các phím nhấn
moveUpState = False
def pressUp():
    global moveUpState
    moveUpState = True
def releaseUp():
    global moveUpState
    moveUpState = False

moveDownState = False
def pressDown():
    global moveDownState
    moveDownState = True
def releaseDown():
    global moveDownState
    moveDownState = False

moveLeftState = False
def pressLeft():
    global moveLeftState
    moveLeftState = True
def releaseLeft():
    global moveLeftState
    moveLeftState = False

moveRightState = False
def pressRight():
    global moveRightState
    moveRightState = True
def releaseRight():
    global moveRightState
    moveRightState = False


# điều khiển player


def checkBorder():
    if player.ycor()>maxY-10:
        player.sety(maxY-10)
    if player.ycor()<-maxY+10:
        player.sety(-maxY+10)
    if player.xcor()>maxX-10:
        player.setx(maxX-10)
    if player.xcor()<-maxX-10:
        player.setx(-maxX+10)

def moveUp():
    #print("up")
    #player.setheading(90)
    player.forward(playerStep)
    checkBorder()

def moveDown():
    #print("down")
    #player.setheading(270)
    player.backward(playerStep)
    checkBorder()

def moveRight():
    #print("right")
    #player.setheading(0)
    player.right(playerAngle)
    #player.forward(playerStep)
    

def moveLeft():
    #print("left")
    #player.setheading(180)
    player.left(playerAngle)
    #player.forward(playerStep)
   

# keyboard
screen.listen()

screen.onkeypress(pressUp,"Up")
screen.onkeyrelease(releaseUp,"Up")

screen.onkeypress(pressDown,"Down")
screen.onkeyrelease(releaseDown,"Down")

screen.onkeypress(pressLeft,"Left")
screen.onkeyrelease(releaseLeft,"Left")

screen.onkeypress(pressRight,"Right")
screen.onkeyrelease(releaseRight,"Right")  

screen.onkey(fire,"space")

# Bắt đầu nhạc nền trong một luồng riêng
threading.Thread(target=startSound).start()


# Hàm hiển thị thông báo và xử lý lựa chọn
def game_over():
    stopSound()  # Dừng nhạc nền khi kết thúc
    screen.clear()  # Xóa màn hình hiện tại
    screen.bgcolor("black")  # Đổi màu nền thành đen
    
    # Turtle để vẽ nội dung thông báo
    game_over_writer = turtle.Turtle()
    game_over_writer.speed(0)
    game_over_writer.color("red")
    game_over_writer.penup()
    game_over_writer.hideturtle()
    game_over_writer.goto(0, 0)
    game_over_writer.write("GAME OVER", align="center", font=("Courier", 48, "normal"))
    global running
    running = False

    pygame.mixer.Sound("sound/gameover1.wav").play()

    # Đặt hàm gọi lại để thoát khỏi trò chơi sau 5 giây
    screen.ontimer(exit_game, 3000)

# Hàm thoát khỏi trò chơi
def exit_game():
    turtle.bye()  # Đóng màn hình Turtle


# Tạo biến điểm
score = 0

# Hiển thị điểm
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, maxY - 40)
score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}  Diff. level = {100*enemyStep:.0f}", align="center", font=("Courier", 24, "normal"))

frame_count = 0
while running:
    frame_count += 1
    # monitoring the bullet
    for bullet in bulletList:
        #   bullet move
        bulletMove(bullet)

        # bullet out of screen
        if bullet.ycor()>maxY or bullet.ycor()<-maxY or \
                bullet.xcor()>maxX or bullet.xcor()<-maxX:
            deleteBullet(bullet)

        #   monitoring the enemy
        for enemy in enemyList:
            #   bullet hit enemy
            if enemy.distance(bullet)<20:
                deleteEnemy(enemy)
                deleteBullet(bullet)
                pygame.mixer.Sound("sound/explosion1.wav").play()

                # Tăng điểm và cập nhật hiển thị
                #global score
                score += 1
                enemyStep = enemyStep*1.01
                update_score()

                
                if len(enemyList)<10:
                    createEnemy()
                    createEnemy()
        
    
    for enemy in enemyList:
        #   enemy move
        enemyMove(enemy)
        
        #   out of screen position
         # bullet out of screen
        if enemy.ycor()>maxY or enemy.ycor()<-maxY or \
                enemy.xcor()>maxX or enemy.xcor()<-maxX:
            deleteEnemy(enemy)
            createEnemy()
            
        #   game over
        if enemy.distance(player)<20:
            game_over()
            
    #   monitoring the keys to control PLAYER
    if (moveUpState):
        moveUp()
    if (moveDownState):
        moveDown()
    if (moveLeftState):
        moveLeft()
    if (moveRightState):
        moveRight()

    # Update screen at every 5 frames
    if frame_count % 5 == 0:
        screen.update()    

screen.mainloop()