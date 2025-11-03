"""
Monte Carlo Tree Search (MCTS) agent implementation.

This agent uses the MCTS algorithm with four main phases:
1. Selection: Traverse tree using UCB1
2. Expansion: Add a new child node
3. Simulation: Random rollout to terminal state
4. Backpropagation: Update statistics along the path

À IMPLÉMENTER PAR LES ÉTUDIANTS
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
        # ---- <VOTRE CODE ICI> ----
        pass
        # --------------------------

    def is_terminal(self) -> bool:
        """
        Check if this node represents a terminal game state.

        Returns:
            True if the game is over at this node.
        """
        # ---- <VOTRE CODE ICI> ----
        # TODO: Vérifier s'il n'y a plus d'actions légales
        pass
        # --------------------------

    def best_child(self, exploration_constant: float) -> 'MCTSNode':
        """
        Select the best child using the UCB1 formula.

        UCB1 balances exploitation (high value) and exploration (few visits):

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
            # ---- <VOTRE CODE ICI> ----
            # TODO: Calculer le score UCB1 pour chaque enfant

            # 1. Terme d'exploitation:
            #    (négatif car la valeur est du point de vue de l'adversaire)
            exploitation = ...

            # 2. Terme d'exploration:
            exploration = ...

            # 3. Score UCB1 total
            ucb1_score = ...

            # 4. Mettre à jour le meilleur score et le meilleur enfant
            ...
            # --------------------------

        return best_child

    def expand(self) -> 'MCTSNode':
        """
        Expand the tree by creating a new child node for an untried action.

        This corresponds to the EXPANSION phase of MCTS.

        Returns:
            The newly created child node.
        """
        # ---- <VOTRE CODE ICI> ----
        # TODO: Implémenter l'expansion

        # 1. Choisir une action non essayée
        action = ...

        # 2. Retirer cette action de la liste des actions non essayées
        ...

        # 3. Cloner l'état du jeu et appliquer l'action
        next_state = ...
        ...

        # 4. Créer un nouveau nœud enfant
        child_node = ...

        # 5. Ajouter l'enfant à la liste des enfants
        ...

        # 6. Retourner le nœud enfant
        return child_node
        # --------------------------

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
        # ---- <VOTRE CODE ICI> ----
        # TODO: Implémenter la simulation (rollout aléatoire)

        # 1. Cloner l'état pour ne pas modifier le nœud
        simulation_state = ...

        # 2. Mémoriser le joueur initial (celui dont c'est le tour à ce nœud)
        initial_player = simulation_state.get_current_player()

        # 3. Jouer aléatoirement jusqu'à atteindre un état terminal
        while not simulation_state.is_terminal():
            legal_actions = ...
            action = ...
            reward, done = ...

            if done:
                # Le jeu est terminé
                # La récompense est du point de vue du joueur qui vient de jouer
                # Nous devons la retourner du point de vue du joueur initial
                # HINT: Utilisez simulation_state.get_current_player() et comparez avec initial_player
                
                ...
                
                return ...
            
        # Si on arrive ici (ne devrait pas arriver), retourner 0
        return 0.0
        # --------------------------

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
        # ---- <VOTRE CODE ICI> ----
        # TODO: Implémenter la backpropagation

        # HINT: Remonter l'arbre en suivant les parents
        # HINT: À chaque nœud, incrémenter visits et ajouter la récompense à value
        # HINT: Inverser la récompense à chaque niveau (jeu à somme nulle)

        node = self
        current_reward = reward

        while node is not None:
            # 1. Incrémenter le compteur de visites
            ...

            # 2. Ajouter la récompense à la valeur
            ...

            # 3. Passer au parent et inverser la récompense
            node = ...
            current_reward = ...
        # --------------------------

    def best_action(self) -> int:
        """
        Select the best action based on visit counts.

        After running many MCTS iterations, the action with the most visits
        is typically the most promising (more robust than highest value).

        Returns:
            The action corresponding to the most visited child.
        """
        # ---- <VOTRE CODE ICI> ----
        # TODO: Retourner l'action de l'enfant le plus visité
        best_child = ...
        return ...
        # --------------------------


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
        # ---- <VOTRE CODE ICI> ----
        # TODO: Implémenter la boucle principale de MCTS

        # 1. Créer le nœud racine
        root = ...

        # 2. Exécuter num_simulations itérations
        for _ in range(self.num_simulations):

            # PHASE 1: SELECTION
            # Descendre dans l'arbre en utilisant UCB1 jusqu'à trouver
            # un nœud non complètement développé ou terminal
            node = root

            # HINT: Tant que le nœud est complètement développé ET non terminal,
            #       sélectionner le meilleur enfant avec best_child()
            while ...:
                node = ...

            # PHASE 2: EXPANSION
            # Si le nœud n'est pas terminal, l'étendre
            if ...:
                node = ...

            # PHASE 3: SIMULATION (Rollout)
            # Effectuer une simulation aléatoire depuis ce nœud
            reward = ...

            # PHASE 4: BACKPROPAGATION
            # Propager le résultat vers le haut de l'arbre
            ...

        # DÉCISION: Sélectionner l'action avec le plus de visites
        return ...
        # --------------------------
