"""
Pygame window used by HumanAgent to play TicTacToe and ConnectFour with the mouse.
"""
import os
from typing import Optional

import numpy as np

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

from mcts.games.base_game import GameState, Player
from mcts.games.tictactoe import TicTacToe

TICTACTOE_CELL_SIZE = 150
CONNECT_FOUR_CELL_SIZE = 90
STATUS_HEIGHT = 60

BACKGROUND_COLOR = (245, 245, 245)
TEXT_COLOR = (40, 40, 40)
HOVER_COLOR = (220, 220, 220)
LAST_MOVE_COLOR = (255, 240, 170)
LAST_MOVE_RING_COLOR = (255, 255, 255)
BOARD_COLOR = (30, 80, 180)
BOARD_HOVER_COLOR = (60, 110, 210)
TICTACTOE_COLORS = {Player.PLAYER1.value: (210, 50, 50), Player.PLAYER2.value: (40, 90, 200)}  # X red, O blue
CONNECT_FOUR_COLORS = {Player.PLAYER1.value: (220, 50, 50), Player.PLAYER2.value: (240, 200, 30)}  # red, yellow


class BoardWindow:
    """Window showing the board, where a human picks an action by clicking."""

    def __init__(self, title: str):
        """
        Open the pygame display (raises pygame.error if no display is available).

        Args:
            title: Window title.
        """
        pygame.display.init()
        pygame.font.init()
        self.title = title
        self.screen = None
        self.font = pygame.font.Font(None, 36)
        self.last_board = None  # board right after our last move, to highlight the opponent's reply

    def ask_action(self, game: GameState, player: Player) -> int:
        """
        Show the board and wait for a click on a legal action.

        Args:
            game: The current game state.
            player: The player controlled by the human.

        Returns:
            The clicked action.
        """
        self._open(game)
        legal_actions = game.get_legal_actions()
        status = f"À vous de jouer ({self._player_label(game, player)})"
        hovered = None
        self.draw(game, status, hovered)

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.close()
                raise KeyboardInterrupt("Window closed by the user")
            if event.type == pygame.MOUSEMOTION:
                action = self._action_at(game, event.pos)
                action = action if action in legal_actions else None
                if action != hovered:
                    hovered = action
                    self.draw(game, status, hovered)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = self._action_at(game, event.pos)
                if action in legal_actions:
                    # Show our move right away, the opponent may take a moment to answer
                    preview = game.clone()
                    preview.step(action)
                    self.last_board = self._board_2d(preview).copy()
                    self.draw(preview, "L'adversaire réfléchit...")
                    return action

    def show_result(self, game: GameState, status: str) -> None:
        """
        Show the final board and wait for a click (or key press) before continuing.

        Args:
            game: The final game state.
            status: Message to display, e.g. the result of the game.
        """
        self._open(game)
        self.draw(game, f"{status} (cliquez pour continuer)")
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.close()
                return
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return

    def close(self) -> None:
        """Close the window."""
        pygame.display.quit()
        self.screen = None

    def draw(self, game: GameState, status: str, hovered: Optional[int] = None) -> None:
        """
        Draw the board, the opponent's last move and a status line.

        Args:
            game: The game state to draw.
            status: Text displayed under the board.
            hovered: Action under the mouse, highlighted if not None.
        """
        board = self._board_2d(game)
        rows, cols = board.shape
        cell = self._cell_size(game)
        if self.last_board is not None and self.last_board.shape == board.shape:
            changed = board != self.last_board
        else:
            changed = np.zeros(board.shape, dtype=bool)

        self.screen.fill(BACKGROUND_COLOR)
        if isinstance(game, TicTacToe):
            self._draw_tictactoe(board, changed, hovered, cell)
        else:
            self._draw_connect_four(board, changed, hovered, cell)

        text = self.font.render(status, True, TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(cols * cell // 2, rows * cell + STATUS_HEIGHT // 2)))
        pygame.display.flip()

    def _draw_tictactoe(self, board: np.ndarray, changed: np.ndarray, hovered: Optional[int], cell: int) -> None:
        colors = TICTACTOE_COLORS
        margin = cell // 5
        for row in range(3):
            for col in range(3):
                rect = pygame.Rect(col * cell, row * cell, cell, cell)
                if changed[row, col]:
                    pygame.draw.rect(self.screen, LAST_MOVE_COLOR, rect)
                elif hovered == row * 3 + col:
                    pygame.draw.rect(self.screen, HOVER_COLOR, rect)
                value = board[row, col]
                if value == Player.PLAYER1.value:
                    pygame.draw.line(self.screen, colors[value], rect.move(margin, margin).topleft,
                                     rect.move(-margin, -margin).bottomright, 10)
                    pygame.draw.line(self.screen, colors[value], (rect.left + margin, rect.bottom - margin),
                                     (rect.right - margin, rect.top + margin), 10)
                elif value == Player.PLAYER2.value:
                    pygame.draw.circle(self.screen, colors[value], rect.center, cell // 2 - margin, 10)
        for i in range(1, 3):
            pygame.draw.line(self.screen, TEXT_COLOR, (i * cell, 0), (i * cell, 3 * cell), 4)
            pygame.draw.line(self.screen, TEXT_COLOR, (0, i * cell), (3 * cell, i * cell), 4)

    def _draw_connect_four(self, board: np.ndarray, changed: np.ndarray, hovered: Optional[int], cell: int) -> None:
        colors = CONNECT_FOUR_COLORS
        rows, cols = board.shape
        pygame.draw.rect(self.screen, BOARD_COLOR, pygame.Rect(0, 0, cols * cell, rows * cell))
        if hovered is not None:
            pygame.draw.rect(self.screen, BOARD_HOVER_COLOR, pygame.Rect(hovered * cell, 0, cell, rows * cell))
        radius = cell // 2 - 8
        for row in range(rows):
            for col in range(cols):
                center = (col * cell + cell // 2, row * cell + cell // 2)
                pygame.draw.circle(self.screen, colors.get(board[row, col], BACKGROUND_COLOR), center, radius)
                if changed[row, col]:
                    pygame.draw.circle(self.screen, LAST_MOVE_RING_COLOR, center, radius, 6)

    def _open(self, game: GameState) -> None:
        """Create (or resize) the window for this game."""
        rows, cols = self._board_2d(game).shape
        cell = self._cell_size(game)
        size = (cols * cell, rows * cell + STATUS_HEIGHT)
        if self.screen is None or self.screen.get_size() != size:
            self.screen = pygame.display.set_mode(size)
            pygame.display.set_caption(f"{self.title} - {type(game).__name__}")

    def _action_at(self, game: GameState, pos) -> Optional[int]:
        """Return the action corresponding to a click position (None outside the board)."""
        rows, cols = self._board_2d(game).shape
        cell = self._cell_size(game)
        x, y = pos
        if not (0 <= x < cols * cell and 0 <= y < rows * cell):
            return None
        row, col = y // cell, x // cell
        return row * 3 + col if isinstance(game, TicTacToe) else col

    @staticmethod
    def _board_2d(game: GameState) -> np.ndarray:
        return game.board.reshape(3, 3) if isinstance(game, TicTacToe) else game.board

    @staticmethod
    def _cell_size(game: GameState) -> int:
        return TICTACTOE_CELL_SIZE if isinstance(game, TicTacToe) else CONNECT_FOUR_CELL_SIZE

    @staticmethod
    def _player_label(game: GameState, player: Player) -> str:
        if isinstance(game, TicTacToe):
            return "X" if player == Player.PLAYER1 else "O"
        return "rouge" if player == Player.PLAYER1 else "jaune"
