"""
Base class for all game-playing agents.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcts.games.base_game import GameState


class Agent(ABC):
    """Base class for all agents (algorithms)."""

    def __init__(self, name: str):
        """
        Initialize the agent.

        Args:
            name: Name of the agent for display purposes.
        """
        self.name = name

    @abstractmethod
    def select_action(self, game_state: 'GameState') -> int:
        """
        Given a game state, return the chosen action.

        This is called during the game to get the agent's move.

        Args:
            game_state: The current game state.

        Returns:
            The chosen action (must be in game_state.get_legal_actions()).
        """
        pass

    def reset(self) -> None:
        """
        Optional: Reset agent's internal state between games.

        Useful for agents that maintain statistics or tree structures.
        """
        pass
