import sys
from snake_game import play_game

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ai":
        play_game(human_play=False)
    else:
        play_game(human_play=True)
