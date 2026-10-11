import pygame
from math import sqrt

WIDTH, HEIGHT = 800, 600
# Creates some extra space so we can see the whole image
MARGIN = 40     

def add_margin(point):
    x, y = point
    return x + MARGIN, y + MARGIN


def slice_screen(num_slices):
    """
    Returns a list of "slices" of the screen, represented by
    the four corners of the slice.

    screen: Pygame display
    
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
        for col in range(0, num_cols):
            left = col * slice_width
            top = row * slice_height
            right = left + slice_width
            bottom = top + slice_height

            slices.append([(left, top), 
                           (right, top),
                           (right, bottom),
                           (left, bottom)
                           ])

    return slices


pygame.init()
screen = pygame.display.set_mode((WIDTH + MARGIN * 2, 
                                  HEIGHT + MARGIN * 2))
clock = pygame.time.Clock()

# ToDo: Have multiple images with selector
image = pygame.image.load('assets/puppy.jpg').convert()

# For drawing the lines
seconds_per_line = 0.1
elapsed = 0.0
slices = slice_screen(16)

# "slices" are the corners of each slice
# Get the lines from the four corners
lines = []
for s in slices:
    lines.extend(
        [
            (add_margin(s[0]), add_margin(s[1])),
            (add_margin(s[1]), add_margin(s[2])), 
            (add_margin(s[2]), add_margin(s[3])), 
            (add_margin(s[3]), add_margin(s[0]))
        ]
    )

running = True
while running:

    dt = clock.tick(60)/1000
    elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Line drawing
    total_progress = elapsed / seconds_per_line
    finished_lines = int(total_progress)
    current_progress = total_progress - finished_lines

    screen.fill((20, 20, 30))  # wipe the previous frame
    screen.blit(image, (add_margin((0, 0))))

    for i, line in enumerate(lines):
        # The line has been drawn already, so draw it
        if i < finished_lines:
            pygame.draw.lines(screen, (255, 255, 255), False, line, 2)
        # If this is the line we're working on now, we're going to 
        # draw its current progress
        elif i == finished_lines:
            start, end = line
            x_0, y_0 = start
            x_1, y_1 = end
            # This looks more complicated than it is
            # Basically, get the fraction of the line that's drawn
            # at the particular point in progress
            curr_x = ((x_1 - x_0) * current_progress) + x_0 
            curr_y = ((y_1 - y_0) * current_progress) + y_0 
            pygame.draw.line(screen, (255, 255, 255), start, 
                             (curr_x, curr_y), 2)
        else:
            break

    pygame.display.update() 

pygame.quit()
