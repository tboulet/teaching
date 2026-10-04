"""
Random agent that selects actions uniformly at random.
"""
import random
from mcts.agents.base_agent import Agent
from mcts.games.base_game import GameState


class RandomAgent(Agent):
    """Agent that plays randomly from legal actions."""

    def __init__(self, name: str = "Random"):
        """
        Initialize random agent.

        Args:
            name: Name of the agent.
        """
        super().__init__(name)

    def select_action(self, game_state: GameState) -> int:
        """
        Select a random legal action.

        Args:
            game_state: The current game state.

        Returns:
            A randomly selected legal action.
        """
        legal_actions = game_state.get_legal_actions()
        return random.choice(legal_actions)
