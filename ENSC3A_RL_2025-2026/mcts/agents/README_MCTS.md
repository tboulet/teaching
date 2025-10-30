# MCTS Agent - Versions pour les Étudiants et Correction

Ce répertoire contient trois versions de l'agent MCTS :

## Fichiers

### 1. `mcts_agent.py` (VERSION ACTUELLE)
- **Version actuelle utilisée par le framework**
- Par défaut : contient l'implémentation COMPLÈTE
- À remplacer par la version étudiant pour le TP

### 2. `mcts_agent_student.py` (VERSION ÉTUDIANTS)
- **Version incomplète à donner aux étudiants**
- Contient des TODO à compléter
- Structure complète avec hints et docstrings
- Les étudiants doivent implémenter :
  - `MCTSNode.is_fully_expanded()`
  - `MCTSNode.best_child()` (formule UCB1)
  - `MCTSNode.expand()`
  - `MCTSNode.simulate()` (rollout aléatoire)
  - `MCTSNode.backpropagate()`
  - `MCTSNode.best_action()`
  - `MCTSAgent.select_action()` (boucle MCTS principale)

### 3. `mcts_agent_correction.py` (CORRECTION)
- **Version complète pour la correction**
- Implémentation de référence
- Utiliser pour vérifier les implémentations des étudiants

## Utilisation pour le TP

### Avant le TP (préparation)

```bash
# Remplacer la version complète par la version étudiant
cd mcts/agents/
mv mcts_agent.py mcts_agent_complete_backup.py
cp mcts_agent_student.py mcts_agent.py
```

### Après le TP (correction)

```bash
# Pour tester avec la correction
cd mcts/agents/
cp mcts_agent_correction.py mcts_agent.py
```

## Test de la Version Étudiants

Pour vérifier que les étudiants ont correctement implémenté MCTS :

```python
from mcts.games import TicTacToe, ConnectFour
from mcts.agents import MCTSAgent, RandomAgent
from mcts.run_match import run_match

# Test basique
game = TicTacToe(visual=False)
mcts = MCTSAgent(name="MCTS", num_simulations=500)
random = RandomAgent(name="Random")

results = run_match(game, mcts, random, num_episodes=10, verbose=True)
print(f"Win rate: {results['agent1_win_rate']:.0%}")

# Attendu : > 70% de victoires contre Random
```

## Résultats Attendus

Avec une implémentation correcte, MCTS devrait obtenir :

**TicTacToe (1000 simulations) :**
- vs Random : ~80% de victoires
- vs Minimax-D9 : Majorité de matchs nuls

**ConnectFour (500 simulations) :**
- vs Random : ~90% de victoires
- vs Minimax-D3 : ~65% de victoires

## Points Clés à Enseigner

1. **UCB1 avec perspective adversaire** : `-child.value / child.visits + C * sqrt(ln(parent.visits) / child.visits)`
   - Le signe négatif est crucial (valeur depuis le point de vue de l'adversaire)

2. **Backpropagation avec jeu à somme nulle** : Inverser la récompense à chaque niveau

3. **Sélection finale** : Choisir l'action avec le plus de visites (pas la plus haute valeur)

4. **Rollout** : Politique aléatoire simple mais efficace

## Conseils pour les Étudiants

- Implémenter dans l'ordre : `expand()` → `simulate()` → `backpropagate()` → `best_child()` → `select_action()`
- Tester chaque méthode individuellement avant de passer à la suivante
- Commencer avec peu de simulations (10-50) pour debugger
- Utiliser `visual=True` pour voir le comportement
