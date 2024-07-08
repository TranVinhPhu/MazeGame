import pygame
import sys
import random
import os
pygame.init()

font = pygame.font.SysFont('calibri', 16)
start_time = pygame.time.get_ticks()
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Maze Game")
screen.fill((56, 56, 56))

pygame.mixer.init()
bg_sound_path = os.path.join(os.path.dirname(__file__), "sound", "BGSound.wav")
pygame.mixer.music.load(bg_sound_path)
pygame.mixer.music.play(-1)  # -1 means loop forever

# Load game icon
icon_path = os.path.join(os.path.dirname(__file__), "img", "maze.jpg")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# Load background image for the main menu
background_path = os.path.join(os.path.dirname(__file__), "img", "menu.jpg")
background_image = pygame.image.load(background_path)
background_image = pygame.transform.scale(background_image, (window_width, window_height))

image_move_path = os.path.join(os.path.dirname(__file__), "img", "arrows.png")
image = pygame.image.load(image_move_path)
image = pygame.transform.scale(image, (80, 80))
cell_size = 30
maze_width, maze_height = 610, 600
rows = maze_height // cell_size
cols = maze_width // cell_size


clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 99, 71)
green = (144, 238, 144)
blue = (135, 206, 250)
yellow = (255, 255, 0)

timer_font = pygame.font.SysFont('comicsansms', 24)

button_font = pygame.font.SysFont('comicsansms', 36)
play_button = pygame.Rect(window_width // 4, window_height // 2, window_width // 2, 50)
exit_button = pygame.Rect(window_width // 4, window_height // 2 + 70, window_width // 2, 50)
# Function to draw the main menu
def draw_main_menu():
    screen.blit(background_image, (0, 0))

    # Draw game title
    title_font = pygame.font.SysFont('comicsansms', 60)
    title_text = title_font.render("Maze Game", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(window_width // 2, window_height // 4))
    screen.blit(title_text, title_rect)

    # Draw play button
    play_button = pygame.Rect(window_width // 4, window_height // 2, window_width // 2, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    play_text = button_font.render("Play", True, (0, 0, 0))
    play_text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, play_text_rect)

    # Draw exit button
    exit_button = pygame.Rect(window_width // 4, window_height // 2 + 70, window_width // 2, 50)
    pygame.draw.rect(screen, (255, 0, 0), exit_button)
    exit_text = button_font.render("Exit", True, (0, 0, 0))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

# Function for the main menu loop
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        draw_main_menu()

if main_menu():
    maze = None
    player_pos = None
    goal_pos = None
    auto_mode = False
    def level_up():
        global maze, player_pos, auto_mode
        maze = create_maze(complexity_multiplier=2.5)  # Increase the complexity
        player_pos = [0, 0]
        auto_mode = False

    # Hàm tìm đường đi từ start đến end sử dụng DFS
    def dfs_path(start, end): #Thông
        stack = [(start, [start])]
        visited = set()

        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == end:
                    return path
                visited.add(vertex)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Up, down, left, right
                    nx, ny = vertex[0] + dx, vertex[1] + dy
                    if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:  # Check if the next position is a wall or not
                        neighbor = (nx, ny)
                        stack.append((neighbor, path + [neighbor]))
                        # Xử lý sự kiện nhấp chuột

    # Sử dụng hàm trong chế độ auto_mode
    def auto_run_to_goal():
        global player_pos

        path = dfs_path(tuple(player_pos), tuple(goal_pos))
        if path:
            next_step = path[1]  # Lấy bước tiếp theo từ đường đi
            player_pos = list(next_step)

    def auto_move_to_goal():
        global player_pos, goal_pos

        dx = goal_pos[0] - player_pos[0]
        dy = goal_pos[1] - player_pos[1]

        if dx != 0:
            player_pos[0] += 1 if dx > 0 else -1
        elif dy != 0:
            player_pos[1] += 1 if dy > 0 else -1

    ####################### TẠO MÊ CUNG BẰNG DFS ##########################
    def create_maze(complexity_multiplier=1.0):
        maze = [[1 for _ in range(cols)] for _ in range(rows)]
        def dfs(x, y):
            maze[x][y] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and maze[nx][ny] == 1
                    and random.random() < complexity_multiplier
                ):
                    maze[x + dx // 2][y + dy // 2] = 0
                    dfs(nx, ny)
        dfs(0, 0)
        maze[rows - 2][cols - 1] = 0
        return maze

    maze = create_maze()
    player_pos = [0, 0]
    goal_pos = [rows - 2, cols - 1]
    auto_mode = False

    def draw_message(message):
        font = pygame.font.SysFont('calibri', 24)
        text = font.render(message, True, white)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        screen.fill((56, 56, 56))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

    def create_button(x, y, width, height, color, text, action=None):
        font = pygame.font.SysFont('comicsansms', 14)
        text_surface = font.render(text, True, black)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_color = color
        border_color = (0, 0, 0)
        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            button_color = (200, 200, 200)
            border_color = (255, 255, 255)
            if click[0] == 1:
                if action is not None:
                    action()
                elif text == "Auto Run":
                    auto_run_to_goal()
        pygame.draw.rect(screen, button_color, (x, y, width, height))
        pygame.draw.rect(screen, border_color, (x, y, width, height), 2)
        screen.blit(text_surface, text_rect)

    def exit_game():
        pygame.quit()
        sys.exit()

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  # Convert milliseconds to seconds

        # Check if the time limit (e.g., 300 seconds) has been reached
        if elapsed_time >= 300:
            draw_message("Time's up! Restarting...")
            auto_mode = False  # Turn off auto mode
            maze = create_maze()
            player_pos = [0, 0]
            start_time = pygame.time.get_ticks()  # Reset the starting time
            
            bg_sound_path = os.path.join(os.path.dirname(__file__), "sound", "BGSound.wav")
            pygame.mixer.music.load(bg_sound_path)
            pygame.mixer.music.play(-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not auto_mode and player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_DOWN and not auto_mode and player_pos[0] < rows - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0:
                    player_pos[0] += 1
                elif event.key == pygame.K_LEFT and not auto_mode and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and not auto_mode and player_pos[1] < cols - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0:
                    player_pos[1] += 1
                elif event.key == pygame.K_SPACE:
                    auto_mode = not auto_mode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 150 < event.pos[0] < 250 and 10 < event.pos[1] < 40:
                        # Level the maze and reset the timer
                        level_up()
                        start_time = pygame.time.get_ticks()
        # Clear the screen
        screen.fill((128, 128, 128))
        screen.blit(image, (window_width - 150, 50))
        # Reduce the font size for the timer text
        timer_font = pygame.font.SysFont('comicsansms', 16)

        # Display the remaining time on the right side of the screen
        timer_text = timer_font.render(f"Time: {300 - elapsed_time} seconds", True, (255, 255, 255))

        # Create a rect object for the timer text
        text_rect = timer_text.get_rect()

        # Align the right side of the text with the right side of the window
        text_rect.right = window_width - 10

        # Lower the vertical position to avoid covering the button
        text_rect.top = window_height - 30

        # Draw the timer text on the screen using the rect object
        screen.blit(timer_text, text_rect)
        # Adjust movement speed when arrow keys are held down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not auto_mode and player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0:
            player_pos[0] -= 1
        elif keys[pygame.K_DOWN] and not auto_mode and player_pos[0] < rows - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0:
            player_pos[0] += 1
        elif keys[pygame.K_LEFT] and not auto_mode and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0:
            player_pos[1] -= 1
        elif keys[pygame.K_RIGHT] and not auto_mode and player_pos[1] < cols - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0:
            player_pos[1] += 1

        #create_button(window_width - 160, 10, 100, 30, (200, 200, 200), "Change Maze", action=change_maze)
        create_button(window_width - 160, 200, 100, 30, (255, 255, 255), "Level Up", action=level_up)
        create_button(window_width - 160, 250, 100, 30, (255, 255, 255), "Exit", action=exit_game)
        create_button(window_width - 160, 300, 100, 30, (255, 255, 255), "Auto Run", action=auto_run_to_goal)
        if auto_mode and player_pos != goal_pos:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(directions)
            auto_run_to_goal()
            for dx, dy in directions:
                nx, ny = player_pos[0] + dx, player_pos[1] + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx]:
                    if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                        player_pos[0], player_pos[1] = nx, ny
                    break

        if auto_mode and player_pos != goal_pos:
            auto_move_to_goal()
                
        if player_pos == goal_pos:
                pygame.mixer.music.stop()  # Dừng nhạc nền hiện tại
                w_sound_path = os.path.join(os.path.dirname(__file__), "sound", "WSound.wav")
                pygame.mixer.music.load(w_sound_path)  # Tải nhạc kết thúc
                pygame.mixer.music.play(0)  # Chơi nhạc kết thúc
                message = "You are win !!!Loading........."
                draw_message(message)
                pygame.display.flip()
                pygame.time.delay(5000)
                auto_mode = False  # Turn off auto mode
                
                bg_sound_path = os.path.join(os.path.dirname(__file__), "sound", "BGSound.wav")
                pygame.mixer.music.load(bg_sound_path)
                pygame.mixer.music.play(-1)
                
                maze = create_maze()
                player_pos = [0, 0]
                start_time = pygame.time.get_ticks()  # Reset lại thời gian
        player_image_path = os.path.join(os.path.dirname(__file__), "img", "c.png")
        #tải hình ảnh ng chơi lên
        player_image = pygame.image.load(player_image_path)
        player_image = pygame.transform.scale(player_image, (cell_size, cell_size))  # Điều chỉnh kích thước hình ảnh để phù hợp với ô vuông
        for row in range(rows):
            for col in range(cols):
                if maze[row][col] == 0:
                    pygame.draw.circle(screen, blue, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), cell_size // 2)
                else:
                    pygame.draw.circle(screen, yellow, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), cell_size // 2)

        # Vẽ hình ảnh người chơi
        screen.blit(player_image, (player_pos[1] * cell_size, player_pos[0] * cell_size))
        pygame.draw.circle(screen, green, (goal_pos[1] * cell_size + cell_size // 2, goal_pos[0] * cell_size + cell_size // 2), cell_size // 2)
        pygame.display.flip()
        clock.tick(15)
