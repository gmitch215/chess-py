# no-list

As apart of the project rubric, I have to mention a list and talk about what happens when it isn't there.

https://github.com/gmitch215/chess-py/blob/bfe81844f443744e28965facb9600b0ac1658bba/src/Board.py#L23-L32

The `Board` class keeps track of the history of pieces and the amount of pieces on the board. Without them, I would need to make a variable for each piece that currently exists,
and I wouldn't be able to know when pieces would be taken because the history would be lost.
