from pygame import *
from variables import *
import terrrain_generator as TG
from math import *

init()

# Load images and scale them to the specified size
PLAYER = image.load(blue_ship).convert_alpha()
PLAYER = transform.scale(PLAYER, (character_width, character_height))
PMOVE = image.load(blue_ship_move).convert_alpha()
PMOVE = transform.scale(PMOVE, (character_width, character_height))

ENEMY = image.load(red_ship).convert_alpha()
ENEMY = transform.scale(ENEMY, (character_width, character_height))
EMOVE = image.load(red_ship_move).convert_alpha()
EMOVE = transform.scale(EMOVE, (character_width, character_height))

# Speed and initial positions
player_speed = 5  # Speed at which the player moves
enemy_push_speed = 10  # Speed at which the enemy pushes towards the player

player_rect = PLAYER.get_rect(center=(200, HEIGHT / 2))  # Set initial position of player
player_x, player_y = player_rect.x, player_rect.y  # Player's coordinates

player_angle = 0  # Player's initial rotation angle
target_angle = 0  # Target rotation angle for smooth rotation

enemy_angle = 0  # Enemy's initial rotation angle

enemy_rect = ENEMY.get_rect(center=(WIDTH - 200, HEIGHT / 2))  # Set initial position of enemy
enemy_x, enemy_y = enemy_rect.x, enemy_rect.y  # Enemy's coordinates

# Create masks for collision detection
player_mask = mask.from_surface(PLAYER)
player_image = player_mask.to_surface()

enemy_mask = mask.from_surface(ENEMY)
enemy_image = enemy_mask.to_surface()

# Set initial character and movement images
player_char = PLAYER
enemy_char = ENEMY
player_move = PMOVE
enemy_move = EMOVE

# Render tags for player and enemy
player_tag = font1.render('Player', True, 'white')
enemy_tag = font1.render('Enemy', True, 'red')

gravity = 0.5  # Gravity value for future use (not used in this snippet)

is_player_tag = False  # Flag indicating if player is "it"
is_enemy_tag = True  # Flag indicating if enemy is "it"


# Define Player class with methods to handle player-specific functionality
class Player:
    def __init__(self, player=player_char, player_movement=player_move, name_tag=player_tag, player_angle=player_angle, player_x=player_x, player_y=player_y):
        self.player = player
        self.player_movement = player_movement
        self.name_tag = name_tag
        self.player_angle = player_angle
        self.player_x = player_x
        self.player_y = player_y
    
    # Method to draw the player on the window
    def draw_player(self):
        rotated_image = transform.rotate(self.player, self.player_angle)  # Rotate player image
        rotated_rect = rotated_image.get_rect(center=(self.player_x + self.player.get_width() // 2, self.player_y + self.player.get_height() // 2))  # Set the position after rotation
        
        WIN.blit(rotated_image, rotated_rect.topleft)  # Draw the rotated player image
        name_player_rect = self.name_tag.get_rect(center=(self.player_x + 35, self.player_y))  # Position of player's name tag
        WIN.blit(self.name_tag, name_player_rect)  # Draw the name tag

# Define Enemy class with methods to handle enemy-specific functionality
class Enemy:
    def __init__(self, enemy=enemy_char, enemy_movement=enemy_move, name_tag=enemy_tag, enemy_angle=enemy_angle, enemy_x=enemy_x, enemy_y=enemy_y):
        self.enemy = enemy
        self.enemy_movement = enemy_movement
        self.name_tag = name_tag
        self.enemy_angle = enemy_angle
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
    
    # Method to draw the enemy on the window
    def draw_enemy(self):
        global enemy_char
        
        rotated_enemy = transform.rotate(self.enemy, self.enemy_angle)  # Rotate enemy image
        rotated_rect = rotated_enemy.get_rect(center=(self.enemy_x + self.enemy.get_width() // 2, self.enemy_y + self.enemy.get_height() // 2))  # Set the position after rotation
        
        WIN.blit(rotated_enemy, rotated_rect.topleft)  # Draw the rotated enemy image
        name_enemy_rect = self.name_tag.get_rect(center=(self.enemy_x + 35, self.enemy_y))  # Position of enemy's name tag
        WIN.blit(self.name_tag, name_enemy_rect)  # Draw the name tag

        enemy_char = ENEMY  # Set enemy character

    # Method to update enemy position based on player position
    def update_position(self, player_x, player_y):
        global enemy_x, enemy_y, enemy_angle, enemy_char
        
        # Draw borders without displaying them (likely used to detect boundaries)
        TG.border_right.draw_border(False)
        TG.border_left.draw_border(False)
        TG.border_top.draw_border(False)
        TG.border_bottom.draw_border(False)
        
        dx = player_x - self.enemy_x  # Difference in x-coordinate
        dy = player_y - self.enemy_y  # Difference in y-coordinate
        distance = (dx**2 + dy**2) ** 0.5  # Distance between player and enemy

        if is_enemy_tag:
            # Logic when enemy is "it"
            if distance > 0:  # If the enemy is not at the same position as the player
                move_x = (dx / distance) * player_speed  # Calculate movement in x-direction
                move_y = (dy / distance) * player_speed  # Calculate movement in y-direction
                
                if move_x != 0 or move_y != 0:
                    enemy_char = EMOVE  # Change to moving image
                
                enemy_x += move_x  # Update enemy's x-coordinate
                enemy_y += move_y  # Update enemy's y-coordinate
                
                target_angle = -degrees(atan2(dx, -dy))  # Calculate the angle the enemy needs to face
                enemy_angle = self._smooth_rotate(enemy_angle, target_angle)  # Smoothly rotate the enemy
        else:
            # Logic when enemy is not "it"
            if distance > 0:
                move_x = -(dx / distance) * player_speed  # Move away from the player
                move_y = -(dy / distance) * player_speed  # Move away from the player
                
                if move_x != 0 or move_y != 0:
                    enemy_char = EMOVE  # Change to moving image
                
                enemy_x += move_x  # Update enemy's x-coordinate
                enemy_y += move_y  # Update enemy's y-coordinate
                
                target_angle = -degrees(atan2(-dx, dy))  # Calculate the angle the enemy needs to face
                enemy_angle = self._smooth_rotate(enemy_angle, target_angle)  # Smoothly rotate the enemy

        # Keep enemy inside boundaries using minimum and maximum limits
        enemy_x = max(TG.border_left.border_rect.x, min(enemy_x, TG.border_right.border_rect.x - self.enemy.get_width()))
        enemy_y = max(TG.border_top.border_rect.y, min(enemy_y, TG.border_bottom.border_rect.y - self.enemy.get_height()))

    # Method for smooth rotation towards target angle
    def _smooth_rotate(self, current_angle, target_angle):
        current_angle %= 360  # Keep the angle within 0 to 360 degrees
        target_angle %= 360  # Keep the target angle within 0 to 360 degrees

        diff = (target_angle - current_angle + 360) % 360  # Difference between angles
        if diff > 180:
            diff -= 360  # Adjust if the difference is greater than 180 degrees

        if diff > 0:
            current_angle += min(diff, 10)  # Rotate towards target angle
        elif diff < 0:
            current_angle -= min(-diff, 10)  # Rotate towards target angle

        return current_angle % 360  # Return the updated angle

# Initialize player and enemy objects
player1 = Player(PLAYER, PMOVE, player_tag, player_angle, player_x, player_y)
enemy1 = Enemy(enemy_char, EMOVE, enemy_tag, enemy_angle, enemy_x, enemy_y)

# Handle player movement and enemy updates
def controller(keys_pressed):
    global player_x, player_y, target_angle, enemy_x, enemy_y, player_char
    
    moved = False
    
    # Check key presses and update player's position accordingly
    if keys_pressed[K_a] or keys_pressed[K_d] or keys_pressed[K_w] or keys_pressed[K_s]:
        moved = True
        if keys_pressed[K_a] and player_x > TG.border_left.border_rect.x - 10:  # Move LEFT
            player_x -= player_speed
            
            if keys_pressed[K_w]:
                target_angle = 45
            elif keys_pressed[K_s]:
                target_angle = 135
            else:
                target_angle = 90
            
        if keys_pressed[K_d] and player_x < TG.border_right.border_rect.x + 10 - PLAYER.get_width():  # Move RIGHT
            player_x += player_speed
            
            if keys_pressed[K_w]:
                target_angle = -45
            elif keys_pressed[K_s]:
                target_angle = -135
            else:
                target_angle = -90
            
        if keys_pressed[K_w] and player_y > TG.border_top.border_rect.y - 10:  # Move UP
            player_y -= player_speed
            
            if keys_pressed[K_d]:
                target_angle = -45
            elif keys_pressed[K_a]:
                target_angle = 45
            else:
                target_angle = 0
            
        if keys_pressed[K_s] and player_y < TG.border_bottom.border_rect.y + 10 - PLAYER.get_height():  # Move DOWN
            player_y += player_speed
            
            if keys_pressed[K_d]:
                target_angle = -135
            elif keys_pressed[K_a]:
                target_angle = 135
            else:
                target_angle = 180
    
    # Update enemy position and redraw window
    if moved:
        enemy1.update_position(player_x, player_y)
        rotation_animation()  # Animate rotation for the player
        draw_window(player_x, player_y, player_move, enemy_x, enemy_y, enemy_char)  # Draw updated positions
    else:
        mixer.music.stop()  # Stop music if player isn't moving
        enemy1.update_position(player_x, player_y)  # Update enemy position
        draw_window(player_x, player_y, player_char, enemy_x, enemy_y, enemy_char)  # Redraw window

# Handle player rotation animation
def rotation_animation():
    global player_angle, target_angle
    
    player_angle %= 360
    target_angle %= 360

    diff = (target_angle - player_angle + 360) % 360
    if diff > 180:
        diff -= 360

    if diff > 0:
        player_angle += 10
    elif diff < 0:
        player_angle -= 10

    player_angle %= 360

# Detect and handle collision between player and enemy
def collider():
    global player_char, enemy_char, player_move, enemy_move, player_x, player_y, enemy_x, enemy_y, is_player_tag, is_enemy_tag
    
    # Calculate overlap between player and enemy
    collision_offset = (enemy_x - player_x, enemy_y - player_y)
    overlap = player_mask.overlap(enemy_mask, collision_offset)
    
    if overlap:
        mixer.music.load(KNOCKBACK_SOUND)  # Play knockback sound effect
        mixer.music.play()
        knockback_strength = 100  # Set the knockback strength
        
        # Apply knockback effect based on player/enemy positions
        if player_x < enemy_x:
            enemy_x += knockback_strength
            player_x -= knockback_strength
        elif player_x > enemy_x:
            enemy_x -= knockback_strength
            player_x += knockback_strength
        
        if player_y < enemy_y:
            enemy_y += knockback_strength
            player_y -= knockback_strength
        elif player_y > enemy_y:
            enemy_y -= knockback_strength
            player_y += knockback_strength
        
        # Keep player and enemy within borders
        enemy_x = max(TG.border_left.border_rect.x, min(enemy_x, TG.border_right.border_rect.x - ENEMY.get_width()))
        enemy_y = max(TG.border_top.border_rect.y, min(enemy_y, TG.border_bottom.border_rect.y - ENEMY.get_height()))
        
        player_x = max(TG.border_left.border_rect.x, min(player_x, TG.border_right.border_rect.x - PLAYER.get_width()))
        player_y = max(TG.border_top.border_rect.y, min(player_y, TG.border_bottom.border_rect.y - PLAYER.get_height()))
        
        # Switch "it" status between player and enemy
        if is_player_tag:
            is_player_tag = False
            is_enemy_tag = True
            player_it()  # Update "it" status
        elif is_enemy_tag:
            is_player_tag = True
            is_enemy_tag = False
            player_it()  # Update "it" status

# Function to draw the window and update characters' positions
def draw_window(player_x, player_y, PLAYER, enemy_x, enemy_y, ENEMY):
    global player1, enemy1
    player1 = Player(PLAYER, PMOVE, player_tag, player_angle, player_x, player_y)
    enemy1 = Enemy(ENEMY, EMOVE, enemy_tag, enemy_angle, enemy_x, enemy_y)

    enemy1.draw_enemy()  # Draw the enemy
    player1.draw_player()  # Draw the player

# Function to switch the "it" tag between player and enemy
def player_it():
    global player_char, enemy_char, player_move, enemy_move, player_tag, enemy_tag
    
    if is_player_tag:
        player_tag = font1.render('Player', True, 'red')  # Change player tag color
        enemy_tag = font1.render('Enemy', True, 'white')  # Change enemy tag color
    
    else:
        player_tag = font1.render('Player', True, 'white')  # Change player tag color
        enemy_tag = font1.render('Enemy', True, 'red')  # Change enemy tag color