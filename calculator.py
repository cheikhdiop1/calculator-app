import pygame
import sys
from Cocoa import NSApplication

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 232, 321  # Updated height
TOP_MARGIN = 28  # Added margin to shift everything down
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

# Colors
BLACK = (34, 34, 34)
WHITE = (255, 255, 255)
DARK_GRAY = (56, 56, 56)
GRAY = (89, 89, 89)
ORANGE = (255, 158, 6)

# Fonts
font_path = "Fonts/SF-Pro.ttf"
font_path2 = "Fonts/SF-Pro-Text-Thin.otf"
font_path3 = "Fonts/SF-Pro.ttf"
default_font_size = 22
top_operator_font_size = 19  # Slightly larger font size for operators and special buttons
side_operator_font_size = 26
top_number_font_size = 48

# Load fonts
default_font = pygame.font.Font(font_path, default_font_size)
top_operator_font = pygame.font.Font(font_path, top_operator_font_size)
side_operator_font = pygame.font.Font(font_path3, side_operator_font_size)
top_number_font = pygame.font.Font(font_path2, top_number_font_size)

# Calculator variables
current_input = "0"
result = ""
operation = ""
selected_operator = None  # Variable to track the selected operator button
replace_input = False  # Flag to indicate if input should replace the current display

# Button setup
buttons = [
    {"label": "AC", "pos": (0, 53 + TOP_MARGIN), "size": (56, 47.5)},
    {"label": "+/-", "pos": (57, 53 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "%", "pos": (115, 53 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "÷", "pos": (173, 53 + TOP_MARGIN), "size": (59, 47.5)},
    {"label": "7", "pos": (0, 101 + TOP_MARGIN), "size": (56, 47.5)},
    {"label": "8", "pos": (57, 101 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "9", "pos": (115, 101 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "×", "pos": (173, 101 + TOP_MARGIN), "size": (59, 47.5)},
    {"label": "4", "pos": (0, 149 + TOP_MARGIN), "size": (56, 47.5)},
    {"label": "5", "pos": (57, 149 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "6", "pos": (115, 149 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "-", "pos": (173, 149 + TOP_MARGIN), "size": (59, 47.5)},
    {"label": "1", "pos": (0, 197 + TOP_MARGIN), "size": (56, 47.5)},
    {"label": "2", "pos": (57, 197 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "3", "pos": (115, 197 + TOP_MARGIN), "size": (57, 47.5)},
    {"label": "+", "pos": (173, 197 + TOP_MARGIN), "size": (59, 47.5)},
    {"label": "0", "pos": (0, 245 + TOP_MARGIN), "size": (114, 48)},
    {"label": ".", "pos": (115, 245 + TOP_MARGIN), "size": (57, 48)},
    {"label": "=", "pos": (173, 245 + TOP_MARGIN), "size": (59, 48)}
]

def draw_buttons():
    for button in buttons:
        label = button["label"]
        pos = button["pos"]
        size = button["size"]

        # Set the button's size to be smaller when selected
        if label in "+-×÷" and label == selected_operator:
            size = (size[0] - 2, size[1] - 2)  # Reduce size by 1 on each side
            pos = (pos[0] + 1, pos[1] + 1)  # Adjust position to center the smaller button
            # Draw the outline slightly larger than the button
            outline_rect = pygame.Rect(pos[0] - 1, pos[1] - 1, size[0] + 2, size[1] + 2)
            pygame.draw.rect(win, BLACK, outline_rect)

        rect = pygame.Rect(pos, size)

        # Set color and font based on button type
        if label == "AC" and (current_input != "0" or result):
            label = "C"
        if label in ["AC", "+/-", "%", "C"]:
            color = DARK_GRAY
            font = top_operator_font  # Larger font for these buttons
        elif label in "+-×÷=":
            color = ORANGE
            font = side_operator_font  # Larger font for operators
        else:
            color = GRAY
            font = default_font  # Default font for numbers

        # Draw button
        pygame.draw.rect(win, color, rect)
        text = font.render(label, True, WHITE)
        win.blit(text, (pos[0] + (size[0] - text.get_width()) // 2, pos[1] + (size[1] - text.get_height()) // 2))

def draw_text():
    display_text = current_input if current_input else result
    if display_text.endswith(".0"):
        display_text = display_text[:-2]  # Remove trailing ".0" for whole numbers
    max_width = WIDTH - 20  # Define the maximum width for the text display area
    font_size = top_number_font_size
    font = pygame.font.Font(font_path2, font_size)
    text_surface = font.render(display_text, True, WHITE)
    y = -6 + TOP_MARGIN  # Adjust the y-position based on the TOP_MARGIN

    # Adjust the font size if the text is too long
    while text_surface.get_width() > max_width and font_size > 6:  # Set a minimum font size
        font_size -= 1
        y += 1
        font = pygame.font.Font(font_path2, font_size)
        text_surface = font.render(display_text, True, WHITE)

    # Right-align the text
    win.blit(text_surface, (WIDTH - text_surface.get_width() - 10, y))

def calculate():
    global current_input, result, operation, selected_operator, replace_input
    try:
        if operation:
            if operation == "+":
                result = str(float(result) + float(current_input))
            elif operation == "-":
                result = str(float(result) - float(current_input))
            elif operation == "×":
                result = str(float(result) * float(current_input))
            elif operation == "÷":
                result = str(float(result) / float(current_input))
            result = result.rstrip('0').rstrip('.') if '.' in result else result
        else:
            result = current_input
        current_input = ""
        selected_operator = None
    except ZeroDivisionError:
        result = "Error"
    replace_input = True  # Reset to true after calculation

def button_pressed(label):
    global current_input, result, operation, replace_input, selected_operator
    if label in "0123456789.":
        if replace_input:
            current_input = "" if label != "." else "0"  # Start fresh unless entering a decimal point
            replace_input = False
        if label == "." and "." in current_input:
            return  # Avoid multiple decimal points
        if current_input == "0" and label != ".":
            current_input = label  # Replace initial 0
        else:
            current_input += label
    elif label in "+-×÷":
        if current_input != "":
            if result != "":
                calculate()
            else:
                result = current_input
            current_input = ""
        operation = label
        selected_operator = label
        replace_input = True  # Set flag to replace input on next number press
    elif label == "=":
        if operation and current_input:
            calculate()
        operation = ""
        selected_operator = None
    elif label == "AC":
        if selected_operator:
            selected_operator = None  # Deselect the operator
        else:
            current_input, result, operation = "0", "", ""
            replace_input = False
    elif label == "+/-":
        if current_input:
            current_input = str(-float(current_input))
        elif result:
            result = str(-float(result))
    elif label == "%":
        if current_input:
            current_input = str(float(current_input) / 100)
        elif result:
            result = str(float(result) / 100)

# Force the application to front
NSApplication.sharedApplication().activateIgnoringOtherApps_(True)

# Main loop
running = True
while running:
    win.fill(BLACK)
    draw_buttons()
    draw_text()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                rect = pygame.Rect(button["pos"], button["size"])
                if rect.collidepoint(pos):
                    button_pressed(button["label"])

pygame.quit()
sys.exit()
