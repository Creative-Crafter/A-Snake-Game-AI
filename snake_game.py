import pygame
import random
import pickle
import os
import sys

pygame.init()

# Fenstergröße und Grid
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20

# Farben
BG_COLOR = (44, 62, 80)
SNAKE_HEAD = (0, 255, 0)
SNAKE_BODY = (0, 100, 0)
FOOD_COLOR = (255, 99, 71)

# Spiel-Fenster
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI")

# Q-Learning-Parameter
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPSILON = 0.1
Q_FILE = "q_table.pkl"

# Aktionen: Oben, Unten, Links, Rechts
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Q-Tabelle laden
if os.path.exists(Q_FILE):
    with open(Q_FILE, "rb") as f:
        q_table = pickle.load(f)
    print("Q-Tabelle geladen.")
else:
    q_table = {}
    print("Neue Q-Tabelle erstellt.")

clock = pygame.time.Clock()

def draw(snake, food):
    win.fill(BG_COLOR)
    for i, segment in enumerate(snake):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(win, color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE), border_radius=4)
    pygame.draw.rect(win, FOOD_COLOR, (food[0], food[1], GRID_SIZE, GRID_SIZE), border_radius=4)
    pygame.display.update()

def get_state(snake, food, snake_dir):
    head = snake[0]

    food_up = food[1] < head[1]
    food_down = food[1] > head[1]
    food_left = food[0] < head[0]
    food_right = food[0] > head[0]

    danger_straight = will_collide(snake, head[0] + snake_dir[0] * GRID_SIZE, head[1] + snake_dir[1] * GRID_SIZE)
    danger_right = will_collide(snake, head[0] + snake_dir[1] * GRID_SIZE, head[1] - snake_dir[0] * GRID_SIZE)
    danger_left = will_collide(snake, head[0] - snake_dir[1] * GRID_SIZE, head[1] + snake_dir[0] * GRID_SIZE)

    moving_x = snake_dir[0]
    moving_y = snake_dir[1]

    return (moving_x, moving_y, food_up, food_down, food_left, food_right, danger_straight, danger_right, danger_left)

def will_collide(snake, x, y):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    if (x, y) in snake:
        return True
    return False

def choose_action(state, snake_dir):
    if state not in q_table:
        q_table[state] = [0] * 4

    possible_actions = list(range(4))

    # Verhindere Rückwärtsbewegung
    if snake_dir == (0, -1):
        if 1 in possible_actions:
            possible_actions.remove(1)
    elif snake_dir == (0, 1):
        if 0 in possible_actions:
            possible_actions.remove(0)
    elif snake_dir == (-1, 0):
        if 3 in possible_actions:
            possible_actions.remove(3)
    elif snake_dir == (1, 0):
        if 2 in possible_actions:
            possible_actions.remove(2)

    if random.random() < EPSILON:
        return random.choice(possible_actions)
    else:
        best_action = max(possible_actions, key=lambda a: q_table[state][a])
        return best_action

def move_snake(snake, action):
    dx, dy = ACTIONS[action]
    new_head = (snake[0][0] + dx * GRID_SIZE, snake[0][1] + dy * GRID_SIZE)
    snake.insert(0, new_head)
    return new_head

def place_food(snake):
    while True:
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        if (x, y) not in snake:
            return (x, y)

def run_game(human_play, episode):
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = random.choice(ACTIONS)
    food = place_food(snake)
    score = 0
    steps = 0
    max_steps = 500

    while True:
        pygame.event.pump()

        keys = pygame.key.get_pressed()
        if human_play:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if snake_dir != (0, 1):
                    snake_dir = (0, -1)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if snake_dir != (0, -1):
                    snake_dir = (0, 1)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if snake_dir != (1, 0):
                    snake_dir = (-1, 0)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if snake_dir != (-1, 0):
                    snake_dir = (1, 0)
        else:
            state = get_state(snake, food, snake_dir)
            action = choose_action(state, snake_dir)
            snake_dir = ACTIONS[action]

        new_head = move_snake(snake, ACTIONS.index(snake_dir) if human_play else action)
        steps += 1

        reward = -0.05
        done = False

        if will_collide(snake[1:], new_head[0], new_head[1]) or steps > max_steps:
            reward = -100
            done = True
        elif new_head == food:
            reward = 100
            score += 1
            food = place_food(snake)
        else:
            snake.pop()

        if not human_play:
            new_state = get_state(snake, food, snake_dir)
            if new_state not in q_table:
                q_table[new_state] = [0] * 4

            old_q = q_table[state][action]
            max_future_q = max(q_table[new_state])
            new_q = (1 - LEARNING_RATE) * old_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[state][action] = new_q

        draw(snake, food)
        clock.tick(15 if human_play else 15)

        if done:
            return score

def play_game(human_play=True):
    try:
        episode = 1
        while True:
            score = run_game(human_play, episode)
            if not human_play:
                print(f"Episode {episode}: Score = {score}")
                if episode % 50 == 0:
                    with open(Q_FILE, "wb") as f:
                        pickle.dump(q_table, f)
                    print("Q-Tabelle gespeichert.")
                episode += 1
            else:
                print(f"Score: {score}")
                episode = 1
    except KeyboardInterrupt:
        print("\nTraining abgebrochen mit STRG+C.")
        if not human_play:
            with open(Q_FILE, "wb") as f:
                pickle.dump(q_table, f)
            print("Q-Tabelle gespeichert und beendet.")
        pygame.quit()
        sys.exit()
