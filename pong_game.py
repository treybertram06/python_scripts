import pygame, sys
from pygame.locals import *

pygame.init()

WIDTH = 640
HEIGHT = 480
FPS = 60

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = 3
        self.dy = -5
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0: # Bounce back if the ball goes off left side of screen
            self.dx *= -1
            self.x = 0
        elif self.x + self.radius >= WIDTH: # Check for collision with right wall and bounce back
            self.dx *= -1
            self.x = WIDTH - self.radius
        
    def check_collision(self):
        if self.y + self.radius >= HEIGHT or self.y <= 0: # Check for collision with top and bottom walls
            self.dy *= -1
        elif paddle_left.collidepoint(pygame.mouse.get_pos()):   # Check for collision with left paddle
            self.dx = -(ball.dx)
            self.x = paddle_left.x + 10
    
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5
    
    def move_up(self):
        if self.y > 0:
            self.y -= self.speed
    
    def move_down(self):
        if self.y + self.height < HEIGHT:
            self.y += self.speed
    
    def collidepoint(self, point): # Add method to check for collision with paddle
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(point)

ball = Ball(WIDTH / 2 - 5, HEIGHT / 2, 10, (255, 255, 255))
paddle_left = Paddle(0, HEIGHT / 2, 10, 60, (255, 255, 255))
paddle_right = Paddle(WIDTH - 10, HEIGHT / 2, 10, (255, 255, 255))

def update():
    global ball, paddle_left, paddle_right
    ball.move()
    if pygame.Rect(paddle_left.x, paddle_left.y, paddle_left.width, paddle_left.height).collidepoint((ball.x + 5, ball.y): # Check for collision with left paddle
        ball.check_collision()
    
def check_for_collision():   # Add a separate function to check for collisions and update the ball's velocity
    if pygame.Rect(paddle_right.x, paddle_right.y, paddle_right.width, paddle_right.height).collidepoint((ball.x - 5, ball.y): # Check for collision with right paddle
        ball.check_collision()
    elif ball.x <= 0:   # Check if the ball goes off the left side of the screen and add points to the right player
        print("Right player scored")

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:  # Added keydown event check
            if event.key == K_UP:   # Use only the up arrow key to move paddle
                paddle_left.move_up() 
            elif event.key == K_DOWN:    
                paddle_left.move_down()
    update()
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)
    pygame.draw.rect(screen, paddle_left.color, pygame.Rect(paddle_left.x, paddle_left.y, paddle_left.width, paddle_left.height)
    pygame.draw.rect(screen, paddle_right.color, pygame.Rect(paddle_right.x, paddle_right.y, paddle_right.width, paddle_right.height))
    pygame.display.flip()