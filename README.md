# 2048 Game in Python

This is a Python implementation of the classic **2048** game, built for the purpose of learning and practicing object-oriented programming and game development. The project is split across three files, each serving a unique purpose:

- `logic_2048.py`: Contains all core game logic using a matrix to represent the board.
- `game_2048.py`: Interfaces with logic_2048.py to simulate moves and display the resulting matrix.
- `drawing_2048.py`: A fully animated version of the game using Pygame, replicating the original 2048 experience.


## Features

- Full implementation of 2048 logic using simple matrix manipulation.
- Clear separation of logic and interface for learning clarity.
- Animated gameplay using Pygame.
- Local play via the terminal.


## Tech Stack and Technologies Used

- Python 3.x
- Pygame (for the animated version)
- VS Code or any Python-compatible code editor


## Try It Yourself

- Clone the repository.
- Make sure you have Python 3 installed.
- (For the animated version) Install Pygame:
  ```
  pip install pygame
  ```
- To run the logic-only version (text-based):
  ```
  python game_2048.py
  ```
- To run the animated version (with Pygame):
  ```
  python drawing_2048.py
  ```
