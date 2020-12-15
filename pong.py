import pygame, sys, random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    #moves by speed defined in speed variables
    ball.x += ball_speed_x
    ball.y += ball_speed_y
# allows ball to bounce around
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(ping_sound)
        ball_speed_y *= -1
    
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1
    
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(ping_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0: # allows for collisions on top and bottom of paddle
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(ping_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    #to avoid player's rectangle from exiting the screen
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom >ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, ball_moving, score_time
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)
    
    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2 -10, screen_height/2 + 20))
    
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width/2 -10, screen_height/2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width/2 -10, screen_height/2 + 20))
    
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1,-1))
        ball_speed_x = 7 * random.choice((1,-1))
        score_time = None
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

#Attempting background music
music = pygame.mixer.music.load('martialarts.mp3')
pygame.mixer.music.play(-1)

screen_width = 1100
screen_height = 760
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Triminator in Balls of Fury')

#Rectangles for the game
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70,10,140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
light_blue = (0, 180, 255)
#speed variables two are used to manipulate speed for each axis
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7

player_score = 0
opponent_score = 0
game_font = pygame.font.SysFont('quicksand', 40)

#import sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
ping_sound = pygame.mixer.Sound("ping.mp3")

#Timer
score_time = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            #only recognizes unpressed to pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed +=7
            if event.key == pygame.K_UP:
                player_speed -=7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -=7
            if event.key == pygame.K_UP:
                player_speed +=7


    ball_animation()
    player_animation()
    opponent_ai()
    

    screen.fill(bg_color) #background display color
    pygame.draw.rect(screen,light_blue, player)
    pygame.draw.rect(screen,light_blue, opponent)
    pygame.draw.ellipse(screen, light_blue, ball) #frame draws ellipse for ball
    pygame.draw.aaline(screen, light_blue, (screen_width/2,0), (screen_width/2, screen_height))
#line to separate two sides
    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text,(560,450)) #blit puts one surface on another

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text,(525,450))

    pygame.display.flip()
    clock.tick(60)