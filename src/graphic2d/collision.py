import os
import random
import colorsys

import graphic2d
from graphic2d import general
from graphic2d import brick

fileCollision = None

def saveCollision(frame1, isWall):
    str1 = f"{frame1},{isWall}\n" 
    fileCollision.write(str1); 
          
# A = Ball , B = brick
def check_intersection_side(rectA, speedA, brickB):
    """Determines which side Rectangle A is intersecting Rectangle B.
    Each rect should be a dict with keys: 'left', 'right', 'top', 'bottom'
    """
    frame_count = general.frame_count;
    
    trace1 = False
    #trace1 = True
    rectB = brickB.pyrect;

    if trace1:
        print(f"frm {frame_count} ---------- check_intersection_side ----------------")
        print(f"frm {frame_count} rectB L {rectB.left} R {rectB.right} T {rectB.top} B {rectB.bottom}")
        print(f"frm {frame_count} rectA L {rectA.left} R {rectA.right} T {rectA.top} B {rectA.bottom}")
        print(f"frm {frame_count} speedA {speedA[0]:.3f} {speedA[1]:.3f}")

    ALeftInside = False
    ARightInside = False
    ATopInside = False
    ABottomInside = False
    if rectB.left <= rectA.left <= rectB.right:
        if trace1:
            print(f"frm {frame_count} brick B         L-----------B");
            print(f"frm {frame_count} ball  A                L--------R");
            print(f"frm {frame_count} C1 BL {rectB.left} AL {rectA.left} BR {rectB.right}")
        ALeftInside = True
    if rectB.left <= rectA.right <= rectB.right:
        if trace1:
            print(f"frm {frame_count} brick B         L-----------R");
            print(f"frm {frame_count} ball  A     L--------R");
            print(f"frm {frame_count} C2 BL {rectB.left} AR {rectA.right} BR {rectB.right}")
        ARightInside = True
    if rectB.top <= rectA.top <= rectB.bottom:
        if trace1:
            print(f"frm {frame_count} brick B         T-----------B");
            print(f"frm {frame_count} ball  A                T--------B");
            print(f"frm {frame_count} C3 BT {rectB.top} AT {rectA.top} BB {rectB.bottom}")
        ATopInside = True
    if rectB.top <= rectA.bottom <= rectB.bottom:
        if trace1:
            print(f"frm {frame_count} brick B         T-----------B");
            print(f"frm {frame_count} ball  A     T--------B");
            print(f"frm {frame_count} C4 BT {rectB.top} AB {rectA.bottom} BB {rectB.bottom}")
        ABottomInside = True

    if trace1: print(f"frm {frame_count} ALeftInside {ALeftInside} ARightInside {ARightInside} ATopInside {ATopInside} ABottomInside {ABottomInside} ")
    
    
    # 1. Check if they are even intersecting at all
    # If there is no overlap on either axis, they don't touch.
    if (
        rectA.right <= rectB.left
        or rectA.left >= rectB.right
        or rectA.bottom <= rectB.top
        or rectA.top >= rectB.bottom
    ):
        if trace1: print(f"frm {frame_count} -10- No intersection")
        return INTER_NONE, 0  # "No intersection"

    overlap = 0
    overlap_type1 = general.INTER_NONE

    #   brick B         T-----------B
    #   ball  A                T--------B
    #   brick B         L-------------------R
    #   ball  A                L--------R
    if ATopInside and ALeftInside and ARightInside and (speedA[1] < 0): 
        brickC = brickB.getNextBrick(general.INTER_BOTTOM)
        if trace1: print(f"frm {frame_count} -01- brick bot disp {brick.isBrickDisplayed(brickC)}")
        if not brick.isBrickDisplayed(brickC):
            overlap_type1 = general.INTER_TOP
            overlap = -(rectA.top - rectB.bottom)
            if trace1: print(f"frm {frame_count} -01- olap {overlap} typ1 {overlap_type1}")
    #   brick B             T-----------B
    #   ball  A       T--------B
    #   brick B         L-------------------R
    #   ball  A                L--------R
    elif ABottomInside and ALeftInside and ARightInside and (speedA[1] > 0): 
        brickC = brickB.getNextBrick(general.INTER_TOP)
        if trace1: print(f"frm {frame_count} -02- brick top disp {brick.isBrickDisplayed(brickC)}")
        if not brick.isBrickDisplayed(brickC):
            overlap_type1 = general.INTER_BOTTOM
            overlap = -(rectB.top - rectA.bottom)
            if trace1: print(f"frm {frame_count} -02- olap {overlap} typ1 {overlap_type1}")
    #   brick B     T----------------B
    #   ball  A          T--------B
    #   brick B         L-------------------R
    #   ball  A                        L--------R
    elif ALeftInside and ATopInside and ABottomInside and (speedA[0] < 0): 
        brickC = brickB.getNextBrick(general.INTER_RIGHT)
        if trace1: print(f"frm {frame_count} -03- brick right disp {brick.isBrickDisplayed(brickC)}")
        if not brick.isBrickDisplayed(brickC):
            overlap_type1 = general.INTER_LEFT
            overlap = -(rectA.left - rectB.right)
            if trace1: print(f"frm {frame_count} -03- olap {overlap} typ1 {overlap_type1}")
    #   brick B     T----------------B
    #   ball  A          T--------B
    #   brick B         L------------R
    #   ball  A     L--------R
    elif ARightInside and ATopInside and ABottomInside and (speedA[0] > 0): 
        brickC = brickB.getNextBrick(general.INTER_LEFT)
        if trace1: print(f"frm {frame_count} -04- brick left disp {brick.isBrickDisplayed(brickC)}")
        if not brick.isBrickDisplayed(brickC):
            overlap_type1 = general.INTER_RIGHT
            overlap = -(rectB.left - rectA.right)
            if trace1: print(f"frm {frame_count} -04- olap {overlap} typ1 {overlap_type1}")
    #   brick B         T-----------B
    #   ball  A                T--------B
    #   brick B         L-------------------R
    #   ball  A     L--------R
    elif ATopInside and ARightInside: 
        brickC = brickB.getNextBrick(general.INTER_LEFT)
        brickCDis = brick.isBrickDisplayed(brickC)
        brickD = brickB.getNextBrick(general.INTER_BOTTOM)
        brickDDis = brick.isBrickDisplayed(brickD)
        if trace1: print(f"frm {frame_count} -05- left Brck {brickCDis} bot brck {brickDDis}")
        overlap_top = -(rectA.top - rectB.bottom)
        overlap_right = -(rectB.right - rectA.left)
        if (not brickCDis) and (not brickDDis):
            if (overlap_top > overlap_right)  and (speedA[1] < 0):
                overlap = overlap_top
                overlap_type1 = general.INTER_TOP
            elif (speedA[0] > 0):
                overlap = overlap_right
                overlap_type1 = general.INTER_RIGHT
        elif (not brickCDis) and (speedA[0] > 0):
            overlap = overlap_right
            overlap_type1 = general.INTER_RIGHT
        elif (not brickDDis) and (speedA[1] < 0):
            overlap = overlap_top
            overlap_type1 = general.INTER_TOP
    #   brick B         T-----------B
    #   ball  A                T--------B
    #   brick B         L-------------------R
    #   ball  A                        L--------R
    elif ATopInside and ALeftInside: 
        brickC = brickB.getNextBrick(general.INTER_RIGHT)
        brickCDis = brick.isBrickDisplayed(brickC)
        brickD = brickB.getNextBrick(general.INTER_BOTTOM)
        brickDDis = brick.isBrickDisplayed(brickD)
        if trace1: print(f"frm {frame_count} -06- Right Brck {brickCDis} Bot Brck {brickDDis}")
        overlap_top = -(rectA.top - rectB.bottom)
        overlap_left = -(rectA.left - rectB.right)
        if (not brickCDis) and (not brickDDis):
            if (overlap_left > overlap_top) and (speedA[0] < 0):
                overlap = overlap_left
                overlap_type1 = general.INTER_LEFT
            elif (speedA[1] < 0):
                overlap = overlap_top
                overlap_type1 = general.INTER_TOP
        elif (not brickCDis)  and (speedA[0] < 0):
            overlap = overlap_left
            overlap_type1 = general.INTER_LEFT
        elif (not brickDDis) and (speedA[1] < 0):
            overlap = overlap_top
            overlap_type1 = general.INTER_TOP
    #   brick B         T-----------B
    #   ball  A     T--------B
    #   brick B         L-------------------R
    #   ball  A     L--------R
    elif ABottomInside and ARightInside: 
        brickC = brickB.getNextBrick(general.INTER_LEFT)
        brickCDis = brick.isBrickDisplayed(brickC)
        brickD = brickB.getNextBrick(general.INTER_TOP)
        brickDDis = brick.isBrickDisplayed(brickD)
        if trace1: print(f"frm {frame_count} -07- left Brck {brickCDis} top brck {brickDDis}")
        overlap_bottom = -(rectB.top - rectA.bottom)
        overlap_right = -(rectB.left - rectA.right)
        if (not brickCDis) and (not brickDDis):
            if (overlap_bottom > overlap_right) and (speedA[1] > 0):
                overlap = overlap_bottom
                overlap_type1 = general.INTER_BOTTOM
            elif (speedA[1] > 0):
                overlap = overlap_right
                overlap_type1 = general.INTER_RIGHT
        elif (not brickCDis) and (speedA[0] > 0):
            overlap = overlap_right
            overlap_type1 = general.INTER_RIGHT
        elif (not brickDDis) and (speedA[1] > 0):
            overlap = overlap_bottom
            overlap_type1 = general.INTER_BOTTOM
    #   brick B         T-----------B
    #   ball  A     T--------B
    #   brick B         L-------------------R
    #   ball  A                        L--------R
    elif ABottomInside and ALeftInside: 
        brickC = brickB.getNextBrick(general.INTER_RIGHT)
        brickCDis = brick.isBrickDisplayed(brickC)
        brickD = brickB.getNextBrick(general.INTER_TOP)
        brickDDis = brick.isBrickDisplayed(brickD)
        if trace1: print(f"frm {frame_count} -08- right Brck {brickCDis} top brck {brickDDis}")
        overlap_bottom = -(rectB.top - rectA.bottom)
        overlap_left = -(rectA.left - rectB.right)
        if (not brickCDis) and (not brickDDis) and (speedA[1] > 0):
            if overlap_bottom > overlap_left:
                overlap = overlap_bottom
                overlap_type1 = general.INTER_BOTTOM
            elif (speedA[0] < 0):
                overlap = overlap_left
                overlap_type1 = general.INTER_LEFT
        elif (not brickCDis) and (speedA[0] < 0):
            overlap = overlap_left
            overlap_type1 = general.INTER_LEFT
        elif (not brickDDis) and (speedA[1] > 0):
            overlap = overlap_bottom
            overlap_type1 = general.INTER_BOTTOM
        
    if trace1: print(f"frm {frame_count} brck TL {rectB.top} {rectB.left} olap {overlap} otyp {overlap_type1}")
        
    return overlap_type1, overlap
    

# ----test method check_intersection_side--------------------
if False:
    nbDis = 30
    nbBricks = len(bricks)
    for ix1 in range(nbBricks-nbDis,nbBricks,1):
        brick1 = bricks[ix1]
        print(f"ix1 {ix1} brick coords {brick1.coords} rowcol {brick1.rowcol} pyrect {brick1.pyrect}")
    ix2 = nbBricks-2
    brick1 = bricks[ix2]
    print(f"ix2 {ix2} brick coords {brick1.coords} rowcol {brick1.rowcol} pyrect {brick1.pyrect}")
    print(f"nbRow {BRICK_NB_ROWS} nbCol {BRICK_NB_COLS} width {brick_width} height {brick_height} ball_radius {ball_radius}")
    #ball_rect = pygame.Rect(ballx - ball_radius, bally - ball_radius, ball_radius * 2, ball_radius * 2 )
    #print(f"ball ball_rect {ball_rect} ")
    print("# test1 ----No Inter------------");
    #brick1 = bricks[0]
    ballx = brick1.coords[0]+brick_width/2; bally = brick1.coords[1] + brick_height + 10
    ball_rect = pygame.Rect( ballx, bally, ball_radius * 2, ball_radius * 2 )
    check_intersection_side(ball_rect, brick1)
    print("# test2 ----inter Top (left) ------------");  
    #brick1 = bricks[0]
    ballx = brick1.coords[0]+brick_width/2; bally = brick1.coords[1] + brick_height - 10
    ball_rect = pygame.Rect( ballx, bally, ball_radius * 2, ball_radius * 2 )
    check_intersection_side(ball_rect, brick1)
    print("# test3 ----inter Top (right)------------");  
    #brick1 = bricks[0]
    ballx = brick1.coords[0]-10; bally = brick1.coords[1] + brick_height - 10
    ball_rect = pygame.Rect( ballx, bally, ball_radius * 2, ball_radius * 2 )
    check_intersection_side(ball_rect, brick1)
    print("# test4 ----inter Top (inside)------------");  
    #brick1 = bricks[0]
    ballx = brick1.coords[0]+10; bally = brick1.coords[1] + brick_height - 10
    ball_rect = pygame.Rect( ballx, bally, ball_radius * 2, ball_radius * 2 )
    check_intersection_side(ball_rect, brick1)
    print("# test5 ----inter Bottom (left) ------------");  
    brick1 = bricks[2]
    #brick1 = bricks[0]
    ballx = brick1.coords[0]+brick_width/2; bally = brick1.coords[1] + 10 - ball_radius * 2
    ball_rect = pygame.Rect( ballx, bally, ball_radius * 2, ball_radius * 2 )
    check_intersection_side(ball_rect, brick1)
    print("# test6 ----inter Bottom (right)------------");  
    #brick1 = bricks[0]
    ballx = brick1.coords[0]-10; bally = brick1.coords[1] + 10 - ball_radius * 2
    ball_rect = pygame.Rect( ballx, bally, ball_radius * 2, ball_radius * 2 )
    check_intersection_side(ball_rect, brick1)
    print("# test7 ----inter Bottom (inside)------------");  
    #brick1 = bricks[0]
    ballx = brick1.coords[0]+10; bally = brick1.coords[1] + 10 - ball_radius * 2
    ball_rect = pygame.Rect( ballx, bally, ball_radius * 2, ball_radius * 2 )
    check_intersection_side(ball_rect, brick1)
    
    raise ValueError("End of test") 
# ------------------------


