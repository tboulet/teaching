"""
Monte Carlo Tree Search (MCTS) agent implementation.

This agent uses the MCTS algorithm with four main phases:
1. Selection: Traverse tree using UCB1
2. Expansion: Add a new child node
3. Simulation: Random rollout to terminal state
4. Backpropagation: Update statistics along the path
"""
import math
import random
from typing import Optional, List
from mcts.agents.base_agent import Agent
from mcts.games.base_game import GameState


class MCTSNode:
    """
    Node in the MCTS search tree.

    Each node represents a game state and stores statistics about
    the outcomes of simulations that pass through this node.
    """

    def __init__(self, state: GameState, parent: Optional['MCTSNode'] = None, action: Optional[int] = None):
        """
        Initialize an MCTS node.

        Args:
            state: The game state at this node.
            parent: The parent node (None for root).
            action: The action that led from parent to this node.
        """
        self.state = state  # Game state at this node
        self.parent = parent  # Parent node
        self.action = action  # Action that led to this node from parent

        self.children: List[MCTSNode] = []  # Child nodes
        self.untried_actions: List[int] = state.get_legal_actions()  # Actions not yet tried

        # Statistics
        self.visits = 0  # Number of times this node was visited
        self.value = 0.0  # Total value accumulated (sum of rewards)

    def is_fully_expanded(self) -> bool:
        """
        Check if all legal actions have been tried.

        Returns:
            True if no untried actions remain.
        """
        return len(self.untried_actions) == 0

    def is_terminal(self) -> bool:
        """
        Check if this node represents a terminal game state.

        Returns:
            True if the game is over at this node.
        """
        return len(self.state.get_legal_actions()) == 0

    def best_child(self, exploration_constant: float) -> 'MCTSNode':
        """
        Select the best child using the UCB1 formula.

        UCB1 balances exploitation (high value) and exploration (few visits):
        UCB1(child) = -(child.value / child.visits) + C * sqrt(ln(parent.visits) / child.visits)

        Note: We negate child.value because the child's value is from the opponent's
        perspective (it's the opponent's turn at the child node). We want to select
        children that are bad for the opponent (good for us).

        Args:
            exploration_constant: The exploration parameter C in UCB1.

        Returns:
            The child node with the highest UCB1 value.
        """
        best_score = float('-inf')
        best_child = None

        for child in self.children:
            # Exploitation term: negative average value (opponent's perspective)
            exploitation = -child.value / child.visits

            # Exploration term: UCB bonus
            exploration = exploration_constant * math.sqrt(math.log(self.visits) / child.visits)

            # UCB1 score
            ucb1_score = exploitation + exploration

            if ucb1_score > best_score:
                best_score = ucb1_score
                best_child = child

        return best_child

    def expand(self) -> 'MCTSNode':
        """
        Expand the tree by creating a new child node for an untried action.

        This corresponds to the EXPANSION phase of MCTS.

        Returns:
            The newly created child node.
        """
        # Select a random untried action
        action = random.choice(self.untried_actions)
        self.untried_actions.remove(action)

        # Clone the state and apply the action
        next_state = self.state.clone()
        next_state.step(action)

        # Create a new child node
        child_node = MCTSNode(state=next_state, parent=self, action=action)
        self.children.append(child_node)

        return child_node

    def simulate(self) -> float:
        """
        Simulate a random playout from this node to a terminal state.

        This corresponds to the SIMULATION (Rollout) phase of MCTS.

        The simulation uses a random policy: at each step, a random legal
        action is selected until the game ends.

        Returns:
            The reward from the perspective of the player who just moved
            to reach this node (i.e., the PREVIOUS player).
        """
        # Clone the state to avoid modifying the node's state
        simulation_state = self.state.clone()

        # Remember whose turn it was when we entered this node
        # The reward will be from the perspective of the player who JUST played
        # to reach this node (the parent's player)
        initial_player = simulation_state.get_current_player()

        # Perform random rollout until terminal state
        while not simulation_state.is_terminal():
            legal_actions = simulation_state.get_legal_actions()
            action = random.choice(legal_actions)
            reward, done = simulation_state.step(action)

            if done:
                # Game ended during rollout
                # reward is from perspective of the player who just moved
                # We need to return it from the perspective of initial_player

                # If the current player (who just moved) is the initial player,
                # return reward as-is
                # Otherwise, negate it (zero-sum game)
                current_player = simulation_state.get_current_player()

                # Note: After a terminal move, current_player has NOT changed yet
                # So we need to check the player who made the terminal move
                # In our implementation, step() switches player BEFORE returning
                # So if done=True, the current_player is the NEXT player (who didn't move)

                # The initial_player is the player whose turn it is at THIS node
                # So if current_player != initial_player, we need to negate
                if current_player != initial_player:
                    return -reward
                else:
                    return reward

        # If we somehow reach here (shouldn't happen), return 0
        return 0.0

    def backpropagate(self, reward: float) -> None:
        """
        Backpropagate the simulation result up the tree.

        This corresponds to the BACKPROPAGATION phase of MCTS.

        The reward is propagated up the tree, updating visit counts and values.
        Since this is a zero-sum game, the reward is negated at each level
        (what's good for one player is bad for the opponent).

        Args:
            reward: The reward from the simulation, from the perspective of
                   the player who played to reach this node.
        """
        node = self
        current_reward = reward

        while node is not None:
            # Update visit count
            node.visits += 1

            # Update value (from the perspective of the player who moved to reach this node)
            node.value += current_reward

            # Move to parent and negate reward (zero-sum game)
            node = node.parent
            current_reward = -current_reward

    def best_action(self) -> int:
        """
        Select the best action based on visit counts.

        After running many MCTS iterations, the action with the most visits
        is typically the most promising (more robust than highest value).

        Returns:
            The action corresponding to the most visited child.
        """
        best_child = max(self.children, key=lambda child: child.visits)
        return best_child.action


class MCTSAgent(Agent):
    """
    Monte Carlo Tree Search agent.

    This agent uses MCTS to select actions by building and searching
    a game tree through iterative simulation.
    """

    def __init__(
        self,
        name: str = "MCTS",
        num_simulations: int = 1000,
        exploration_constant: float = 1.41
    ):
        """
        Initialize MCTS agent.

        Args:
            name: Name of the agent.
            num_simulations: Number of MCTS iterations to run per action.
            exploration_constant: Exploration parameter C for UCB1 (sqrt(2) ≈ 1.41 is common).
        """
        super().__init__(name)
        self.num_simulations = num_simulations
        self.exploration_constant = exploration_constant

    def select_action(self, game_state: GameState) -> int:
        """
        Select an action using MCTS.

        The algorithm runs num_simulations iterations of:
        1. Selection: Traverse tree using UCB1
        2. Expansion: Add a new child node
        3. Simulation: Random rollout
        4. Backpropagation: Update statistics

        After all iterations, select the action with the most visits.

        Args:
            game_state: The current game state.

        Returns:
            The best action according to MCTS.
        """
        # Create root node
        root = MCTSNode(state=game_state)

        # Run MCTS iterations
        for _ in range(self.num_simulations):
            # PHASE 1: SELECTION
            # Start at root and select nodes until we find one that can be expanded
            node = root

            # Traverse the tree using UCB1 until we find a non-fully-expanded node
            while node.is_fully_expanded() and not node.is_terminal():
                node = node.best_child(self.exploration_constant)

            # PHASE 2: EXPANSION
            # If the node is not terminal and has untried actions, expand it
            if not node.is_terminal():
                node = node.expand()

            # PHASE 3: SIMULATION (Rollout)
            # Perform a random simulation from this node
            reward = node.simulate()

            # PHASE 4: BACKPROPAGATION
            # Propagate the result back up the tree
            node.backpropagate(reward)

        # DECISION: Select the action with the most visits
        return root.best_action()
