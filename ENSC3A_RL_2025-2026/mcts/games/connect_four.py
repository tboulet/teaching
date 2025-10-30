"""
Connect Four game implementation.
"""
import numpy as np
from typing import List, Tuple, Optional
from mcts.games.base_game import GameState, Player


class ConnectFour(GameState):
    """
    Connect Four game on a 6x7 grid.

    Actions are column numbers 0-6. Pieces drop to the lowest empty row.
    First to connect 4 pieces horizontally, vertically, or diagonally wins.
    """

    def __init__(self, visual: bool = False):
        """
        Initialize Connect Four game.

        Args:
            visual: If True, display the board after each move.
        """
        self.rows = 6
        self.cols = 7
        self.board = None
        self.current_player = None
        super().__init__(visual)

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board = np.zeros((self.rows, self.cols), dtype=int)  # 0 = empty, 1 = Player1, 2 = Player2
        self.current_player = Player.PLAYER1

    def get_legal_actions(self) -> List[int]:
        """Return list of columns that are not full."""
        return [col for col in range(self.cols) if self.board[0, col] == 0]

    def step(self, action: int) -> Tuple[Optional[float], bool]:
        """
        Drop a piece in the given column.

        Args:
            action: Column to drop piece (0-6).

        Returns:
            reward: +1 if current player wins, -1 if loses, 0 if draw, None if ongoing
            done: True if game is terminal
        """
        if action not in self.get_legal_actions():
            raise ValueError(f"Invalid action {action}. Legal actions: {self.get_legal_actions()}")

        # Find the lowest empty row in the column
        row = self._get_lowest_empty_row(action)
        self.board[row, action] = self.current_player.value

        # Check for win
        if self._check_winner(row, action):
            return 1.0, True

        # Check for draw
        if len(self.get_legal_actions()) == 0:
            return 0.0, True

        # Switch player
        self.current_player = Player.PLAYER2 if self.current_player == Player.PLAYER1 else Player.PLAYER1

        return None, False

    def get_current_player(self) -> Player:
        """Return the current player."""
        return self.current_player

    def clone(self) -> 'ConnectFour':
        """Return a deep copy of the game state."""
        new_game = ConnectFour(visual=False)  # Don't carry over visual mode to clones
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        return new_game

    def render(self) -> str:
        """Return string representation of the board."""
        symbols = {0: '.', 1: 'X', 2: 'O'}

        lines = []
        lines.append("  " + " ".join(str(i) for i in range(self.cols)))
        lines.append("  " + "-" * (self.cols * 2 - 1))

        for row in self.board:
            row_str = "  " + " ".join(symbols[cell] for cell in row)
            lines.append(row_str)

        return "\n".join(lines)

    def _get_lowest_empty_row(self, col: int) -> int:
        """
        Find the lowest empty row in a column.

        Args:
            col: The column to check.

        Returns:
            The row index of the lowest empty cell.
        """
        for row in range(self.rows - 1, -1, -1):
            if self.board[row, col] == 0:
                return row
        raise ValueError(f"Column {col} is full!")

    def _check_winner(self, row: int, col: int) -> bool:
        """
        Check if the last move at (row, col) resulted in a win.

        Args:
            row: Row of the last move.
            col: Column of the last move.

        Returns:
            True if the current player won.
        """
        player = self.current_player.value

        # Check horizontal
        count = 1
        # Check left
        for c in range(col - 1, -1, -1):
            if self.board[row, c] == player:
                count += 1
            else:
                break
        # Check right
        for c in range(col + 1, self.cols):
            if self.board[row, c] == player:
                count += 1
            else:
                break
        if count >= 4:
            return True

        # Check vertical
        count = 1
        # Check down
        for r in range(row + 1, self.rows):
            if self.board[r, col] == player:
                count += 1
            else:
                break
        if count >= 4:
            return True

        # Check diagonal (/)
        count = 1
        # Check down-left
        r, c = row + 1, col - 1
        while r < self.rows and c >= 0:
            if self.board[r, c] == player:
                count += 1
                r += 1
                c -= 1
            else:
                break
        # Check up-right
        r, c = row - 1, col + 1
        while r >= 0 and c < self.cols:
            if self.board[r, c] == player:
                count += 1
                r -= 1
                c += 1
            else:
                break
        if count >= 4:
            return True

        # Check diagonal (\)
        count = 1
        # Check down-right
        r, c = row + 1, col + 1
        while r < self.rows and c < self.cols:
            if self.board[r, c] == player:
                count += 1
                r += 1
                c += 1
            else:
                break
        # Check up-left
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if self.board[r, c] == player:
                count += 1
                r -= 1
                c -= 1
            else:
                break
        if count >= 4:
            return True

        return False
