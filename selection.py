import pygame
import time
import csv

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Selection Sort Visualizer")

# Colors
background_color = (40, 40, 40)
text_color = (255, 255, 255)
box_color = (110, 110, 110)
highlight_color = (50, 235, 60)
swap_color = (255, 100, 100)
sorted_color = (0, 174, 255)
highlight_bg_color = (80, 80, 80)
min_index_color = (255, 165, 0)  # Orange color for min index

# Font setup
small_font = pygame.font.SysFont('Consolas', 18)
bold_font = pygame.font.SysFont('Consolas', 31, bold=True)
large_font = pygame.font.SysFont('Consolas', 32, bold=True)

# Selection Sort Pseudocode
selection_sort_pseudocode = [
    "selectionSort(arr, n)",
    "  for i = 0 to n - 1",
    "    min_index = i",
    "    for j = i + 1 to n - 1",
    "      if arr[j] < arr[min_index]",
    "        min_index = j",
    "    swap arr[i] with arr[min_index]"
]

def draw_code(highlight_line):
    """Draws the pseudocode with a highlight on the specified line."""
    y_offset = 30
    margin = 30
    for idx, line in enumerate(selection_sort_pseudocode):
        if idx == highlight_line:
            pygame.draw.rect(screen, highlight_bg_color, (margin, y_offset, 400, 20))
        color = text_color
        code_text = small_font.render(line, True, color)
        screen.blit(code_text, (margin + 5, y_offset))
        y_offset += 25

def draw_array(array, i=-1, j=-1, min_index=-1, swap=False, sorted_indices=[]):
    """Draws the array of integers as boxes with optional highlighting."""
    spacing = 80
    box_width = 70
    box_height = 70
    margin = 10
    array_width = len(array) * spacing
    start_x = (screen_width - array_width) // 2

    base_y = 350

    for idx, num in enumerate(array):
        x = start_x + idx * spacing
        color = box_color  # Default color for unsorted elements
        
        # Color priority: min index > i/j
        if idx in sorted_indices:
            color = sorted_color
        elif swap and (idx == i or idx == min_index):
            color = swap_color
        elif idx == min_index:
            color = min_index_color
        elif idx == j or idx == i:
            color = highlight_color
        
        # Draw the rectangle for each number
        pygame.draw.rect(screen, color, (x, base_y, box_width, box_height))
        num_text = bold_font.render(str(num), True, text_color)
        text_rect = num_text.get_rect(center=(x + box_width // 2, base_y + box_height // 2))
        screen.blit(num_text, text_rect)

        # Draw the array index above each box
        index_text = small_font.render(str(idx), True, text_color)
        index_text_rect = index_text.get_rect(center=(x + box_width // 2, base_y - 20))
        screen.blit(index_text, index_text_rect)

        # Draw pointing triangles for i and j
        if idx == i or idx == j:
            pygame.draw.polygon(screen, highlight_color, [
                (x + 30, base_y + box_height + 10), 
                (x + 20, base_y + box_height + 30), 
                (x + 40, base_y + box_height + 30)
            ])

def swap_animation(array, i, min_index, sorted_indices, num_passes, num_swaps):
    """Animates the swapping of array[i] and array[min_index]."""
    x1 = (screen_width - len(array) * 80) // 2 + i * 80
    x2 = (screen_width - len(array) * 80) // 2 + min_index * 80
    y = 350

    for step in range(21):
        offset = 4 * step * (min_index - i)
        screen.fill(background_color)

        draw_code(6)  # Highlight swap line
        for idx, num in enumerate(array):
            x = (screen_width - len(array) * 80) // 2 + idx * 80
            if idx == i:
                pygame.draw.rect(screen, swap_color, (x1 + offset, y, 70, 70))
                num_text = bold_font.render(str(array[i]), True, text_color)
                text_rect = num_text.get_rect(center=(x1 + offset + 35, y + 35))
                screen.blit(num_text, text_rect)
            elif idx == min_index:
                pygame.draw.rect(screen, swap_color, (x2 - offset, y, 70, 70))
                num_text = bold_font.render(str(array[min_index]), True, text_color)
                text_rect = num_text.get_rect(center=(x2 - offset + 35, y + 35))
                screen.blit(num_text, text_rect)
            else:
                color = sorted_color if idx in sorted_indices else box_color
                pygame.draw.rect(screen, color, (x, y, 70, 70))
                num_text = bold_font.render(str(num), True, text_color)
                text_rect = num_text.get_rect(center=(x + 35, y + 35))
                screen.blit(num_text, text_rect)

            # Draw indices during swap animation
            index_text = small_font.render(str(idx), True, text_color)
            index_text_rect = index_text.get_rect(center=(x + 35, y - 20))
            screen.blit(index_text, index_text_rect)

        draw_current_info(i, -1, min_index, array, num_passes, num_swaps, sorted=False)
        draw_key()
        pygame.display.update()
        time.sleep(0.03)

def draw_current_info(i, j, min_index, array, num_passes, num_swaps, sorted):
    """Draws the current status information on the screen."""
    margin = 30
    current_i_text = small_font.render(f"Current  i        : {i}", True, text_color)
    current_j_text = small_font.render(f"Current  j        : {j}", True, text_color)
    min_index_text = small_font.render(f"Current min_index : {min_index}", True, text_color)

    screen.blit(current_i_text, (margin, screen_height - 100))
    screen.blit(current_j_text, (margin, screen_height - 70))
    screen.blit(min_index_text, (margin, screen_height - 40))

    passes_text = small_font.render(f"Number of passes : {num_passes}", True, text_color)
    swaps_text = small_font.render(f"Number of swaps  : {num_swaps}", True, text_color)
    sorted_text = small_font.render(f"Sorted : {'Yes' if sorted else 'No'}", True, text_color)

    screen.blit(passes_text, (screen_width - 250, screen_height - 100))
    screen.blit(swaps_text, (screen_width - 250, screen_height - 70))
    screen.blit(sorted_text, (screen_width - 250, screen_height - 40))

    time_complexity_text = small_font.render("Time Complexity: O(n^2)", True, text_color)
    screen.blit(time_complexity_text, (490, screen_height - 40))

def draw_key():
    """Draws the color legend for the visualization."""
    key_label = small_font.render("KEY", True, text_color)
    screen.blit(key_label, (screen_width - 190, 20))

    key_texts = [
        "Unsorted Element",
        "i/j Index Element",
        "Min Index Element",
        "Undergoing Swap",
        "Sorted Element"
    ]
    key_colors = [box_color, highlight_color, min_index_color, swap_color, sorted_color]
    y_offset = 50

    for text, color in zip(key_texts, key_colors):
        pygame.draw.rect(screen, color, (screen_width - 300, y_offset, 30, 30))
        key_text = small_font.render(text, True, text_color)
        screen.blit(key_text, (screen_width - 260, y_offset + 5))
        y_offset += 40

def selection_sort_visual(array):
    """Visualizes the selection sort algorithm with animations."""
    global num_passes, num_swaps
    n = len(array)
    num_passes = 0
    num_swaps = 0
    sorted_indices = []

    for i in range(n - 1):
        min_index = i
        num_passes += 1
        for j in range(i + 1, n):
            screen.fill(background_color)
            draw_array(array, i, j, min_index, sorted_indices=sorted_indices)
            draw_code(4)
            draw_current_info(i, j, min_index, array, num_passes, num_swaps, sorted=False)
            draw_key()
            pygame.display.update()
            time.sleep(0.5)

            if array[j] < array[min_index]:
                min_index = j
                screen.fill(background_color)
                draw_array(array, i, j, min_index, sorted_indices=sorted_indices)
                draw_code(5)
                draw_current_info(i, j, min_index, array, num_passes, num_swaps, sorted=False)
                draw_key()
                pygame.display.update()
                time.sleep(0.5)

        # Swap if a new minimum is found
        if min_index != i:
            # Perform swap animation
            swap_animation(array, i, min_index, sorted_indices, num_passes, num_swaps)
            array[i], array[min_index] = array[min_index], array[i]
            num_swaps += 1

        # Mark the current index as sorted
        sorted_indices.append(i)

    # After the sorting loop, add this line to ensure the last index is marked as sorted
    sorted_indices.append(n - 1)  # Include the last element in the sorted list

    # Final display to show the sorted array
    screen.fill(background_color)
    draw_array(array, sorted_indices=sorted_indices)
    draw_current_info(n - 1, -1, -1, array, num_passes, num_swaps, sorted=True)
    draw_code(0)  # Highlight the first line for completion
    draw_key()
    pygame.display.update()
    time.sleep(2)  # Pause before closing

def read_array_from_csv(file_path):
    """Reads an array of integers from a CSV file."""
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        array = []
        for row in reader:
            array.extend(map(int, row))
    return array

def main():
    # Load array from CSV file
    array = read_array_from_csv('input_array.csv')

    # Start the selection sort visualization
    selection_sort_visual(array)

    # Wait for a quit event
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
