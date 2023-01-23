# skiwfish
My python chess implementation and engine

## Usage

W.I.P. but current usage is as follows:

After installing python 3.x, 

```
python3 skiwfish.py
```

This will bring up a board and list of [Standard Algebraic Notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)) legal moves.

```
  -----------------
8 | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 
7 | ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ 
6 | - - - - - - - - 
5 | - - - - - - - - 
4 | - - - - - - - - 
3 | - - - - - - - - 
2 | ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 
1 | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
  -----------------
    a b c d e f g h


Legal Moves For White: ['Nc3', 'Na3', 'Nh3', 'Nf3', 'a3', 'a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'e3', 'e4', 'f3', 'f4', 'g3', 'g4', 'h3', 'h4']

White move?

```

1. Typing one of the listed legal moves will execute it.
2. Typing `engine` will have the A.I. find a move for you.
3. Typing `random` will pick a move randomly from the list of legal moves.

## Bugs and stuff

Some notes about the current implementation:

1. The game will declare checkmate if no legal moves exist, even if it's actually a stalemate
2. Castling is really buggy right now; there's a lot of instances where castling will be in the list of legal moves but not actually be legal according to the rules.  Still working on it.
3. The list of legal moves doesn't adhere strictly to Standard Algebraic Notation.  One thing to look out for is moves that need to be disambiguated.  For example, consider this board state:

```  -----------------
8 | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 
7 | - ♙ ♙ - ♙ ♙ ♙ ♙ 
6 | - - - - - - - - 
5 | ♙ ♞ - ♙ - - - - 
4 | - - - - - - - - 
3 | - - - - - ♞ - - 
2 | ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 
1 | ♜ - ♝ ♛ ♚ ♝ - ♜ 
  -----------------
    a b c d e f g h


Legal Moves For White: ['Rb1', 'Rg1', 'a3', 'a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'e3', 'e4', 'g3', 'g4', 'h3', 'h4', 'Ng5', 'Ne5', 'Ng1', 'Nh4', 'Nd4', 'Nxc7', 'Na7', 'Nc3', 'Na3', 'Nd6', 'Nb5d4']
```

In this position, white's two knights can both move to `d4`.  The standard way to notate this is `Nbd4` for the knight on the b file and `Nfd4` for the knight on the f file.  The way it's notated (currently) in this implemenation though is `Nd4` for the knight on the f file and `Nb5d4` for the knight on the b file.  If there's ever any difficuly disambiguating moves, just take a look at the move list.  I'll work on this :P 

## Have Fun!