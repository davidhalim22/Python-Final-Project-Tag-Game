from pygame import *
import os
import math
from time import sleep
import characters
from variables import *
import game_start as GS
import terrrain_generator as TG
import time as tm
import random

init()
player_points = 0  # Player's initial score
enemy_points = 4  # Enemy's initial score
num = None  # Random number for determining tag

start_time = tm.time()  # Timer start time
timer_duration = 5  # Duration of the timer in seconds

display.set_caption("Space Tag")  # Set game window title

# Store initial positions of player and enemy
player_start_pos = characters.player_rect  # Initial player position
enemy_start_pos = characters.enemy_rect  # Initial enemy position

is_game_over = False  # Game over flag
running = True  # Main loop flag
play_game_over = True  # Game over sound flag

decider_text = 'You Won'  # Initial end-game text
decider_color = 'blue'  # Initial end-game text color

# Menu class for game UI
class Menu:
    def __init__(self, game_interface, coordinate_mask, size, colors, coordinate_text):
        self.game_interface = game_interface  # Menu text
        self.coordinate_mask = coordinate_mask  # Menu position
        self.size = size  # Menu size
        self.colors = colors  # Menu color
        self.coordinate_text = coordinate_text  # Text position
        self.menu_bar_rect = None  # Menu bar rectangle
        self.menu_bar_mask = None  # Menu bar mask

    def draw_menu(self):
        # Render menu text and draw menu bar
        interface_text = menu_pixel_font.render(self.game_interface, True, self.colors)
        interface_text_rect = interface_text.get_rect(center=(self.coordinate_text))
        menu_bar = Surface(self.size)  # Create menu bar surface
        menu_bar_rect = menu_bar.get_rect(center=(self.coordinate_mask))  # Set menu bar position
        menu_bar.fill(self.colors)  # Fill menu bar with color
        menu_bar_mask = mask.from_surface(menu_bar)  # Generate collision mask for menu bar
        
        WIN.blit(interface_text, interface_text_rect)  # Draw text onto window
        
        self.menu_bar_mask = menu_bar_mask  # Store menu bar mask
        self.menu_bar_rect = menu_bar_rect  # Store menu bar rectangle
    
    def collide(self, mouse_pos):
        # Check if the mouse is colliding with the menu bar
        collision_offset = (mouse_pos[0] - self.menu_bar_rect.x, mouse_pos[1] - self.menu_bar_rect.y)
        overlap = self.menu_bar_mask.overlap(self.menu_bar_mask, collision_offset)  # Check overlap
        return overlap

# Create restart and exit menus
restart_menu = Menu('Restart', (WIDTH/2 - 203, HEIGHT/2 + 27), (350, 50), 'blue', (WIDTH/2 - 200, HEIGHT/2 + 25))
exit_menu = Menu('Exit', (WIDTH/2 + 200, HEIGHT/2 + 27), (200, 50), 'blue', (WIDTH/2 + 203, HEIGHT/2 + 25))

def draw_window(keys_pressed):
    # Update character movement and draw terrain
    characters.controller(keys_pressed)  # Handle character controls
    TG.terrain()  # Draw terrain

def timer():
    # Timer function to display countdown and handle end of timer
    global start_time, timer_duration

    elapsed_time = tm.time() - start_time  # Calculate elapsed time
    time_left = max(0, timer_duration - elapsed_time)  # Time remaining, ensuring non-negative

    minutes, seconds = divmod(int(time_left), 60)  # Convert time to minutes and seconds
    timer_text = interface_pixel_font.render(f'{minutes:02}:{seconds:02}', True, 'white')  # Render timer text
    
    timer_text_rect = timer_text.get_rect(center=(WIDTH/2, 20))  # Position timer text
    WIN.blit(timer_text, timer_text_rect)  # Display timer text

    if time_left <= 0:  # Timer ends
        game_decider()  # Determine game state

def loading_zone(delay_seconds):
    # Display loading screen and update game state
    WIN.blit(BACKGROUND_IMAGE, BACKGROUND_IMAGE_RECT)  # Draw background image
    restart_text = interface_pixel_font.render("Loading...", True, 'white')  # Loading text
    restart_text_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  # Center text
    
    if characters.is_player_tag:  # If player is "it"
        enemy_point_alarm_text = menu_pixel_font.render(f"1+", True, 'red')
        enemy_point_alarm_text_rect = enemy_point_alarm_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
        WIN.blit(enemy_point_alarm_text, enemy_point_alarm_text_rect)
    else:  # If enemy is "it"
        player_point_alarm_text = menu_pixel_font.render(f"1+", True, 'blue')
        player_point_alarm_text_rect = player_point_alarm_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
        WIN.blit(player_point_alarm_text, player_point_alarm_text_rect)
    
    WIN.blit(restart_text, restart_text_rect)  # Display loading text
    display.update()

    sleep(delay_seconds)  # Pause for loading
    
    reset_game_state()  # Reset game state after loading

def reset_game_state():
    # Reset the game state variables and positions
    global start_time, is_game_over, play_game_over
    
    is_game_over = False  # Reset game over flag
    start_time = tm.time()  # Reset timer
    characters.player_x, characters.player_y = player_start_pos.x, player_start_pos.y  # Reset player position
    characters.enemy_x, characters.enemy_y = enemy_start_pos.x, enemy_start_pos.y  # Reset enemy position
    characters.player_angle = characters.enemy_angle = 0  # Reset angles
    play_game_over = True  # Allow game over sound again
    
    if num == 1:  # If player starts as "it"
        characters.is_player_tag = True
        characters.is_enemy_tag = False
        characters.player_tag = font1.render('Player', True, 'red')  # Highlight player as "it"
        characters.enemy_tag = font1.render('Enemy', True, 'white')
    elif num == 0:  # If enemy starts as "it"
        characters.is_player_tag = False
        characters.is_enemy_tag = True
        characters.player_tag = font1.render('Player', True, 'white')
        characters.enemy_tag = font1.render('Enemy', True, 'red')  # Highlight enemy as "it"
    

def interface():
    # Display scores for player and enemy
    player_score = interface_pixel_font.render(f'{player_points}', True, 'blue')  # Player score
    enemy_score = interface_pixel_font.render(f'{enemy_points}', True, 'red')  # Enemy score
    
    player_score_rect = player_score.get_rect(center=(20, 20))  # Player score position
    enemy_score_rect = enemy_score.get_rect(center=(WIDTH - 20, 20))  # Enemy score position
    
    WIN.blit(player_score, player_score_rect)  # Draw player score
    WIN.blit(enemy_score, enemy_score_rect)  # Draw enemy score

def game_decider():
    # Decide the game outcome and update scores
    global player_points, enemy_points, is_game_over, decider_text, decider_color
    
    if player_points < 5 or enemy_points < 5:  # If neither has reached max points
        if characters.is_player_tag:  # If player is "it"
            enemy_points += 1  # Enemy scores
        else:  # If enemy is "it"
            player_points += 1  # Player scores
            
        loading_zone(2)  # Show loading screen
            
    if player_points == 5 or enemy_points == 5:  # Check for game over
        if player_points == 5:  # Player wins
            decider_text = 'You Won'
            decider_color = 'blue'
            is_game_over = True
        elif enemy_points == 5:  # Enemy wins
            decider_text = 'You Lose'
            decider_color = 'red'
            is_game_over = True
    
def game_over(mouse_pressed, mouse_pos):
    # Handle game over screen interactions
    global is_game_over, start_time, player_points, enemy_points, running, play_game_over
    
    if play_game_over:  # Play game over sound once
        mixer.music.load(GAME_OVER_SFX)
        mixer.music.play()
        play_game_over = False
    
    game_over_image = image.load(os.path.join(ASSETS_DIR, 'Menu', 'game over.png'))  # Load game over image
    game_over_image = transform.scale(game_over_image, (300, 300))  # Resize image
    game_over_image_rect = game_over_image.get_rect(center=(WIDTH/2, HEIGHT/2 - 200))  # Position image
    
    game_decider_text = menu_pixel_font.render(decider_text, True, decider_color)  # Display win/lose text
    game_decider_text_rect = game_decider_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 200))  # Position text
    
    WIN.blit(game_over_image, game_over_image_rect)  # Draw game over image
    WIN.blit(game_decider_text, game_decider_text_rect)  # Draw win/lose text
    
    restart_menu.draw_menu()  # Draw restart menu
    exit_menu.draw_menu()  # Draw exit menu
    
    if restart_menu.collide(mouse_pos):  # If mouse over restart
        restart_menu.colors = 'white'  # Highlight menu
        if mouse_pressed[0]:  # If clicked
            mixer.music.load(CLICK_SOUND)  # Play click sound
            mixer.music.play()
            start_time = tm.time()  # Reset timer
            reset_game_state()  # Reset game state
            player_points = 0  # Reset scores
            enemy_points = 0
            is_game_over = False  # Exit game over state
    elif exit_menu.collide(mouse_pos):  # If mouse over exit
        exit_menu.colors = 'white'  # Highlight menu
        if mouse_pressed[0]:  # If clicked
            mixer.music.load(CLICK_SOUND)  # Play click sound
            mixer.music.play()
            running = False  # Exit game
    
    if not exit_menu.collide(mouse_pos):  # Reset exit menu color
        exit_menu.colors = 'blue'
    if not restart_menu.collide(mouse_pos):  # Reset restart menu color
        restart_menu.colors = 'blue'
    
def main():
    # Main game loop
    global WIN, num, running, start_time
    
    clock = time.Clock()  # Create game clock
    
    GS.main_menu()  # Display main menu
    start_time = tm.time()  # Start timer
    running = GS.game_run  # Set game running state
    
    mixer.music.load(BACKGROUND_MUSIC)  # Load background music
    mixer.music.set_volume(0.2)  # Set volume
    mixer.music.play(-1)  # Loop music
    mixer.music.stop()  # Stop music immediately (to be restarted elsewhere)
    
    while running:  # Main game loop
        clock.tick(FPS)  # Maintain FPS
        for events in event.get():  # Process events
            if events.type == QUIT:  # Quit event
                running = False
            
            if events.type == VIDEORESIZE:  # Handle window resizing
                WIN = display.set_mode(events.size, RESIZABLE)  # Adjust window size

        num = random.randint(0, 1)  # Randomize tag start
        keys_pressed = key.get_pressed()  # Get pressed keys
        mouse_pressed = mouse.get_pressed()  # Get mouse clicks
        mouse_pos = mouse.get_pos()  # Get mouse position
        
        WIN.blit(BACKGROUND_IMAGE, BACKGROUND_IMAGE_RECT)  # Draw background
        
        if is_game_over:  # If game is over
            game_over(mouse_pressed, mouse_pos)  # Handle game over
        else:  # Game is running
            timer()  # Update timer
            interface()  # Display scores
            draw_window(keys_pressed)  # Update game state
            characters.collider()  # Check collisions
        display.update()  # Update display

# Run the game
main()
quit()