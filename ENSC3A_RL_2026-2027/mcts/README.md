# MCTS Framework - TP Reinforcement Learning

Framework pour l'implémentation et la comparaison d'algorithmes de jeu, avec un focus sur Monte Carlo Tree Search (MCTS).

## Structure du Projet

```
mcts/
├── games/              # Implémentations des jeux
│   ├── base_game.py   # Classe abstraite GameState
│   ├── tictactoe.py   # Tic-Tac-Toe (3x3)
│   └── connect_four.py # Puissance 4 (6x7)
├── agents/            # Implémentations des algorithmes
│   ├── base_agent.py  # Classe abstraite Agent
│   ├── random_agent.py    # Agent aléatoire
│   ├── human_agent.py     # Joueur humain (CLI)
│   ├── minimax_agent.py   # Minimax avec alpha-beta
│   └── mcts_agent.py      # MCTS (À IMPLÉMENTER)
└── run_match.py       # Script principal pour lancer des matchs
```

## Utilisation

<!> Les commandes se run depuis `ENSC3A_RL_2026-2027`.

### Lancer un Match

```bash
# Lancer les exemples fournis
python -m mcts.run_match

# Tester votre implémentation de MCTS (tests progressifs)
python -m mcts.test_mcts_student
```

### Utilisation Programmatique

```python
from mcts.games import TicTacToe, ConnectFour
from mcts.agents import RandomAgent, MinimaxAgent
from mcts.run_match import run_match

# Créer le jeu (visual=False pour désactiver l'affichage)
game = TicTacToe(visual=False)

# Créer les agents
agent1 = MinimaxAgent(name="Minimax", max_depth=9)
agent2 = RandomAgent(name="Random")

# Lancer le match
results = run_match(
    game=game,
    agent1=agent1,
    agent2=agent2,
    num_episodes=20,
    verbose=True,           # Afficher les résultats de chaque partie
    render_last_game=True   # Visualiser la dernière partie
)

print(f"Résultats : {results}")
```

## Interface GameState

Chaque jeu doit implémenter :

- `reset()` : Réinitialiser le jeu
- `get_legal_actions()` : Retourner la liste des actions légales
- `step(action)` : Exécuter une action, passer au joueur suivant et retourner (reward, done)
- `get_current_player()` : Retourner le joueur dont c'est le tour
- `get_winner()` : Retourner le gagnant (None si partie en cours ou match nul)
- `is_terminal()` : Indiquer si la partie est terminée (fourni par la classe de base)
- `clone()` : Retourner une copie du jeu
- `render()` : Retourner une représentation textuelle
- `display()` : Afficher le jeu si visual=True

## Interface Agent

Chaque agent doit implémenter :

- `select_action(game_state)` : Choisir une action
- `reset()` : (Optionnel) Réinitialiser l'état interne

## Agents Disponibles

### RandomAgent
Choisit une action aléatoire parmi les actions légales.

```python
agent = RandomAgent(name="Random")
```

### HumanAgent
Demande au joueur humain de saisir une action via le terminal.

```python
agent = HumanAgent(name="Human")
```

### MinimaxAgent
Utilise l'algorithme Minimax avec élagage alpha-beta.

```python
agent = MinimaxAgent(name="Minimax", max_depth=5)
```

### MCTSAgent (À IMPLÉMENTER)

À vous de l'implémenter ! Lisez `mcts/agents/mcts_agent.py` et completez les classes MCTSNode et MCTSAgent.

## Tests

Pour tester le framework :

```python
# Test rapide
from mcts.games import TicTacToe
from mcts.agents import MinimaxAgent, RandomAgent
from mcts.run_match import run_match

game = TicTacToe(visual=False)
results = run_match(
    game=game,
    agent1=MinimaxAgent(name="Minimax", max_depth=9),
    agent2=RandomAgent(name="Random"),
    num_episodes=10,
    verbose=True
)
print(results)
# Attendu : Minimax devrait gagner ~95-100% des parties
```

## Résultats Attendus

- **Minimax vs Random** (TicTacToe) : ~100% de victoires pour Minimax
- **Minimax vs Random** (ConnectFour, depth=3) : ~90-95% de victoires pour Minimax
- **MCTS vs Random** : À tester après implémentation !
