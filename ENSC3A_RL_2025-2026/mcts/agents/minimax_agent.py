"""
Minimax agent with alpha-beta pruning and depth limit.
"""
from mcts.agents.base_agent import Agent
from mcts.games.base_game import GameState


class MinimaxAgent(Agent):
    """
    Agent using Minimax algorithm with alpha-beta pruning.

    The agent searches the game tree to a specified depth and selects
    the action that maximizes its minimum guaranteed reward.
    """

    def __init__(self, name: str = "Minimax", max_depth: int = 5):
        """
        Initialize Minimax agent.

        Args:
            name: Name of the agent.
            max_depth: Maximum depth to search in the game tree.
        """
        super().__init__(name)
        self.max_depth = max_depth

    def select_action(self, game_state: GameState) -> int:
        """
        Select the best action using Minimax with alpha-beta pruning.

        Args:
            game_state: The current game state.

        Returns:
            The best action according to Minimax.
        """
        legal_actions = game_state.get_legal_actions()

        # Store the player we're maximizing for
        self.maximizing_player = game_state.get_current_player()

        best_action = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Try each legal action
        for action in legal_actions:
            # Simulate the action
            cloned_state = game_state.clone()
            reward, done = cloned_state.step(action)

            # Evaluate this action
            if done:
                # Terminal state reached
                value = reward
            else:
                # Continue searching
                value = self._minimax(cloned_state, depth=1, alpha=alpha, beta=beta, maximizing=False)

            # Update best action
            if value > best_value:
                best_value = value
                best_action = action

            # Update alpha
            alpha = max(alpha, best_value)

        return best_action

    def _minimax(self, game_state: GameState, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            game_state: Current game state.
            depth: Current depth in the search tree.
            alpha: Alpha value for pruning.
            beta: Beta value for pruning.
            maximizing: True if maximizing player's turn, False if minimizing.

        Returns:
            The value of the current state.
        """
        # Check terminal conditions
        legal_actions = game_state.get_legal_actions()

        if len(legal_actions) == 0 or depth >= self.max_depth:
            # Terminal state or depth limit reached
            # Return heuristic evaluation
            return self._evaluate_state(game_state)

        if maximizing:
            # Maximizing player (us)
            max_value = float('-inf')

            for action in legal_actions:
                cloned_state = game_state.clone()
                reward, done = cloned_state.step(action)

                if done:
                    # Terminal state
                    value = reward
                else:
                    value = self._minimax(cloned_state, depth + 1, alpha, beta, False)

                max_value = max(max_value, value)
                alpha = max(alpha, max_value)

                # Alpha-beta pruning
                if beta <= alpha:
                    break

            return max_value

        else:
            # Minimizing player (opponent)
            min_value = float('inf')

            for action in legal_actions:
                cloned_state = game_state.clone()
                reward, done = cloned_state.step(action)

                if done:
                    # Terminal state - reward is from opponent's perspective
                    # Since this is good for opponent, it's bad for us (negate it)
                    # And we're minimizing from our perspective, so we want low values
                    value = -reward
                else:
                    value = self._minimax(cloned_state, depth + 1, alpha, beta, True)

                min_value = min(min_value, value)
                beta = min(beta, min_value)

                # Alpha-beta pruning
                if beta <= alpha:
                    break

            return min_value

    def _evaluate_state(self, game_state: GameState) -> float:
        """
        Heuristic evaluation of a non-terminal state.

        Args:
            game_state: The game state to evaluate.

        Returns:
            Estimated value of the state (between -1 and 1).
        """
        # Simple heuristic: assume draw if depth limit reached
        # More sophisticated heuristics could be implemented per game
        return 0.0
