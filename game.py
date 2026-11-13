
import tkinter as tk
import random
from playsound import playsound
import threading

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

game_over = False

snake = [(5, 10)]
direction = "Right"

apple_x = 15
apple_y = 10

frame_rate = 100

root = tk.Tk()
root.geometry("600x600")
root.title("SARPA !!!")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black"
)
canvas.pack()


def draw_player():
    for position in snake:
        canvas.create_rectangle(
            position[0] * CELL_SIZE,
            position[1] * CELL_SIZE,
            (position[0] + 1) * CELL_SIZE,
            (position[1] + 1) * CELL_SIZE,
            fill="green",
            outline="green"
        )


def draw_apple():
    canvas.create_rectangle(
        apple_x * CELL_SIZE,
        apple_y * CELL_SIZE,
        (apple_x + 1) * CELL_SIZE,
        (apple_y + 1) * CELL_SIZE,
        fill="red",
        outline="red"
    )


def key_pressed(event):
    global direction

    if event.keysym == "Up" and direction != "Down":
        direction = "Up"

    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"

    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"

    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"


def player_movements(grow=False):
    head_x, head_y = snake[0]

    if direction == "Up":
        head_y -= 1
    elif direction == "Down":
        head_y += 1
    elif direction == "Left":
        head_x -= 1
    elif direction == "Right":
        head_x += 1

    # Add new head
    snake.insert(0, (head_x, head_y))

    # Remove tail only if the snake is not growing
    if not grow:
        snake.pop()


def check_collisions():
    global game_over

    head_x, head_y = snake[0]

    # Wall collision
    if (
        head_x < 0 or head_x >= COLS or
        head_y < 0 or head_y >= ROWS
    ):
        game_over = True
        return

    # Body collision
    for position in snake[1:]:
        body_x, body_y = position

        if head_x == body_x and head_y == body_y:
            game_over = True
            break


def check_apple_collision():
    global apple_x, apple_y

    head_x, head_y = snake[0]

    if head_x == apple_x and head_y == apple_y:
        play_eat_sound()
        # Find all empty cells
        empty_cells = []

        for x in range(COLS):
            for y in range(ROWS):

                if (x, y) not in snake:
                    empty_cells.append((x, y))

        # Choose a random empty cell
        if len(empty_cells) > 0:
            new_position = random.choice(empty_cells)

            apple_x = new_position[0]
            apple_y = new_position[1]
def play_eat_sound():
    threading.Thread(
        target=playsound,
        args=("sounds/food.mp3",),
        daemon=True
    ).start()


def play_game_over_sound():
    threading.Thread(
        target=playsound,
        args=("sounds/gameover.mp3",),
        daemon=True
    ).start()


    
#reset
def reset():
    global snake, direction, game_over
    global apple_x, apple_y

    snake = [(5, 10)]
    direction = "Right"
    game_over = False

    apple_x = 15
    apple_y = 10

    game_loop()


def game_loop():
    if game_over:
        canvas.delete("all")
        
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 30)
        )
        play_game_over_sound()
        root.after(2000, reset)
        return

    # Get current head position
    head_x, head_y = snake[0]

    # Calculate next position
    next_x = head_x
    next_y = head_y

    if direction == "Up":
        next_y -= 1
    elif direction == "Down":
        next_y += 1
    elif direction == "Left":
        next_x -= 1
    elif direction == "Right":
        next_x += 1

    # Check whether the snake will eat the apple
    grow = False

    if next_x == apple_x and next_y == apple_y:
        grow = True

    player_movements(grow)

    check_collisions()

    if game_over:
        game_loop()
        return

    if grow:
        check_apple_collision()

    canvas.delete("all")

    draw_player()
    draw_apple()

    root.after(frame_rate, game_loop)


root.bind("<KeyPress>", key_pressed)

game_loop()
root.mainloop()
