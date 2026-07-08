import pygame
import time
import csv

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Insertion Sort Visualizer")

# Colors
background_color = (40, 40, 40)
text_color = (255, 255, 255)
box_color = (110, 110, 110)
highlight_color = (50, 235, 60)
swap_color = (255, 100, 100)
sorted_color = (0, 174, 255)
highlight_bg_color = (80, 80, 80)
key_color = (255, 165, 0)

# Font setup
small_font = pygame.font.SysFont('Consolas', 18)
bold_font = pygame.font.SysFont('Consolas', 31, bold=True)

# Insertion Sort Pseudocode
insertion_sort_pseudocode = [
    "insertionSort(arr, n)",
    "  for i = 1 to n - 1",
    "    key = arr[i]",
    "    j = i - 1",
    "    while j >= 0 and arr[j] > key",
    "      arr[j + 1] = arr[j]",
    "      j = j - 1",
    "    arr[j + 1] = key"
]

def draw_code(highlight_line=-1):
    """Draws the pseudocode with a highlight on the specified line."""
    y_offset = 30
    margin = 30
    for idx, line in enumerate(insertion_sort_pseudocode):
        if idx == highlight_line:
            pygame.draw.rect(screen, highlight_bg_color, (margin, y_offset, 400, 20))
        color = text_color
        code_text = small_font.render(line, True, color)
        screen.blit(code_text, (margin + 5, y_offset))
        y_offset += 25

def draw_array(array, i=-1, j=-1, sorted_indices=[]):
    """Draws the array of integers as boxes with optional highlighting."""
    spacing = 80
    box_width = 70
    box_height = 70
    array_width = len(array) * spacing
    start_x = (screen_width - array_width) // 2
    base_y = 350

    for idx, num in enumerate(array):
        x = start_x + idx * spacing
        color = sorted_color if idx in sorted_indices else box_color
        if idx == j:
            color = highlight_color
        if idx == i:
            color = key_color
        pygame.draw.rect(screen, color, (x, base_y, box_width, box_height))
        num_text = bold_font.render(str(num), True, text_color)
        text_rect = num_text.get_rect(center=(x + box_width // 2, base_y + box_height // 2))
        screen.blit(num_text, text_rect)

        # Draw array index above each box
        index_text = small_font.render(str(idx), True, text_color)
        index_text_rect = index_text.get_rect(center=(x + box_width // 2, base_y - 20))
        screen.blit(index_text, index_text_rect)

        # Draw triangle pointer for the current comparison
        if idx == j:
            pygame.draw.polygon(screen, highlight_color, [
                (x + 35, base_y + box_height + 10),
                (x + 25, base_y + box_height + 30),
                (x + 45, base_y + box_height + 30)
            ])
        
        if idx == i:
            pygame.draw.polygon(screen, key_color, [
                (x + 35, base_y + box_height + 10),
                (x + 25, base_y + box_height + 30),
                (x + 45, base_y + box_height + 30)
            ])

def draw_key():
    """Draws the color key for the visualization."""
    key_label = small_font.render("KEY", True, text_color)
    screen.blit(key_label, (screen_width - 210, 20))

    key_texts = ["Unsorted Element", "j Index Element", "Current Key Value", "Sorted Element"]
    key_colors = [box_color, highlight_color, key_color, sorted_color]
    y_offset = 50

    for text, color in zip(key_texts, key_colors):
        pygame.draw.rect(screen, color, (screen_width - 300, y_offset, 30, 30))
        key_text = small_font.render(text, True, text_color)
        screen.blit(key_text, (screen_width - 260, y_offset + 5))
        y_offset += 40

def draw_current_info(i, j, passes, shifts, sorted):
    """Draws the current sorting information on the screen."""
    margin = 30
    current_i_text = small_font.render(f"Current i: {i}", True, text_color)
    current_j_text = small_font.render(f"Current j: {j}", True, text_color)
    passes_text = small_font.render(f"Number of passes: {passes}", True, text_color)
    shifts_text = small_font.render(f"Number of shifts: {shifts}", True, text_color)
    sorted_text = small_font.render(f"Sorted: {'Yes' if sorted else 'No'}", True, text_color)

    screen.blit(current_i_text, (margin, screen_height - 90))
    screen.blit(current_j_text, (margin, screen_height - 60))
    screen.blit(passes_text, (screen_width - 250, screen_height - 100))
    screen.blit(shifts_text, (screen_width - 250, screen_height - 70))
    screen.blit(sorted_text, (screen_width - 250, screen_height - 40))

    time_complexity_text = small_font.render("Time Complexity: O(n^2)", True, text_color)
    screen.blit(time_complexity_text, (470, screen_height - 40))

def insertion_sort_visual(array):
    """Visualizes the insertion sort algorithm with animations."""
    n = len(array)
    sorted_indices = [0]
    num_passes = 0
    num_shifts = 0

    for i in range(1, n):
        key = array[i]
        j = i - 1
        num_passes += 1
        screen.fill(background_color)
        draw_code(1)  # Highlight the start of the outer loop
        draw_array(array, i=i, j=j, sorted_indices=sorted_indices)
        draw_current_info(i, j, num_passes, num_shifts, sorted=False)
        draw_key()
        pygame.display.update()
        time.sleep(0.6)

        # Shifting elements to the right to make space for the key
        while j >= 0 and array[j] > key:
            screen.fill(background_color)
            array[j + 1] = array[j]
            num_shifts += 1
            draw_code(4)  # Highlight the condition check and shift step
            draw_array(array, i=i, j=j, sorted_indices=sorted_indices)
            draw_current_info(i, j, num_passes, num_shifts, sorted=False)
            draw_key()
            pygame.display.update()
            time.sleep(0.6)
            j -= 1

        # Placing the key at the correct position
        array[j + 1] = key
        sorted_indices.append(i)
        screen.fill(background_color)
        draw_code(5)  # Highlight the insertion step
        draw_array(array, i=i+1, j=-1, sorted_indices=sorted_indices)
        draw_current_info(i, -1, num_passes, num_shifts, sorted=False)
        draw_key()
        pygame.display.update()
        time.sleep(0.6)

    # Final display to show the sorted array
    screen.fill(background_color)
    draw_array(array, sorted_indices=list(range(n)))
    draw_current_info(n - 1, -1, num_passes, num_shifts, sorted=True)
    draw_code()  # Keep the pseudocode displayed without highlighting any line
    draw_key()
    pygame.display.update()
    time.sleep(2)  # Pause before closing

    # Display sorted state with pseudocode visible
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

def load_array_from_csv(filename="input_array.csv"):
    """Loads the array from a CSV file."""
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = [int(num) for num in row]
                return array
    except FileNotFoundError:
        print("CSV file not found. Please ensure 'input_array.csv' is in the same directory.")
        pygame.quit()
        exit()

def main():
    # Load array from CSV file
    array = load_array_from_csv()

    # Start the insertion sort visualization
    insertion_sort_visual(array)

if __name__ == "__main__":
    main()
