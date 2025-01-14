from pygame import *
from variables import * 

# Initialize Pygame
init()

# Frames per second
FPS = 60

# Render the game title text
GAME_TITLE = title_pixel_font.render('Space Tag', True, 'blue')

# Render the "Start" button text in two states (normal and highlighted)
START_GAME = menu_pixel_font.render('Start', True, 'blue')
WHITE_START_GAME = menu_pixel_font.render('Start', True, 'white')

# Render the "Quit" button text in two states (normal and highlighted)
EXIT_GAME = menu_pixel_font.render('Quit', True, 'blue')
WHITE_EXIT_GAME = menu_pixel_font.render('Quit', True, 'white')

# Define the positions for the game title and buttons
game_title_rect = GAME_TITLE.get_rect(center=(WIDTH / 2, HEIGHT / 9))
start_game_rect = START_GAME.get_rect(center=(WIDTH / 2, HEIGHT - 450))
exit_game_rect = EXIT_GAME.get_rect(center=(WIDTH / 2, HEIGHT - 296))

# Create masks for the "Start" button
start_mask = mask.from_surface(START_GAME)
start_image = start_mask.to_surface()

# Create a cursor surface for collision detection
mouse_cursor = Surface((10, 10))
mouse_cursor_rect = mouse_cursor.get_rect()
mouse_cursor.fill('white')
mouse_cursor_mask = mask.from_surface(mouse_cursor)

# Initialize button state variables
start_menu = START_GAME
exit_menu = EXIT_GAME



# Class for creating interactive menu boxes
class Box_menu:
    def __init__(self, size, coordinate, colors):
        self.size = size
        self.coordinate = coordinate
        self.colors = colors
        self.box_mask = None
        self.box_rect = None
    
    def draw_box(self):
        """
        Draw the menu box on the screen.
        """
        box = Surface(self.size)
        box_rect = box.get_rect(center=self.coordinate)
        box.fill(self.colors)
        box_mask = mask.from_surface(box)
        self.box_mask = box_mask
        self.box_rect = box_rect
    
    def collision(self, mouse_pos):
        """
        Check if the mouse cursor collides with the menu box.
        """
        collision_offset = (mouse_pos[0] - self.box_rect.x, mouse_pos[1] - self.box_rect.y)
        overlap = self.box_mask.overlap(self.box_mask, collision_offset)
        return overlap

# Create menu boxes for "Start" and "Quit" options
box1 = Box_menu((250, 60), (WIDTH / 2 - 2, HEIGHT - 445), 'white')  # Start box
box2 = Box_menu((200, 60), (WIDTH / 2 - 2, HEIGHT - 296), 'white')  # Quit box

# Initialize game state variables
running = True  # Whether the menu is running
game_run = True  # Whether the game should start

def main_menu():
    """
    Display the main menu screen and handle user interactions.
    """
    global running, WIN, game_run

    clock = time.Clock()  # Create a clock object for controlling frame rate

    while running:
        clock.tick(FPS)  # Limit the loop to run at FPS speed
        for events in event.get():  # Handle events
            if events.type == QUIT:  # Handle quit event
                running = False
                game_run = False

            if events.type == VIDEORESIZE:  # Handle window resize
                WIN = display.set_mode(events.size, RESIZABLE)
        
        # Get current mouse position and button states
        mouse_pos = mouse.get_pos()
        mouse_pressed = mouse.get_pressed()
        
        # Draw the background and game title
        WIN.blit(BACKGROUND_START, BACKGROUND_START_RECT)
        WIN.blit(GAME_TITLE, game_title_rect)
        
        # Draw the quit button box
        box2.draw_box()
        
        # Check interactions with "Start" and "Quit" buttons
        start(mouse_pos, mouse_pressed)
        exit(mouse_pos, mouse_pressed)
        
        # Update the display
        display.update()

def start(mouse_pos, mouse_pressed):
    """
    Handle interactions with the "Start" button.
    """
    global start_menu, game_run, running

    # Draw the "Start" button box
    box1.draw_box()
    WIN.blit(start_menu, start_game_rect)

    # Check for collision with the "Start" button
    if box1.collision(mouse_pos):
        start_menu = WHITE_START_GAME  # Highlight the button
        if mouse_pressed[0]:  # If left mouse button is clicked
            mixer.music.load(CLICK_SOUND)
            mixer.music.play()  # Play click sound
            game_run = True  # Start the game
            running = False  # Exit the menu loop
    else:
        start_menu = START_GAME  # Reset to normal state if no collision

def exit(mouse_pos, mouse_pressed):
    """
    Handle interactions with the "Quit" button.
    """
    global exit_menu, game_run, running

    # Draw the "Quit" button box
    box2.draw_box()
    WIN.blit(exit_menu, exit_game_rect)
    
    # Check for collision with the "Quit" button
    if box2.collision(mouse_pos):
        exit_menu = WHITE_EXIT_GAME  # Highlight the button
        if mouse_pressed[0]:  # If left mouse button is clicked
            mixer.music.load(CLICK_SOUND)
            mixer.music.play()  # Play click sound
            game_run = False  # Stop the game
            running = False  # Exit the menu loop
    else:
        exit_menu = EXIT_GAME  # Reset to normal state if no collision