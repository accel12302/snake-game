import tkinter as tk
import random 

root = tk.Tk()

# Setting some window properties
root.title("Snake Game")
root.configure(background="gray")
root.minsize(200, 200)
root.maxsize(1000, 1000)
root.geometry("600x600+50+50")

# Canvas
canvas = tk.Canvas(root, width=550, height=550, bg="white")
canvas.pack(anchor=tk.CENTER, expand=True)

SNAKE_SIZE = 20  # Define snake block size

snake_body = [[60, 60]]
grow_pending = False
direction = "RIGHT"

food_x = random.randint(0, 27) * SNAKE_SIZE
food_y = random.randint(0, 27) * SNAKE_SIZE

def draw_food():
    canvas.create_rectangle(
        food_x, food_y,
        food_x + SNAKE_SIZE, food_y + SNAKE_SIZE,
        fill="red", outline=""
    )

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

def draw_snake():
    for segment in snake_body:
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + SNAKE_SIZE, segment[1] + SNAKE_SIZE,
            fill="green", outline=""
        )

def move_snake():
    global snake_body, grow_pending
    head_x, head_y = snake_body[0]
    if direction == "RIGHT":
        new_head = [head_x + SNAKE_SIZE, head_y]
    elif direction == "LEFT":
        new_head = [head_x - SNAKE_SIZE, head_y]
    elif direction == "UP":
        new_head = [head_x, head_y - SNAKE_SIZE]
    elif direction == "DOWN":
        new_head = [head_x, head_y + SNAKE_SIZE]
    snake_body.insert(0, new_head)
    if grow_pending:
        grow_pending = False
    else:
        snake_body.pop()

def check_food_collision():
    global food_x, food_y, grow_pending
    if snake_body[0][0] == food_x and snake_body[0][1] == food_y:
        food_x = random.randint(0, 27) * SNAKE_SIZE
        food_y = random.randint(0, 27) * SNAKE_SIZE
        grow_pending = True
        print("Food eaten!")
        print(f"Score: {score()}")

def check_wall_collision():
    head_x, head_y = snake_body[0]
    if head_x < 0 or head_x >= 550 or head_y < 0 or head_y >= 550:
        print("Game Over! You hit the wall.")
        root.destroy()

def check_self_collision():
    head = snake_body[0]
    if head in snake_body[1:]:
        print("Game Over! You hit yourself.")
        root.destroy()

def score():
    return len(snake_body) -1 
    
def game_loop():
    canvas.delete("all")
    move_snake()
    check_food_collision()
    check_wall_collision()
    check_self_collision()
    draw_snake()
    draw_food()
    score_label.config(text=f"Score: {score()}")
    root.after(150, game_loop)

root.bind("<Left>",  lambda event: change_direction("LEFT"))
root.bind("<Right>", lambda event: change_direction("RIGHT"))
root.bind("<Up>",    lambda event: change_direction("UP"))
root.bind("<Down>",  lambda event: change_direction("DOWN"))

score_label = tk.Label(root, text="Score:" + str(score()), font=("Arial", 14), bg="gray")
score_label.pack(side=tk.BOTTOM, pady=10)


game_loop()
root.mainloop()