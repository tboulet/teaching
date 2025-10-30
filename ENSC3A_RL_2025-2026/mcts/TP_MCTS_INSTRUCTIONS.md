# TP MCTS - Instructions pour les Enseignants

## Vue d'Ensemble

Le framework MCTS est maintenant complet avec :
- ✅ Implémentation complète et testée de MCTS
- ✅ Version étudiante avec TODOs à compléter
- ✅ Suite de tests progressifs pour validation
- ✅ Documentation et exemples

## Structure des Fichiers

```
mcts/
├── games/                          # Jeux (complets, fournis)
│   ├── tictactoe.py
│   └── connect_four.py
├── agents/
│   ├── mcts_agent.py              # VERSION ACTUELLE (complète par défaut)
│   ├── mcts_agent_student.py      # Version à donner aux étudiants
│   ├── mcts_agent_correction.py   # Correction de référence
│   └── README_MCTS.md             # Documentation des versions
├── test_mcts_student.py           # Suite de tests progressifs
├── run_match.py                   # Fonction pour lancer des matchs
├── examples.py                    # Exemples d'utilisation
└── TP_MCTS_INSTRUCTIONS.md        # Ce fichier
```

## Préparation du TP

### Étape 1 : Préparer la version étudiante

```bash
cd mcts/agents/
cp mcts_agent_student.py mcts_agent.py
```

Cette commande remplace l'implémentation complète par la version avec TODOs.

### Étape 2 : Distribuer aux étudiants

Donnez aux étudiants :
- Le dossier `mcts/` complet
- Le fichier `test_mcts_student.py`
- (Optionnel) Le fichier `private/report.txt` avec le contenu des slides

Les étudiants n'ont PAS besoin de :
- `mcts_agent_correction.py` (gardez-le pour vous)
- `README_MCTS.md` (mais peut être utile)

## Ce que les Étudiants Doivent Implémenter

### Dans la classe `MCTSNode` :

1. **`is_fully_expanded()`** - Facile
   - Vérifier si `untried_actions` est vide

2. **`expand()`** - Moyen
   - Choisir une action non essayée
   - Cloner l'état et appliquer l'action
   - Créer un nouveau nœud enfant

3. **`simulate()`** - Moyen/Difficile
   - Jouer aléatoirement jusqu'à la fin
   - Gérer correctement la perspective des récompenses

4. **`backpropagate()`** - Moyen
   - Remonter l'arbre en mettant à jour visites et valeur
   - Inverser la récompense à chaque niveau (jeu à somme nulle)

5. **`best_child()`** - Difficile
   - Implémenter la formule UCB1
   - **Point clé**: Signe négatif pour la perspective adversaire

6. **`best_action()`** - Facile
   - Retourner l'action de l'enfant le plus visité

### Dans la classe `MCTSAgent` :

7. **`select_action()`** - Moyen
   - Boucle principale des 4 phases MCTS
   - Intégrer Selection, Expansion, Simulation, Backpropagation

## Utilisation de la Suite de Tests

Les étudiants peuvent tester leur implémentation progressivement :

```bash
python -m mcts.test_mcts_student
```

Les tests sont conçus pour être exécutés dans l'ordre :
1. ✅ Test 1 : Création de nœuds
2. ✅ Test 2 : Expansion
3. ✅ Test 3 : Simulation
4. ✅ Test 4 : Backpropagation
5. ✅ Test 5 : UCB1
6. ✅ Test 6 : Sélection d'action
7. ✅ Test 7 : Agent MCTS complet
8. ✅ Test 8 : Performance vs Random

## Résultats Attendus

Avec une implémentation correcte :

| Scénario | Résultat attendu |
|----------|------------------|
| TicTacToe - MCTS(1000) vs Random | ~80% de victoires |
| TicTacToe - MCTS(1000) vs Minimax-D9 | Majorité de matchs nuls |
| ConnectFour - MCTS(500) vs Random | ~90% de victoires |
| ConnectFour - MCTS(500) vs Minimax-D3 | ~65% de victoires |

## Points Pédagogiques Clés

### 1. Formule UCB1 avec Adversaire
```python
UCB1 = -(child.value / child.visits) + C * sqrt(ln(parent.visits) / child.visits)
```
Le signe négatif est **crucial** : les enfants représentent le tour de l'adversaire.

### 2. Backpropagation en Jeu à Somme Nulle
```python
while node is not None:
    node.visits += 1
    node.value += current_reward
    node = node.parent
    current_reward = -current_reward  # Inverser!
```

### 3. Sélection Finale
Choisir l'action avec le **plus de visites**, pas la plus haute valeur (plus robuste).

## Erreurs Communes des Étudiants

### ❌ Erreur 1 : Oublier le signe négatif dans UCB1
```python
# FAUX
exploitation = child.value / child.visits

# CORRECT
exploitation = -child.value / child.visits
```

### ❌ Erreur 2 : Ne pas inverser la récompense dans backpropagation
```python
# FAUX
while node:
    node.value += reward  # Toujours la même récompense
    node = node.parent

# CORRECT
current_reward = reward
while node:
    node.value += current_reward
    current_reward = -current_reward  # Inverser à chaque niveau
    node = node.parent
```

### ❌ Erreur 3 : Mauvaise gestion des perspectives dans simulate()
Les étudiants oublient souvent de vérifier quel joueur a gagné par rapport au joueur initial.

## Évaluation

### Critères de Notation Suggérés

- **Code fonctionne** (40%) : Passe tous les tests
- **Qualité du code** (20%) : Lisibilité, commentaires
- **Compréhension** (20%) : Questions orales sur UCB1, backpropagation
- **Performance** (20%) : Résultats contre Random et Minimax

### Questions Orales Suggérées

1. Pourquoi utilise-t-on le signe négatif dans UCB1 ?
2. Que représente le terme d'exploration dans UCB1 ?
3. Pourquoi inverse-t-on la récompense dans backpropagation ?
4. Pourquoi choisir l'action la plus visitée plutôt que la plus haute valeur ?
5. Quelle est la différence entre MCTS et Minimax ?

## Après le TP : Restaurer la Version Complète

```bash
cd mcts/agents/
cp mcts_agent_correction.py mcts_agent.py
```

## Extensions Possibles (Bonus)

Pour les étudiants avancés :

1. **Heuristique de simulation** : Remplacer la politique aléatoire
2. **Réutilisation de l'arbre** : Garder le sous-arbre entre les coups
3. **Parallelisation** : Exécuter plusieurs simulations en parallèle
4. **RAVE** : Rapid Action Value Estimation
5. **Neural MCTS** : Utiliser un réseau de neurones pour l'évaluation

## Exemples de Code pour les Étudiants

### Tester leur implémentation :
```python
from mcts.games import TicTacToe
from mcts.agents import MCTSAgent, RandomAgent
from mcts.run_match import run_match

game = TicTacToe(visual=False)
mcts = MCTSAgent(name="MCTS", num_simulations=500)
random = RandomAgent(name="Random")

results = run_match(game, mcts, random, num_episodes=10, verbose=True)
print(f"Win rate: {results['agent1_win_rate']:.0%}")
```

### Visualiser une partie :
```python
game = TicTacToe(visual=True)
results = run_match(game, mcts, random, num_episodes=1)
```

## Support

Pour toute question sur le framework :
- Consultez `mcts/README.md`
- Regardez `mcts/examples.py` pour des exemples
- Testez avec `python -m mcts.test_mcts_student`

Bon TP ! 🎯
