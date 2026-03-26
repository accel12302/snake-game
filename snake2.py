import tkinter as tk
import random

# Window setup
root = tk.Tk()
root.title("Snake Game")
root.geometry("700x760+50+50")
root.configure(bg="#3b4a2f")  # dark green/brown outer border color
root.resizable(False, False)


# Constants
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 760
BORDER_SIZE = 15
UI_HEIGHT = 60
GAME_SPEED = 150
SNAKE_SIZE = 20

CANVAS_SIZE = WINDOW_WIDTH - (BORDER_SIZE * 2)

# Make canvas fit the snake grid exactly
CANVAS_SIZE = (CANVAS_SIZE // SNAKE_SIZE) * SNAKE_SIZE


# Game state
snake_body = [[60, 60]]
direction = "RIGHT"
grow_pending = False
game_over = False
game_job = None

food_x = 0
food_y = 0


# Layout
game_frame = tk.Frame(root, bg="#3b4a2f", padx=BORDER_SIZE, pady=BORDER_SIZE)
game_frame.pack(pady=(10, 0))

canvas = tk.Canvas(
    game_frame,
    width=CANVAS_SIZE,
    height=CANVAS_SIZE,
    bg="#ccffcc",
    highlightthickness=0
)
canvas.pack()

ui_frame = tk.Frame(root, bg="#3b4a2f", height=UI_HEIGHT)
ui_frame.pack(fill="x", pady=(8, 10))


# Helper functions
def score():
    return len(snake_body) - 1


def spawn_food():
    global food_x, food_y

    while True:
        new_x = random.randint(0, (CANVAS_SIZE // SNAKE_SIZE) - 1) * SNAKE_SIZE
        new_y = random.randint(0, (CANVAS_SIZE // SNAKE_SIZE) - 1) * SNAKE_SIZE
        if [new_x, new_y] not in snake_body:
            food_x = new_x
            food_y = new_y
            break



# Drawing
def draw_grid():
    for x in range(0, CANVAS_SIZE, SNAKE_SIZE):
        for y in range(0, CANVAS_SIZE, SNAKE_SIZE):
            color = "#c8f7c5" if (x // SNAKE_SIZE + y // SNAKE_SIZE) % 2 == 0 else "#b7eb8f"
            canvas.create_rectangle(
                x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
                fill=color, outline=""
            )


def draw_snake():
    for i, segment in enumerate(snake_body):
        x, y = segment
        color = "#1b5e20" if i == 0 else "#2e7d32"

        canvas.create_rectangle(
            x, y,
            x + SNAKE_SIZE, y + SNAKE_SIZE,
            fill=color, outline=""
        )


def draw_food():
    canvas.create_rectangle(
        food_x, food_y,
        food_x + SNAKE_SIZE, food_y + SNAKE_SIZE,
        fill="#e53935", outline=""
    )


def draw_game_over():
    draw_grid()
    canvas.create_rectangle(
        0, 0, CANVAS_SIZE, CANVAS_SIZE,
        fill="#3b4a2f", stipple="gray25", outline=""
    )
    canvas.create_text(
        CANVAS_SIZE // 2,
        CANVAS_SIZE // 2 - 20,
        text="GAME OVER",
        font=("Arial", 28, "bold"),
        fill="white"
    )
    canvas.create_text(
        CANVAS_SIZE // 2,
        CANVAS_SIZE // 2 + 20,
        text=f"Final Score: {score()}",
        font=("Arial", 16, "bold"),
        fill="white"
    )



# Game stuff
def change_direction(new_direction):
    global direction

    if new_direction == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    elif new_direction == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"
    elif new_direction == "UP" and direction != "DOWN":
        direction = "UP"
    elif new_direction == "DOWN" and direction != "UP":
        direction = "DOWN"


def move_snake():
    global grow_pending

    head_x, head_y = snake_body[0]

    if direction == "RIGHT":
        new_head = [head_x + SNAKE_SIZE, head_y]
    elif direction == "LEFT":
        new_head = [head_x - SNAKE_SIZE, head_y]
    elif direction == "UP":
        new_head = [head_x, head_y - SNAKE_SIZE]
    else:
        new_head = [head_x, head_y + SNAKE_SIZE]

    snake_body.insert(0, new_head)

    if grow_pending:
        grow_pending = False
    else:
        snake_body.pop()


def check_food_collision():
    global grow_pending

    if snake_body[0][0] == food_x and snake_body[0][1] == food_y:
        grow_pending = True
        spawn_food()


def check_wall_collision():
    head_x, head_y = snake_body[0]
    return (
        head_x < 0 or
        head_x >= CANVAS_SIZE or
        head_y < 0 or
        head_y >= CANVAS_SIZE
    )


def check_self_collision():
    return snake_body[0] in snake_body[1:]


def end_game():
    global game_over, game_job
    game_over = True
    game_job = None
    canvas.delete("all")
    draw_game_over()
    score_label.config(text=f"Score: {score()}")
    reset_button.pack(side="right", padx=20)


def reset_game():
    global snake_body, direction, grow_pending, game_over, game_job

    if game_job is not None:
        root.after_cancel(game_job)

    snake_body = [[60, 60]]
    direction = "RIGHT"
    grow_pending = False
    game_over = False
    game_job = None

    spawn_food()
    reset_button.pack_forget()
    score_label.config(text=f"Score: {score()}")

    canvas.delete("all")
    draw_grid()
    draw_snake()
    draw_food()

    game_loop()


def game_loop():
    global game_job

    if game_over:
        return

    move_snake()

    if check_wall_collision() or check_self_collision():
        end_game()
        return

    check_food_collision()

    canvas.delete("all")
    draw_grid()
    draw_snake()
    draw_food()
    score_label.config(text=f"Score: {score()}")

    game_job = root.after(GAME_SPEED, game_loop)



# Controls
root.bind("<Left>", lambda event: change_direction("LEFT"))
root.bind("<Right>", lambda event: change_direction("RIGHT"))
root.bind("<Up>", lambda event: change_direction("UP"))
root.bind("<Down>", lambda event: change_direction("DOWN"))

# Optional WASD
root.bind("a", lambda event: change_direction("LEFT"))
root.bind("d", lambda event: change_direction("RIGHT"))
root.bind("w", lambda event: change_direction("UP"))
root.bind("s", lambda event: change_direction("DOWN"))


# UI
score_label = tk.Label(
    ui_frame,
    text=f"Score: {score()}",
    font=("Arial", 16, "bold"),
    bg="#3b4a2f",
    fg="white"
)
score_label.pack(side="left", padx=20)

reset_button = tk.Button(
    ui_frame,
    text="Reset Game",
    font=("Arial", 12, "bold"),
    bg="#6b4f2a",
    fg="white",
    activebackground="#5a4223",
    activeforeground="white",
    relief="flat",
    command=reset_game
)


# Start game
spawn_food()
draw_grid()
draw_snake()
draw_food()
game_loop()

root.mainloop()