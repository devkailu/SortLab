import pygame
import time
import csv

pygame.init()

screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bubble Sort Visualizer")

background_color = (40, 40, 40)
text_color = (255, 255, 255)
box_color = (110, 110, 110)
highlight_color = (50, 235, 60)
swap_color = (255, 100, 100)
sorted_color = (0, 174, 255)
highlight_bg_color = (80, 80, 80)

small_font = pygame.font.SysFont('Consolas', 18)
bold_font = pygame.font.SysFont('Consolas', 31, bold=True)  # Increased by 3 points
large_font = pygame.font.SysFont('Consolas', 32, bold=True)

bubble_sort_pseudocode = [
    "bubbleSort(arr, n)",
    "  for i = 0 to n - 2",
    "    swapped = false",
    "    for j = 0 to n - i - 2",
    "      if arr[j] > arr[j + 1]",
    "        swap arr[j] with arr[j + 1]",
    "        swapped = true",
    "    if swapped is false break"
]

def draw_code(highlight_line):
    y_offset = 30
    margin = 30
    for idx, line in enumerate(bubble_sort_pseudocode):
        if idx == highlight_line:
            pygame.draw.rect(screen, highlight_bg_color, (margin, y_offset, 400, 20))
        color = text_color
        code_text = small_font.render(line, True, color)
        screen.blit(code_text, (margin + 5, y_offset))
        y_offset += 25

def draw_array(array, i=-1, j=-1, swap=False, sorted_indices=[]):
    spacing = 80
    box_width = 70
    box_height = 70
    margin = 10
    array_width = len(array) * spacing
    start_x = (screen_width - array_width) // 2

    base_y = 350 

    for idx, num in enumerate(array):
        x = start_x + idx * spacing
        color = sorted_color if idx in sorted_indices or sorted_indices == list(range(len(array))) else box_color
        if idx == j or idx == j + 1:
            color = swap_color if swap else highlight_color
        color = sorted_color if idx in sorted_indices or sorted_indices == list(range(len(array))) else color

        pygame.draw.rect(screen, color, (x, base_y, box_width, box_height))
        num_text = bold_font.render(str(num), True, text_color)
        text_rect = num_text.get_rect(center=(x + box_width // 2, base_y + box_height // 2))
        screen.blit(num_text, text_rect)

        if idx == j:
            pygame.draw.polygon(screen, highlight_color, [
                (x + 30, base_y + box_height + 10), 
                (x + 20, base_y + box_height + 30), 
                (x + 40, base_y + box_height + 30)
            ])


def swap_animation(array, j, i, sorted_indices):
    x1 = (screen_width - len(array) * 80) // 2 + j * 80
    x2 = x1 + 80
    y = 350

    spacing = 80
    box_width = 70
    box_height = 70
    margin = 10
    array_width = len(array) * spacing
    start_x = (screen_width - array_width) // 2

    base_y = 350  

    for step in range(21):  
        offset = 4 * step
        screen.fill(background_color)
        draw_code(5)
        for idx, num in enumerate(array):
            x = start_x + idx * spacing
            
            if idx == j:
                pygame.draw.rect(screen, swap_color, (x1 + offset, y, box_width, box_height))
                num_text = bold_font.render(str(array[j]), True, text_color)
                text_rect = num_text.get_rect(center=(x1 + offset + box_width // 2, y + box_height // 2))
                screen.blit(num_text, text_rect)
            elif idx == j + 1:
                pygame.draw.rect(screen, swap_color, (x2 - offset, y, box_width, box_height))
                num_text = bold_font.render(str(array[j + 1]), True, text_color)
                text_rect = num_text.get_rect(center=(x2 - offset + box_width // 2, y + box_height // 2))
                screen.blit(num_text, text_rect)
            else:
                color = sorted_color if idx in sorted_indices else box_color
                pygame.draw.rect(screen, color, (x, y, box_width, box_height))
                num_text = bold_font.render(str(num), True, text_color)
                text_rect = num_text.get_rect(center=(x + box_width // 2, y + box_height // 2))
                screen.blit(num_text, text_rect)

        draw_current_info(i, j, array, num_passes, num_swaps, sorted=False)
        draw_key()
        pygame.display.update()
        time.sleep(0.03)

def draw_current_info(i, j, array, num_passes, num_swaps, sorted):
    margin = 30
    current_i_text = small_font.render(f"Current  i        : {i}", True, text_color)
    current_j_text = small_font.render(f"Current  j        : {j}", True, text_color)
    comparison_text = small_font.render(f"arr[j] > arr[j+1] : {array[j] > array[j+1]}", True, text_color)

    screen.blit(current_i_text, (margin, screen_height - 100))
    screen.blit(current_j_text, (margin, screen_height - 70))
    screen.blit(comparison_text, (margin, screen_height - 40))

    passes_text = small_font.render(f"Number of passes : {num_passes}", True, text_color)
    swaps_text = small_font.render(f"Number of swaps  : {num_swaps}", True, text_color)
    sorted_text = small_font.render(f"Sorted : {'Yes' if sorted else 'No'}", True, text_color)

    time_complexity_text = small_font.render("Time Complexity: O(n^2)", True, text_color)
    screen.blit(time_complexity_text, (490, screen_height - 40))

    screen.blit(passes_text, (screen_width - 250, screen_height - 100))
    screen.blit(swaps_text, (screen_width - 250, screen_height - 70))
    screen.blit(sorted_text, (screen_width - 250, screen_height - 40))

def draw_key():
    key_label = small_font.render("KEY", True, text_color)
    screen.blit(key_label, (screen_width - 190, 20))

    key_texts = ["Unsorted Element", "Currently in Comparison", "Undergoing Swap", "Sorted Element"]
    key_colors = [box_color, highlight_color, swap_color, sorted_color]
    y_offset = 50

    for i, (text, color) in enumerate(zip(key_texts, key_colors)):
        pygame.draw.rect(screen, color, (screen_width - 300, y_offset, 30, 30))
        key_text = small_font.render(text, True, text_color)
        screen.blit(key_text, (screen_width - 260, y_offset + 5))
        y_offset += 40

def bubble_sort_visual(array):
    global num_passes, num_swaps
    n = len(array)
    num_passes = 0
    num_swaps = 0
    sorted_indices = []

    for i in range(n - 1):
        swapped = False
        num_passes += 1
        for j in range(n - i - 1):
            screen.fill(background_color)
            draw_array(array, i, j, sorted_indices=sorted_indices)
            draw_code(4)
            draw_current_info(i, j, array, num_passes, num_swaps, sorted=False)
            draw_key()

            pygame.display.update()
            time.sleep(0.5)

            if array[j] > array[j + 1]:
                num_swaps += 1
                draw_code(5)
                swap_animation(array, j, i, sorted_indices)
                array[j], array[j + 1] = array[j + 1], array[j] 
                swapped = True

            pygame.display.update()
            time.sleep(0.5)

        sorted_indices.append(n - i - 1)
        if not swapped:
            draw_code(7)
            draw_current_info(i, j, array, num_passes, num_swaps, sorted=True)
            pygame.display.update()
            break

    for idx in range(n):
        sorted_indices.append(idx)  

    screen.fill(background_color)
    draw_array(array, sorted_indices=sorted_indices) 
    draw_key()
    pygame.display.update()
    time.sleep(0.1)  

    draw_current_info(i, j, array, num_passes, num_swaps, sorted=True)
    draw_array(array, i=-1, j=-1, sorted_indices=sorted_indices)
    draw_code(-1) 
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

def load_array_from_csv(filename="input_array.csv"):
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

array = load_array_from_csv()

screen.fill(background_color)
draw_array(array)
draw_key()
draw_code(-1)
pygame.display.update()

bubble_sort_visual(array)

