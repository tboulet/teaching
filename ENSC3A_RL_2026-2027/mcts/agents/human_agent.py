"""
Human agent that plays by clicking in a window (GUI) or by typing actions in the terminal (CLI).
"""
from mcts.agents.base_agent import Agent
from mcts.games.base_game import GameState


class HumanAgent(Agent):
    """Agent controlled by a human, through a pygame window or the command line."""

    def __init__(self, name: str = "Human", gui: bool = True):
        """
        Initialize human agent.

        Args:
            name: Name of the agent.
            gui: If True, play by clicking in a window. Falls back to the
                 command line if no display is available.
        """
        super().__init__(name)
        self.gui = gui
        self.window = None
        self.player = None  # player controlled by the human in the current game

    def reset(self) -> None:
        """Forget the previous game's board (used to highlight the opponent's moves)."""
        if self.window is not None:
            self.window.last_board = None

    def select_action(self, game_state: GameState) -> int:
        """
        Get action from human input.

        Args:
            game_state: The current game state.

        Returns:
            The action chosen by the human.
        """
        self.player = game_state.get_current_player()
        if self.gui and self._open_window():
            try:
                return self.window.ask_action(game_state, self.player)
            except KeyboardInterrupt:
                print("\nGame interrupted by user.")
                exit(0)
        return self._select_action_cli(game_state)

    def game_over(self, game_state: GameState) -> None:
        """Show the final board and the result in the window (GUI mode)."""
        if self.window is None or self.window.screen is None:
            return
        winner = game_state.get_winner()
        if winner is None:
            status = "Match nul"
        elif winner == self.player:
            status = "Victoire !"
        else:
            status = "Défaite..."
        self.window.show_result(game_state, status)

    def _open_window(self) -> bool:
        """Create the window on first use. Returns False (and switches to CLI) if it cannot be opened."""
        if self.window is None:
            try:
                from mcts.gui import BoardWindow
                self.window = BoardWindow(self.name)
            except Exception as e:
                print(f"Impossible d'ouvrir une fenêtre ({e}), on joue dans le terminal.")
                self.gui = False
                return False
        return True

    def _select_action_cli(self, game_state: GameState) -> int:
        """Ask the action in the terminal until a legal one is entered."""
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
                exit(0)
