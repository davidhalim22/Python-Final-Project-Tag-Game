from pygame import *  # Importing all pygame modules
import os  # Importing os module for file path handling

init()  # Initialize Pygame

# Get screen information (maximum screen size)
info = display.Info()
MAX_WIDTH, MAX_HEIGHT = info.current_w, info.current_h  # Maximum screen width and height
WIDTH, HEIGHT = 1280, 720  # Set custom screen width and height
WIN = display.set_mode((WIDTH, HEIGHT), RESIZABLE)  # Create a Pygame window with the specified dimensions

# Path to background music
BACKGROUND_MUSIC = os.path.join('D:\Documents\Python Final Project\Assets\Music', 'BG SOUND 2.wav')

# Directory where game assets (images, sounds) are stored
ASSETS_DIR = r'D:\Documents\Python Final Project\Assets'

# Load background images for the game
BACKGROUND_IMAGE = image.load(os.path.join(ASSETS_DIR, 'background', 'space.jpg'))  # Main background
BACKGROUND_IMAGE_RECT = BACKGROUND_IMAGE.get_rect(center=(WIDTH / 2, HEIGHT / 2))  # Get rect for background position
BACKGROUND_START = image.load(os.path.join(ASSETS_DIR, 'background', 'background start.jpg'))  # Start screen background
BACKGROUND_START_RECT = BACKGROUND_START.get_rect(center=(WIDTH / 2, HEIGHT / 2))  # Get rect for start background position

# Sound effect file paths
CLICK_SOUND = os.path.join(ASSETS_DIR, 'Music', 'click_effect.mp3')  # Sound when clicking
GAME_OVER_SFX = os.path.join(ASSETS_DIR, 'Music', 'game-over-arcade.mp3')  # Game over sound effect
KNOCKBACK_SOUND = os.path.join(ASSETS_DIR, 'Music', 'hitting.mp3')  # Sound for player knockback

# Rocket sound effect file path
ROCKET_FX = os.path.join(ASSETS_DIR, 'Music', 'rocket-launch.mp3')

# Set Frames Per Second (FPS) for the game
FPS = 60

# Initialize variables for handling input (keyboard and mouse)
keys_pressed = key.get_pressed()  # Get the current state of all keys
mouse_pos = mouse.get_pos()  # Get the current position of the mouse
mouse_pressed = mouse.get_pressed()  # Get the current state of mouse buttons

# File paths for character images
blue_ship = os.path.join('D:\Documents\Python Final Project\Assets\Characters', 'player1.png')  # Player ship image
blue_ship_move = os.path.join('D:\Documents\Python Final Project\Assets\Characters', 'player1_move.png')  # Player ship moving image

red_ship = os.path.join('D:\Documents\Python Final Project\Assets\Characters', 'player2.png')  # Enemy ship image
red_ship_move = os.path.join('D:\Documents\Python Final Project\Assets\Characters', 'player2_move.png')  # Enemy ship moving image

# Font setup for text rendering
font1 = font.Font(None, 24)  # Default font with size 24
title_pixel_font = font.Font('D:\Documents\Python Final Project\Assets\public-pixel-font\PublicPixel-rv0pA.ttf', 72)  # Title font (pixel style)
menu_pixel_font = font.Font('D:\Documents\Python Final Project\Assets\public-pixel-font\PublicPixel-rv0pA.ttf', 50)  # Menu font (pixel style)
interface_pixel_font = font.Font('D:\Documents\Python Final Project\Assets\public-pixel-font\PublicPixel-rv0pA.ttf', 20)  # Interface font (pixel style)

# Character dimensions (width and height)
character_width, character_height = 75, 75  # Set the width and height for character images