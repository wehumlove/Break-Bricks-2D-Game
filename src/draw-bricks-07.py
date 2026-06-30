import os
import random
import colorsys
import sys

# run the script in the folder where the python code is
dir1 = "./";
sys.path.append( dir1 )
print(f"sys.path: {sys.path}")

import graphic2d
from graphic2d import general
from graphic2d import brick
from graphic2d import collision

# 1. Run in "headless" mode so no GUI window pops up
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
          
pathdir = "./"
output_dir = pathdir + "/output_images"

# file to record the collisions to add the sound in blender video editing
# so that we dont have to do it manually
pathCollision = pathdir + "collision.txt"
open(pathCollision, "w").close();
collision.fileCollision = open(pathCollision, "w")
          
# Initialize Pygame
pygame.init()

# - -----------------------------------------------------------
# 2. Setup game infos

random.seed(128)

screen_width = 1080
screen_height = 1920
ball_radius = 30
ball_speed_factor = 3

brick_width = 75
brick_height = 30
brick_padding = 4
brick_offset_top = 100
general.brick_nb_rows = 8

ball_color = (0, 255, 255)

bricksMove = 0.17
bricksMove = 0.3

FPS = 60

# - -----------------------------------------------------------

surface = pygame.Surface((screen_width, screen_height))

# Create output folder for the frames
os.makedirs(output_dir, exist_ok=True)
general.delete_all_files(output_dir);

# 3. ball speed
valMin = 4; valMax = 10
diff = (valMax - valMin)
velX = random.random() * diff * 2  - diff 
if velX < 0: velX -= valMin; 
else: velX += valMin
velY = random.random() * diff * 2  - diff 
if velY < 0: velY -= valMin; 
else: velY += valMin
ball_speed = [velX * ball_speed_factor, velY * ball_speed_factor]
#print(f"ball_speed {ball_speed[0]} {ball_speed[1]}")

# ball positin
ball_pos = [screen_width/2, screen_height-100]  # Lowered starting position
general.brick_nb_cols = int( (screen_width - brick_padding) / (brick_width + brick_padding) )
total_grid_width = (general.brick_nb_cols * brick_width) + ((general.brick_nb_cols - 1) * brick_padding)
brick_offset_left = (screen_width - total_grid_width) // 2

# bricks colors
ROW_COLORS = [
    "FF0000",
    "FFA700",
    "FFFE00",
    "62FF00",
    "00FFFD",
    "0082FF",
    "0018FF",
    "5800FF",
]

# convert from hexa to color
nb1 = general.brick_nb_rows
for ix1 in range(nb1):
    ix2 = ix1 % len(ROW_COLORS)
    c2 = general.getColorFromHex(ROW_COLORS[ix2])
    ROW_COLORS[ix2] = (c2)

# Generate brick grid 
general.bricksArray = []
for row in range(general.brick_nb_rows):
    for col in range(general.brick_nb_cols):
        x = brick_offset_left + col * (brick_width + brick_padding)
        y = brick_offset_top + row * (brick_height + brick_padding)
        x = int(x); y = int(y)
        rect = pygame.Rect(x, y, brick_width, brick_height)
        c2 = ROW_COLORS[row % len(ROW_COLORS)]
        brick1 = brick.Brick()
        brick1.rowcol = [row,col]
        brick1.coords = [x,y]
        brick1.pyrect = rect
        brick1.color1 = c2;
        brick1.displayed = True
        #print(c2)
        general.bricksArray.append(brick1)

# 4. frames counting
general.frame_count = 1
max_frames = 10000  
#max_frames = 210  

nbBricks0 = len(general.bricksArray)

bottomLine = pygame.Rect(0, screen_height-brick_height, screen_width, brick_height)

print("Simulating game with descending heart bricks... Please wait.")

while general.frame_count < max_frames:

    # --- A. CLEAR CANVAS ---
    surface.fill(general.BLACK)
    
    # --- B. MOVE & DRAW BRICKS ---
    lowestY = 0
    nbBricksDisplayed = 0
    for brick in general.bricksArray:
        if not brick.displayed: continue;
        # Move down 2 pixels per frame
        brick.coords[1] += bricksMove
        y1 = int(brick.coords[1])
        brick.pyrect.y = y1
        if y1 > lowestY: lowestY = y1
        # Draw brick body
        pygame.draw.rect(surface, brick.color1, brick.pyrect)
        # Draw clean black border outline
        pygame.draw.rect(surface, general.BLACK, brick.pyrect, width=1)
        nbBricksDisplayed += 1

    # grey floor on bottom
    pygame.draw.rect(surface, general.GREY, bottomLine)

    
    if nbBricksDisplayed == 0: break;
    
    lowestY += brick_height
    height2 = screen_height - brick_height
    if lowestY >= height2: break;
    
    nbSecs = int( general.frame_count / FPS )
    print(f"frm {general.frame_count} nbSecs {nbSecs} nbB {nbBricksDisplayed} / {nbBricks0} lowestY {lowestY} / {height2} spd {ball_speed[0]:.3f} {ball_speed[1]:.3f} ")
    
    # --- C. UPDATE BALL PHYSICS ---
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    ball_rect = pygame.Rect(
        ball_pos[0] - ball_radius, 
        ball_pos[1] - ball_radius, 
        ball_radius * 2, 
        ball_radius * 2
    )

    # --- D. WALL COLLISIONS ---
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= screen_width:
        ball_speed[0] = -ball_speed[0]
        if ball_pos[0] - ball_radius <= 0: ball_pos[0] = ball_radius + 0.01
        if ball_pos[0] + ball_radius >= screen_width: ball_pos[0] = screen_width - (ball_radius + 0.01)
        #print(f"frm {general.frame_count} wall collision 1")
        collision.saveCollision(general.frame_count, True)
    
    if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= height2:
        ball_speed[1] = -ball_speed[1]
        if ball_pos[1] - ball_radius <= 0: ball_pos[1] = ball_radius + 0.01
        if ball_pos[1] + ball_radius >= height2: ball_pos[1] = height2 - (ball_radius + 0.01)
        #print(f"frm {general.frame_count} wall collision 2")
        collision.saveCollision(general.frame_count, True)

    # --- E. BRICK COLLISIONS ---
    brickCollision1 = None
    maxOverlapCollision1 = 0
    interCollision = 0
    bricks_hits = []
    # loop to search for the bricks in collision
    for brick in general.bricksArray[:]:
        if not brick.displayed: continue
        rect1 = brick.pyrect
        if ball_rect.colliderect(rect1):
            # Resolve vertical vs horizontal bouncing path
            overlapType, overlap = collision.check_intersection_side(ball_rect, ball_speed, brick)
            print(f"frm {general.frame_count} brick {brick.rowcol} otyp {overlapType} olap {overlap}")
            if overlap > maxOverlapCollision1:
                brickCollision1 = brick
                interCollision = overlapType
                maxOverlapCollision1 = overlap
            if overlapType != general.INTER_NONE:
                bricks_hits.append(brick)
                
    if brickCollision1:
        rect1 = brickCollision1.pyrect
        rowcol1 = brickCollision1.rowcol
        if (interCollision == general.INTER_TOP) or (interCollision == general.INTER_BOTTOM):
            print(f"frm {general.frame_count} horizontal collision RC {rowcol1[0]} {rowcol1[1]} TL {rect1.top} {rect1.left} ")
            ball_speed[1] = -ball_speed[1]
        else:
            print(f"frm {general.frame_count} vertical collision RC {rowcol1[0]} {rowcol1[1]} TL {rect1.top} {rect1.left} ")
            ball_speed[0] = -ball_speed[0]
        collision.saveCollision(general.frame_count, False)
        
    # set flag for bricks not to display
    for brick2 in bricks_hits:
        brick2.displayed = False
        #continue  

    # --- F. DRAW BALL ---
    pygame.draw.circle(surface, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.draw.circle(surface, general.WHITE, (int(ball_pos[0]), int(ball_pos[1])), ball_radius, width=2)

    # --- G. SAVE FRAME ---
    frame_filename = os.path.join(output_dir, f"frame_{general.frame_count:04d}.bmp")
    pygame.image.save(surface, frame_filename)
    
    general.frame_count += 1

# add 4 seconds after the end to display the winner and confettis
for ix1 in range(4 * FPS):
    general.frame_count += 1
    frame_filename = os.path.join(output_dir, f"frame_{general.frame_count:04d}.bmp")
    pygame.image.save(surface, frame_filename)

#print(f"\nFinished! Generated {general.frame_count} frames inside the '{output_dir}/' directory.")
pygame.quit()
collision.fileCollision.close()
