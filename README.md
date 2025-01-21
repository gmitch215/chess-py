# chess-py

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

A python program to play chess against an AI in the terminal.

This is a fork of [marcusbuffett/command-line-chess](https://github.com/marcusbuffett/command-line-chess) with significant improvements, serving as my Q3 Capstone project for AP Computer Science Principles.

## Features

- Play chess against an AI in the terminal
- Two player mode (run `chess --two` to enter)
- possible commands:
    * `a3`, `Nc3`, `Qxa`, etc: make a move
    * `l`: prints every legal move
    * `r`: make a random move
    * `u`: undo your last move
    * `quit`: resign the current game
    * `gm`: prints moves of current game in PGN format
    * `?`: help, prints all available commands

## Screenshots

Initial State:

![Initial](https://i.imgur.com/PSS7csc.png)

First move:

![First move](https://i.imgur.com/AsXhhvC.png)

## Installation

- First clone the repository:

```
git clone https://github.com/gmitch215/chess-py
```

- navigate into the newly created `chess-py` directory and run:

```
pip install .
```

## Usage

```sh
chess -h        # to see all possible options
```
```
usage: chess [-h] [-t] [-w W] [-b B] [-c]

A python program to play chess against an AI in the terminal.

optional arguments:
  -h, --help       show this help message and exit
  -t, --two        to play a 2-player game (default: False)
  -w W, --white W  color for white player (default: white)
  -b B, --black B  color for black player (default: black)
  -c, --checkered  use checkered theme for the chess board (default: False)

Enjoy the game!

```

## LICENSE
Take a look at the [LICENSE](https://github.com/gmitch215/chess-py/LICENSE) file

## Authors

- [@gmitch215](https://github.com/gmitch215)
- [@marcusbuffett](https://www.github.com/marcusbuffett)
- [@ClasherKasten](https://www.github.com/ClasherKasten)

## AI

The AI is a simple brute-force AI with min-max pruning. It evaluates a given position by counting the value of the pieces for each side (pawn -> 1, knight/bishop -> 3, rook -> 5, queen -> 9). It will evaluate the tree of moves, and take the path that results in the greatest gain.
