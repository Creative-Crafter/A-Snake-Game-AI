# 🐍 Snake AI Game

A modern and smart Snake game built with **Python** and **Pygame**.  
Featuring Q-Learning AI training, human control mode, local learning memory, and stylish visuals!

## 🚀 Features

- 🎮 Play manually or let the AI train itself
- 🧠 **Q-Learning**-based AI that gets smarter over time
- 💾 Saves AI progress (`q_table.pkl`) locally
- 🛡️ Snake avoids running into itself or walls
- 🟩 Smooth, rounded snake design with a stylish background
- ⚡ Increased speed during AI training for faster learning

## 🕹️ Controls (Human Mode)

| Key                  | Action          |
|----------------------|-----------------|
| `Arrow Up` / `W`      | Move up          |
| `Arrow Down` / `S`    | Move down        |
| `Arrow Left` / `A`    | Move left        |
| `Arrow Right` / `D`   | Move right       |

## 📸 Screenshots

*(Add your own screenshots here!)*

![demo.mp4](/videos/demo.mp4)

## 💡 How to Use

1. Clone or download the repository.
2. Install the required library:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Human Mode** (play yourself):
   ```bash
   python start_snake_game.py
   ```
4. **Start AI Mode** (train the AI):
   ```bash
   python start_snake_game.py ai
   ```
5. **Stop** with `Ctrl + C`. The AI's progress is saved automatically in `q_table.pkl`.

## 🛠️ Technologies Used

- Python 3
- Pygame
- Q-Learning (Reinforcement Learning)

---

Have fun training and beating the AI! 🎉
