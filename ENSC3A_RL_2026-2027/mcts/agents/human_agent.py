"""
Human agent that gets input from the command line.
"""
from mcts.agents.base_agent import Agent
from mcts.games.base_game import GameState


class HumanAgent(Agent):
    """Agent controlled by human input via CLI."""

    def __init__(self, name: str = "Human"):
        """
        Initialize human agent.

        Args:
            name: Name of the agent.
        """
        super().__init__(name)

    def select_action(self, game_state: GameState) -> int:
        """
        Get action from human input.

        Args:
            game_state: The current game state.

        Returns:
            The action chosen by the human.
        """
        legal_actions = game_state.get_legal_actions()

        while True:
            try:
                action_str = input(f"{self.name}, enter your action {legal_actions}: ")
                action = int(action_str)

                if action in legal_actions:
                    return action
                else:
                    print(f"Invalid action! Must be one of {legal_actions}")

            except ValueError:
                print("Invalid input! Please enter a number.")
            except (KeyboardInterrupt, EOFError):
                print("\nGame interrupted by user.")
                raise
