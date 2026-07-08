import pygame
import time
import csv

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Merge Sort Visualizer")

# Colors
background_color = (40, 40, 40)
text_color = (255, 255, 255)
box_color = (120, 120, 120)
partition_color = (70, 130, 180)  # Blue for partitions
merge_color = (255, 70, 70)  # Red for elements in active merge
sorted_color = (0, 174, 255)  # Blue for sorted elements
highlight_bg_color = (80, 80, 80)
comparison_color = (255, 135, 0)  # Yellow for elements in comparison
division_border_color = (50, 235, 60)  # Green border for active division

# Font setup
small_font = pygame.font.SysFont('Consolas', 18)
bold_font = pygame.font.SysFont('Consolas', 31, bold=True)

# Box dimensions
box_width = 70
box_height = 70

# Merge Sort Pseudocode
merge_sort_pseudocode = [
    "mergeSort(arr, left, right)",
    "  if left < right",
    "    mid = (left + right) // 2",
    "    mergeSort(arr, left, mid)",
    "    mergeSort(arr, mid + 1, right)",
    "    merge(arr, left, mid, right)"
]

merge_pseudocode = [
    "merge(arr, left, mid, right)",
    "  i = left, j = mid + 1, k = left",
    "  while i <= mid and j <= right",
    "    if arr[i] <= arr[j]",
    "      temp[k++] = arr[i++]",
    "    else",
    "      temp[k++] = arr[j++]",
    "  while i <= mid",
    "    temp[k++] = arr[i++]",
    "  while j <= right",
    "    temp[k++] = arr[j++]"
]

# Track statistics
num_partitions = 0
num_merges = 0

def draw_code(highlight_line, merge_highlight_line=None):
    y_offset = 20
    margin = 30
    for idx, line in enumerate(merge_sort_pseudocode):
        if idx == highlight_line:
            pygame.draw.rect(screen, highlight_bg_color, (margin, y_offset, 350, 20))
        color = text_color
        code_text = small_font.render(line, True, color)
        screen.blit(code_text, (margin + 5, y_offset))
        y_offset += 30
    
    # Draw merge pseudocode to the right of merge sort pseudocode
    y_offset = 30
    merge_margin = 470
    for idx, line in enumerate(merge_pseudocode):
        if idx == merge_highlight_line:
            pygame.draw.rect(screen, highlight_bg_color, (merge_margin, y_offset, 350, 20))
        color = text_color
        code_text = small_font.render(line, True, color)
        screen.blit(code_text, (merge_margin + 5, y_offset))
        y_offset += 20

def draw_array(array, left, right, mid=-1, sorted_indices=[], i=-1, j=-1, k=-1):
    """Draws the array with colored partitions and optional highlighting for merging steps."""
    spacing = 80
    start_x = (screen_width - (len(array) * spacing)) // 2 - 25
    base_y = 350

    # Draw array indices above the boxes, adjusted for spacing
    for idx in range(len(array)):
        x = start_x + idx * spacing
        # Adjust index positioning based on additional spacing
        if idx > left - 1:
            x += 25
        if idx >= right + 1:
            x += 25
        
        index_text = small_font.render(str(idx), True, text_color)
        text_rect = index_text.get_rect(center=(x + box_width // 2, base_y - 30))
        screen.blit(index_text, text_rect)

    for idx, num in enumerate(array):
        x = start_x + idx * spacing
        if idx > left - 1:
            x += 25
        if idx >= right + 1:
            x += 25

        # Determine color based on position and merge step
        color = sorted_color if idx in sorted_indices else (
            merge_color if left <= idx <= right else box_color
        )
        if idx == i or idx == j:
            color = comparison_color
        if idx == k:
            color = sorted_color

        pygame.draw.rect(screen, color, (x, base_y, box_width, box_height))
        num_text = bold_font.render(str(num), True, text_color)
        text_rect = num_text.get_rect(center=(x + box_width // 2, base_y + box_height // 2))
        screen.blit(num_text, text_rect)

        # Draw triangle pointers for i and j, adjusted for spacing
        if idx == i:
            pygame.draw.polygon(screen, comparison_color, [(x + box_width // 2 - 10, base_y + 120),
                                                             (x + box_width // 2 + 10, base_y + 120),
                                                             (x + box_width // 2, base_y + 100)])
        if idx == j:
            pygame.draw.polygon(screen, comparison_color, [(x + box_width // 2 - 10, base_y + 120),
                                                             (x + box_width // 2 + 10, base_y + 120),
                                                             (x + box_width // 2, base_y + 100)])

    # Draw a green border around the current division
    pygame.draw.rect(screen, division_border_color, 
                     (start_x + left * spacing + 10, base_y - 15, 
                      (right - left + 1) * spacing + 20, box_height + 30), 4)



def merge_animation(array, temp_array, left, right, mid):
    """Animates the merge process with detailed steps within merging."""
    global num_merges
    num_merges += 1
    temp = temp_array[left:right+1]
    i, j, k = left, mid + 1, left
    sorted_indices = []

    while i <= mid and j <= right:
        screen.fill(background_color)
        draw_code(5, merge_highlight_line=2)
        draw_array(array, left, right, mid, sorted_indices, i=i, j=j, k=k)
        
        if temp_array[i] <= temp_array[j]:
            temp[k - left] = temp_array[i]
            sorted_indices.append(i)
            i += 1
        else:
            temp[k - left] = temp_array[j]
            sorted_indices.append(j)
            j += 1
        k += 1
        
        display_stats(left, right)
        draw_key()
        pygame.display.update()
        time.sleep(0.4)

    while i <= mid:
        screen.fill(background_color)
        draw_code(5, merge_highlight_line=6)
        draw_array(array, left, right, mid, sorted_indices, i=i, k=k)
        temp[k - left] = temp_array[i]
        sorted_indices.append(i)
        i += 1
        k += 1
        display_stats(left, right)
        draw_key()
        pygame.display.update()
        time.sleep(0.4)

    while j <= right:
        screen.fill(background_color)
        draw_code(5, merge_highlight_line=8)
        draw_array(array, left, right, mid, sorted_indices, j=j, k=k)
        temp[k - left] = temp_array[j]
        sorted_indices.append(j)
        j += 1
        k += 1
        display_stats(left, right)
        draw_key()
        pygame.display.update()
        time.sleep(0.4)

    for idx, value in enumerate(temp):
        array[left + idx] = value

def merge_sort_visual(array, left, right):
    """Recursive merge sort visualization function."""
    global num_partitions
    if left < right:
        num_partitions += 1
        mid = (left + right) // 2
        merge_sort_visual(array, left, mid)
        merge_sort_visual(array, mid + 1, right)
        merge(array, left, mid, right)

def merge(array, left, mid, right):
    temp_array = array.copy()
    merge_animation(array, temp_array, left, right, mid)
    draw_final_sorted(array, left, right)

def draw_final_sorted(array, left, right):
    """Highlights the final sorted section after merging."""
    screen.fill(background_color)
    draw_code(-1)
    draw_array(array, left, right, sorted_indices=range(left, right+1))
    display_stats(left, right, sorted=True)
    draw_key()
    pygame.display.update()
    time.sleep(0.5)

def display_stats(left, right, sorted=False):
    """Displays statistics and current partition info at the bottom of the screen."""
    margin = 30
    margin1 = screen_width - 280
    margin2 = 470
    current_left_text = small_font.render(f"Current Left  : {left}", True, text_color)
    current_right_text = small_font.render(f"Current Right : {right}", True, text_color)
    partitions_text = small_font.render(f"Number of Partitions : {num_partitions}", True, text_color)
    merges_text = small_font.render(f"Number of Merges     : {num_merges}", True, text_color)
    sorted_text = small_font.render(f"Sorted : {'Yes' if sorted else 'No'}", True, text_color)
    time_complexity_text = small_font.render("Time Complexity: O(log n)", True, text_color)

    # Position the Current Left/Right above the Partitions/Merges/Sorted fields
    screen.blit(current_left_text, (margin, screen_height - 90))
    screen.blit(current_right_text, (margin, screen_height - 60))
    screen.blit(time_complexity_text, (margin2, screen_height - 60))
    screen.blit(partitions_text, (margin1, screen_height - 120))
    screen.blit(merges_text, (margin1, screen_height - 90))
    screen.blit(sorted_text, (margin1, screen_height - 60))

def draw_key():
    """Draws the color key for the visualization at the bottom right."""
    key_texts = [
        "Unsorted Element",
        "In Merge Comparison",
        "Currently Sorted",
        "Partition in Focus",
        "Active Merge Element"
    ]
    key_colors = [box_color, comparison_color, sorted_color, division_border_color, merge_color]
    x_offset = screen_width - 280
    y_offset = 60

    key_text1 = small_font.render("KEY", True, text_color)
    screen.blit(key_text1, (x_offset + 90, y_offset - 35))

    for i, (text, color) in enumerate(zip(key_texts, key_colors)):
        pygame.draw.rect(screen, color, (x_offset, y_offset + i * 32, 20, 20))
        key_text = small_font.render(text, True, text_color)
        screen.blit(key_text, (x_offset + 30, y_offset + i * 32))

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

# Main function to start visualization
def main():
    array = load_array_from_csv()
    screen.fill(background_color)
    draw_array(array, 0, len(array) - 1)
    pygame.display.update()
    merge_sort_visual(array, 0, len(array) - 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
