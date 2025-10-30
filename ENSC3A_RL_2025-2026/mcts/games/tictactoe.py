"""
Tic-Tac-Toe game implementation.
"""
import numpy as np
import random
from typing import List, Tuple, Optional
from copy import deepcopy
from mcts.games.base_game import GameState, Player


class TicTacToe(GameState):
    """
    Tic-Tac-Toe game on a 3x3 grid.

    Actions are numbered 0-8, corresponding to positions:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """

    def __init__(self, visual: bool = False):
        """
        Initialize Tic-Tac-Toe game.

        Args:
            visual: If True, display the board after each move.
        """
        self.board = None
        self.current_player = None
        super().__init__(visual)

    def reset(self) -> None:
        """Reset the game to initial state with a randomly chosen starting player."""
        self.board = np.zeros(9, dtype=int)  # 0 = empty, 1 = Player1, 2 = Player2
        self.current_player = random.choice([Player.PLAYER1, Player.PLAYER2])

    def get_legal_actions(self) -> List[int]:
        """Return list of empty positions."""
        return [i for i in range(9) if self.board[i] == 0]

    def step(self, action: int) -> Tuple[Optional[float], bool]:
        """
        Place a mark at the given position.

        Args:
            action: Position to place mark (0-8).

        Returns:
            reward: +1 if current player wins, -1 if loses, 0 if draw, None if ongoing
            done: True if game is terminal
        """
        if action not in self.get_legal_actions():
            raise ValueError(f"Invalid action {action}. Legal actions: {self.get_legal_actions()}")

        # Place mark
        self.board[action] = self.current_player.value

        # Check for win
        winner = self._check_winner()
        if winner is not None:
            reward = 1.0 if winner == self.current_player else -1.0
            return reward, True

        # Check for draw
        if len(self.get_legal_actions()) == 0:
            return 0.0, True

        # Switch player
        self.current_player = Player.PLAYER2 if self.current_player == Player.PLAYER1 else Player.PLAYER1

        return None, False

    def get_current_player(self) -> Player:
        """Return the current player."""
        return self.current_player

    def clone(self) -> 'TicTacToe':
        """Return a deep copy of the game state."""
        new_game = TicTacToe(visual=False)  # Don't carry over visual mode to clones
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        return new_game

    def render(self) -> str:
        """Return string representation of the board."""
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        board_2d = self.board.reshape(3, 3)

        lines = []
        lines.append("  0   1   2")
        for row_idx, row in enumerate(board_2d):
            row_str = f"{row_idx * 3} " + " | ".join(symbols[cell] for cell in row)
            lines.append(row_str)
            if row_idx < 2:
                lines.append("  -----------")

        return "\n".join(lines)

    def _check_winner(self) -> Optional[Player]:
        """
        Check if there is a winner.

        Returns:
            The winning player, or None if no winner yet.
        """
        board_2d = self.board.reshape(3, 3)

        # Check rows
        for row in board_2d:
            if row[0] != 0 and row[0] == row[1] == row[2]:
                return Player(row[0])

        # Check columns
        for col in range(3):
            if board_2d[0, col] != 0 and board_2d[0, col] == board_2d[1, col] == board_2d[2, col]:
                return Player(board_2d[0, col])

        # Check diagonals
        if board_2d[0, 0] != 0 and board_2d[0, 0] == board_2d[1, 1] == board_2d[2, 2]:
            return Player(board_2d[0, 0])
        if board_2d[0, 2] != 0 and board_2d[0, 2] == board_2d[1, 1] == board_2d[2, 0]:
            return Player(board_2d[0, 2])

        return None
