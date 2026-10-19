import pygame
import random
from math import sqrt
from typing import List

WIDTH, HEIGHT = 800, 600
# Total time to draw the puzzle
TOTAL_DRAW_SECONDS = 8
# Creates some extra space so we can see the whole image
MARGIN = 120

NUM_SLICES = 250


def add_margin(point):
    """ 
    Adds a big border or margin to a point
    """
    x, y = point
    return x + MARGIN, y + MARGIN

def slice_screen(num_slices) -> List[List]:
    """
    Returns rows of "slices" of the screen, represented by
    the four corners of the slice. These are our puzzle pieces. Each
    list within the outside list contains the corners for each slice 
    across one row.  
    
    num_slices: Number of "pieces" to divide the screen into. 
    This function will return something close to the number input by the 
    user, but possibly not the exact number because the dimensions 
    of the screen may not be easily divisible into <num_slices>.  
    """

    # This math looks more complicated than it is, 
    # honestly the intuition is pretty simple and the idea of 
    # aspect ratio makes it more confusing
    aspect_ratio = WIDTH / HEIGHT
    # The rounding here is what determines how many slices we 
    # actually produce
    num_rows = round(sqrt(num_slices / aspect_ratio))
    num_cols = round(num_slices / num_rows)

    slice_width = WIDTH / num_cols
    slice_height = HEIGHT / num_rows

    slices = list()

    for row in range(0, num_rows):
        row_slices = list()
        for col in range(0, num_cols):
            left = col * slice_width
            top = row * slice_height
            right = left + slice_width
            bottom = top + slice_height

            row_slices.append([
                (left, top), 
                (right, top),
                (right, bottom),
                (left, bottom)
                ])
        slices.append(row_slices)

    return slices

def make_side(point_1, point_2) -> List:
    """
    Adds the "hump" to a line in a slice. Bear in mind too that for 
    every hump on an edge, its neighbor slice has a "hole". But the
    hole is trivial to represent since it has the same coordinates
    as the hump lines. 

       |         | 
       |   ___   | Hole 
       |__|   |__|

                   
           ___ 
        __|   |__
       |         | Hump
       |         |

    point_1: Coords for one point

    point_2: Coords for end of the line segment 
    
    Return: List indicating coordinates, possibly with a hump
    """

    (x_0, y_0) = point_1
    (x_1, y_1) = point_2

    # This is relatively where the "hump" appears on
    # the line. I wanted a pretty simple mechanism
    # for adding randomness. 
    hump_center = round(random.uniform(0.3, 0.7), 1)
    
    mid_x = x_0 + (x_1 - x_0) * hump_center
    mid_y = y_0 + (y_1 - y_0) * hump_center

    # Find the length of the line 
    # If horizontal, else if vertical line
    if x_0 == x_1:
        length = abs(y_1 - y_0)
    else:
        length = abs(x_1 - x_0)

    # Arbitrary, but I've decided that the hump will always be one 
    # fifth of the original line segment
    hump_height = .2 * length

    # LEFT and TOP is always just a straight line
    # Left or Top
    if (x_0 == x_1 and y_0 > y_1) or (x_0 < x_1 and y_0 == y_1):
        return [(x_0, y_0), (x_1, y_1)]

    # Right
    if x_0 == x_1 and y_0 < y_1:
        return [ 
            (x_0, y_0),
            (x_0, mid_y - (.1 * length)), # hump_bottom_left
            (x_0 + hump_height, mid_y - (.1 * length)), # hump_top_left
            (x_0 + hump_height, mid_y + (.1 * length)), # hump_top_right
            (x_0, mid_y + (.1 * length)), # hump_bottom_right
            (x_1, y_1)
        ]

    # Bottom
    if x_0 > x_1 and y_0 == y_1:
        return [
            (x_0, y_0),
            (mid_x + (.1 * length), y_0), # hump_bottom_left
            (mid_x + (.1 * length), y_0 + hump_height), # hump_top_left
            (mid_x - (.1 * length), y_0 + hump_height), # hump_top_right
            (mid_x - (.1 * length), y_0), # hump_bottom_right
            (x_1, y_1)
        ]


pygame.init()
screen = pygame.display.set_mode((WIDTH + MARGIN * 2, 
                                  HEIGHT + MARGIN * 2))
clock = pygame.time.Clock()

# ToDo: Have multiple images with selector
image = pygame.image.load('assets/puppy.jpg').convert()

# For drawing the lines
elapsed = 0.0
slices = slice_screen(NUM_SLICES)
seconds_per_side = TOTAL_DRAW_SECONDS / (4 * NUM_SLICES) # 4 because of 4 edges

# "slices" above are the corners of each slice
# Simply represent a side by the lines that compose it 
# Top, Right, Bottom, Left
lines = []

for row, row_slices in enumerate(slices):
    row_lines = list()

    for col, s in enumerate(row_slices):
        slice_lines = list()

        top = (s[0], s[1])
        right =  (s[1], s[2]) 
        bottom = (s[2], s[3]) 
        left = (s[3], s[0])

        # Top side
        # Don't add a hump for the slices on the top row
        if row == 0:
            slice_lines.append(make_side(*top))
        else:
            # For all other slices, the top side is the "hole" of 
            # it's upstairs neighbor's hump
            # This is messy, kind of regret not making this more 
            # object oriented =(
            slice_lines.append(list(reversed(lines[row-1][col][2])))

        # Right side
        if col != len(row_slices)-1:
            slice_lines.append(make_side(*right))
        else:
            slice_lines.append([*right])

        # Bottom side
        if row != len(slices) - 1:
            slice_lines.append(make_side(*bottom))
        else:
            slice_lines.append([*bottom])

        # Left side
        # Same idea as above: don't add a hump to any side on the
        # left of the image. Otherwise, give the side a "hole"
        # corresponding to the hump of its left neighbor
        if col == 0:
            slice_lines.append(make_side(*left))
        else:
            slice_lines.append(list(reversed(row_lines[col-1][1])))

        row_lines.append(slice_lines)

    lines.append(row_lines)

# Just flatten all of the sides, the indices aren't really needed
# anymore now that we've identified all of the humps and their 
# corresponding holes
flat_sides = list()
for row_lines in lines:
    for slice_lines in row_lines:
        for side in slice_lines:
            flat_sides.append([add_margin(p) for p in side])

running = True
while running:

    dt = clock.tick(60)/1000
    elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Line drawing
    total_progress = elapsed / seconds_per_side
    finished_sides = int(total_progress)
    current_progress = total_progress - finished_sides

    screen.fill((20, 20, 30))  # wipe the previous frame
    screen.blit(image, (add_margin((0, 0))))

    for i, side in enumerate(flat_sides):
        # The line has been drawn already, so draw it
        if i < finished_sides:
            pygame.draw.lines(screen, (255, 255, 255), False, side, 2)
        # If this is the line we're working on now, we're going to 
        # draw its current progress
        elif i == finished_sides:
            # These are all in service of finding out how much progress
            # we've made on the current line
            total_segments = len(side)-1
            segments_drawn = current_progress * total_segments
            finished_segments = int(segments_drawn)
            segment_progress = segments_drawn - finished_segments

            start = side[finished_segments]
            end = side[finished_segments + 1]
            x_0, y_0 = start
            x_1, y_1 = end
            # This looks more complicated than it is
            # Basically, get the fraction of the line that's drawn
            # at the particular point in progress
            curr_x = ((x_1 - x_0) * segment_progress) + x_0 
            curr_y = ((y_1 - y_0) * segment_progress) + y_0 
            pygame.draw.lines(screen, (255, 255, 255), False,
                  side[:finished_segments + 1] + [(curr_x, curr_y)], 2)

        else:
            break

    pygame.display.update() 

pygame.quit()
