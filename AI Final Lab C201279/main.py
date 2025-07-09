import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Get screen size dynamically
info = pygame.display.Info()
SCREEN_WIDTH = min(info.current_w, info.current_h) - 100  # Leave some padding
SCREEN_HEIGHT = SCREEN_WIDTH
TILE_SIZE = SCREEN_WIDTH // 8
FONT = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_BLUE = (173, 216, 230)
WOOD_BROWN = (139, 69, 19)
NEON_PURPLE = (128, 0, 128)

# Load the queen image
queen_img = pygame.image.load('C:\Queen_img.png')
queen_img = pygame.transform.scale(queen_img, (TILE_SIZE - 10, TILE_SIZE - 10))

# Game state
levels = [
    {"size": 8, "moves": 20, "time_limit": 260, "obstacles": 0},  # Level 1: Easy, no obstacles
    {"size": 8, "moves": 18, "time_limit": 180, "obstacles": 2},  # Level 2: Add obstacles
    {"size": 8, "moves": 16, "time_limit": 80, "obstacles": 3},  # Level 3: More obstacles
    {"size": 8, "moves": 14, "time_limit": 45, "obstacles": 4},  # Level 4: Increased difficulty
    {"size": 8, "moves": 12, "time_limit": 40, "obstacles": 5},  # Level 5: Higher obstacles
    {"size": 8, "moves": 10, "time_limit": 35, "obstacles": 6}, # Level 6: Time pressure
    {"size": 8, "moves": 8, "time_limit": 30, "obstacles": 7},  # Level 7: Challenging
    {"size": 8, "moves": 6, "time_limit": 25, "obstacles": 8},  # Level 8: Extreme
]
current_level = 0
queens = []
moves = 0
score = 0
theme = WHITE  # Default theme color
extra_moves = 0
hints = 0
undo_moves = 0
obstacles = []

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("8-Queen Game")


def draw_board(board_size, theme=WHITE):
    """Draw the chessboard."""
    for row in range(board_size):
        for col in range(board_size):
            color = theme if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_queens():
    """Draw the queens on the board using images."""
    for queen in queens:
        x, y = queen
        screen.blit(queen_img, (x * TILE_SIZE + 5, y * TILE_SIZE + 5))


def draw_obstacles():
    """Draw obstacles on the board."""
    for obs in obstacles:
        x, y = obs
        pygame.draw.rect(screen, DARK_GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def is_valid_placement(x, y, board_size):
    """Check if the queen placement is valid."""
    for qx, qy in queens:
        if x == qx or y == qy or (x - y) == (qx - qy) or (x + y) == (qx + qy):
            return False
    if (x, y) in obstacles:
        return False
    return True


def draw_text(text, position, color=GOLD):
    """Draw text on the screen."""
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, position)


def fireworks():
    """Display fireworks effect."""
    for _ in range(50):
        x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(screen, random.choice([RED, GREEN, BLUE, GOLD]), (x, y), random.randint(5, 15))
        pygame.display.flip()
        time.sleep(0.05)


def queen_dance():
    """Show queens dancing on the board."""
    for _ in range(10):
        for queen in queens:
            x, y = queen
            color = random.choice([RED, GREEN, BLUE, GOLD])
            pygame.draw.circle(screen, color, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 20)
        pygame.display.flip()
        time.sleep(0.1)


def end_level(stars):
    """Display level completion screen."""
    screen.fill(BLACK)
    draw_text(f"Level Complete!", (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4))
    for i in range(stars):
        pygame.draw.polygon(
            screen,
            GOLD,
            [
                (150 + i * 100, 200), (170 + i * 100, 250),
                (220 + i * 100, 250), (180 + i * 100, 280),
                (200 + i * 100, 330), (150 + i * 100, 300),
                (100 + i * 100, 330), (120 + i * 100, 280),
                (80 + i * 100, 250), (130 + i * 100, 250),
            ],
        )
    pygame.display.flip()
    time.sleep(2)
    queen_dance()


def give_reward():
    """Give a random reward for completing a level."""
    global extra_moves, hints, undo_moves, theme
    reward = random.choice(["extra_moves", "hint", "undo_move", "new_theme"])
    if reward == "extra_moves":
        extra_moves += 5
        return "Reward: 5 Extra Moves!"
    elif reward == "hint":
        hints += 1
        return "Reward: 1 Hint!"
    elif reward == "undo_move":
        undo_moves += 3
        return "Reward: 3 Undo Moves!"
    elif reward == "new_theme":
        theme = random.choice([LIGHT_BLUE, WOOD_BROWN, NEON_PURPLE])
        return "Reward: New Theme Unlocked!"


def show_hint(board_size):
    """Highlight a valid position for 3 seconds."""
    for x in range(board_size):
        for y in range(board_size):
            if is_valid_placement(x, y, board_size):
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.display.flip()
                time.sleep(3)
                return


def generate_obstacles(board_size, count):
    """Generate obstacle positions randomly on the board."""
    obstacle_positions = []
    while len(obstacle_positions) < count:
        x, y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        if (x, y) not in queens and (x, y) not in obstacle_positions:
            obstacle_positions.append((x, y))
    return obstacle_positions


# Main game loop
running = True
start_time = time.time()
while running:
    screen.fill(BLACK)
    level = levels[current_level]
    board_size = level["size"]
    move_limit = level["moves"] + extra_moves
    time_limit = level["time_limit"]

    # Generate obstacles for the current level
    if not obstacles:
        obstacles = generate_obstacles(board_size, level["obstacles"])

    # Draw the board, obstacles, and pieces
    draw_board(board_size, theme)
    draw_obstacles()
    draw_queens()

    # Display current level, score, moves, and time
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(time_limit - elapsed_time))
    draw_text(f"Level: {current_level + 1}", (10, 10))
    draw_text(f"Score: {score}", (10, 50))
    draw_text(f"Moves: {moves}/{move_limit}", (10, 90))
    draw_text(f"Time: {remaining_time}s", (10, 130))
    draw_text(f"Hints: {hints}", (10, 170))
    draw_text(f"Undo: {undo_moves}", (10, 210))

    if remaining_time == 0:
        draw_text("Time's Up! Game Over!", (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), RED)
        pygame.display.flip()
        time.sleep(2)
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and moves < move_limit:
            x, y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
            if not is_valid_placement(x, y, board_size):
                pygame.draw.rect(screen, RED, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                draw_text("Invalid Move!", (10, SCREEN_HEIGHT - 50), RED)
                pygame.display.flip()
                time.sleep(1)
                moves += 1
            else:
                queens.append((x, y))
                moves += 1
                score += 10
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h and hints > 0:
                show_hint(board_size)
                hints -= 1
            elif event.key == pygame.K_u and undo_moves > 0 and queens:
                queens.pop()
                undo_moves -= 1
                moves -= 1

    if len(queens) == board_size:
        stars = 3 if moves <= move_limit * 0.5 else 2 if moves <= move_limit * 0.75 else 1
        end_level(stars)
        reward_message = give_reward()
        current_level += 1
        if current_level >= len(levels):
            fireworks()
            draw_text("Congratulations! You've completed all 8 levels!", (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2), GOLD)
            pygame.display.flip()
            time.sleep(5)
            running = False
        else:
            queens = []
            moves = 0
            obstacles = []
            start_time = time.time()
            draw_text(reward_message, (10, SCREEN_HEIGHT - 50), GREEN)
            pygame.display.flip()
            time.sleep(2)
    elif moves >= move_limit:
        draw_text("Game Over!", (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), RED)
        pygame.display.flip()
        time.sleep(2)
        running = False

    pygame.display.flip()

pygame.quit()