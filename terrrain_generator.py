from pygame import *
from variables import *

init()

# Class for creating and drawing borders
class Border:
    def __init__(self, size, coordinate, colors):
        self.size = size  # Size of the border (width, height)
        self.coordinate = coordinate  # Position of the border (center of the rectangle)
        self.colors = colors  # Color of the border
        self.border_mask = None  # Initialize mask for border collision detection (if needed)
        self.border_rect = None  # Rectangle representation of the border
    
    # Method to draw the border
    def draw_border(self, is_border_draw=True):
        border = Surface(self.size)  # Create a surface for the border with the given size
        border_rect = border.get_rect(center=(self.coordinate))  # Set the position of the border
        border.fill(self.colors)  # Fill the border surface with the specified color
        border_mask = mask.from_surface(border)  # Create a mask from the surface (used for collision detection)
        border_image = border_mask.to_surface()  # Convert the mask back into a surface
        self.border_mask = border_mask  # Store the mask for future use
        self.border_rect = border_rect  # Store the rectangle for future use
        
        if is_border_draw:  # If the flag is set to True, draw the border to the screen
            WIN.blit(border_image, border_rect)  # Blit (draw) the border image on the window


# Create instances of the Border class for each border (top, bottom, left, right)
border_top = Border((1085, 5), (WIDTH / 2, 50), 'red')  # Top border
border_bottom = Border((1085, 5), (WIDTH / 2, HEIGHT - 50), 'red')  # Bottom border
border_left = Border((5, 615), (100, HEIGHT / 2), 'red')  # Left border
border_right = Border((5, 615), (WIDTH - 100, HEIGHT / 2), 'red')  # Right border


# Function to draw the entire terrain (all borders)
def terrain():
    border_top.draw_border()  # Draw top border
    border_bottom.draw_border()  # Draw bottom border
    border_left.draw_border()  # Draw left border
    border_right.draw_border()  # Draw right border
    display.update()  # Update the display to show the drawn borders