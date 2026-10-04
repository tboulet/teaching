"""
Base class for two-player zero-sum games.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from enum import Enum


class Player(Enum):
    """Enumeration for players."""
    PLAYER1 = 1
    PLAYER2 = 2


class GameState(ABC):
    """
    Abstract base class for two-player zero-sum games.

    This class defines the interface that all game implementations must follow.
    Students will use this interface but won't need to modify it.
    """

    def __init__(self, visual: bool = False):
        """
        Initialize the game state.

        Args:
            visual: If True, the game will display visual feedback during play.
        """
        self.visual = visual
        self.reset()

    @abstractmethod
    def reset(self) -> None:
        """Reset the game to initial state."""
        pass

    @abstractmethod
    def get_legal_actions(self) -> List[int]:
        """
        Return list of legal action indices.

        Returns:
            List of integers representing valid actions.
        """
        pass

    @abstractmethod
    def step(self, action: int) -> Tuple[Optional[float], bool]:
        """
        Execute action and switch to the next player.

        Args:
            action: The action to execute (must be in get_legal_actions()).

        Returns:
            reward: +1 if current player wins, -1 if loses, 0 if draw, None if ongoing
            done: True if game is terminal (win/loss/draw)
        """
        pass

    @abstractmethod
    def get_current_player(self) -> Player:
        """
        Return the player whose turn it is.

        Returns:
            The current player (Player.PLAYER1 or Player.PLAYER2).
        """
        pass

    @abstractmethod
    def clone(self) -> 'GameState':
        """
        Return a deep copy of the current state.

        Returns:
            A new GameState instance with the same state.
        """
        pass

    @abstractmethod
    def render(self) -> str:
        """
        Return string representation of the game state.

        Returns:
            String representation for display.
        """
        pass

    def is_terminal(self) -> bool:
        """
        Check if game is over.

        Returns:
            True if no legal actions remain.
        """
        return len(self.get_legal_actions()) == 0

    def display(self) -> None:
        """Print the game state if visual mode is enabled."""
        if self.visual:
            print(self.render())
            print()
