"""
Exemples d'utilisation du framework MCTS.

Ce fichier contient différents exemples pour comprendre
comment utiliser le framework.
"""

from mcts.games import TicTacToe, ConnectFour
from mcts.agents import RandomAgent, MinimaxAgent, HumanAgent, MCTSAgent
from mcts.run_match import run_match


def example_1_random_vs_random():
    """Exemple 1: Deux agents aléatoires s'affrontent au TicTacToe."""
    print("\n" + "="*60)
    print("Exemple 1: Random vs Random (TicTacToe)")
    print("="*60)

    game = TicTacToe(visual=False)
    agent1 = RandomAgent(name="Random-1")
    agent2 = RandomAgent(name="Random-2")

    results = run_match(
        game=game,
        agent1=agent1,
        agent2=agent2,
        num_episodes=10,
        verbose=True,
        render_last_game=True
    )

    print(f"\nRésultats finaux: {results}")


def example_2_minimax_vs_random_tictactoe():
    """Exemple 2: Minimax vs Random au TicTacToe."""
    print("\n" + "="*60)
    print("Exemple 2: Minimax vs Random (TicTacToe)")
    print("="*60)

    game = TicTacToe(visual=False)
    agent1 = MinimaxAgent(name="Minimax", max_depth=9)
    agent2 = RandomAgent(name="Random")

    results = run_match(
        game=game,
        agent1=agent1,
        agent2=agent2,
        num_episodes=10,
        verbose=True,
        render_last_game=True
    )

    print(f"\nRésultats finaux: {results}")


def example_3_minimax_vs_random_connect4():
    """Exemple 3: Minimax vs Random au Connect Four."""
    print("\n" + "="*60)
    print("Exemple 3: Minimax vs Random (ConnectFour)")
    print("="*60)

    game = ConnectFour(visual=False)
    # Note: depth=3 car ConnectFour est plus complexe que TicTacToe
    agent1 = MinimaxAgent(name="Minimax-D3", max_depth=3)
    agent2 = RandomAgent(name="Random")

    results = run_match(
        game=game,
        agent1=agent1,
        agent2=agent2,
        num_episodes=10,
        verbose=True,
        render_last_game=True
    )

    print(f"\nRésultats finaux: {results}")


def example_4_minimax_vs_minimax():
    """Exemple 4: Minimax de différentes profondeurs s'affrontent."""
    print("\n" + "="*60)
    print("Exemple 4: Minimax-D3 vs Minimax-D2 (ConnectFour)")
    print("="*60)

    game = ConnectFour(visual=False)
    agent1 = MinimaxAgent(name="Minimax-D3", max_depth=3)
    agent2 = MinimaxAgent(name="Minimax-D2", max_depth=2)

    results = run_match(
        game=game,
        agent1=agent1,
        agent2=agent2,
        num_episodes=10,
        verbose=True,
        render_last_game=True
    )

    print(f"\nRésultats finaux: {results}")


def example_5_human_vs_random():
    """Exemple 5: Joueur humain vs Random (TicTacToe)."""
    print("\n" + "="*60)
    print("Exemple 5: Human vs Random (TicTacToe)")
    print("="*60)
    print("Vous allez jouer contre un agent aléatoire.")
    print("Entrez le numéro de l'action quand c'est votre tour.\n")

    game = TicTacToe(visual=True)  # visual=True pour voir le plateau
    agent1 = HumanAgent(name="You")
    agent2 = RandomAgent(name="Random")

    results = run_match(
        game=game,
        agent1=agent1,
        agent2=agent2,
        num_episodes=1,  # Une seule partie
        verbose=True,
        render_last_game=False  # Déjà en visual=True
    )

    print(f"\nRésultats finaux: {results}")


def example_6_comparing_agents():
    """Exemple 6: Comparer plusieurs agents sur un même jeu."""
    print("\n" + "="*60)
    print("Exemple 6: Comparaison de plusieurs agents")
    print("="*60)

    game = TicTacToe(visual=False)
    agents = [
        RandomAgent(name="Random"),
        MinimaxAgent(name="Minimax-D7", max_depth=7),
        MinimaxAgent(name="Minimax-D9", max_depth=9),
    ]

    # Faire jouer chaque paire d'agents
    for i, agent1 in enumerate(agents):
        for j, agent2 in enumerate(agents):
            if i >= j:  # Éviter les doublons et les matchs contre soi-même
                continue

            print(f"\n{'-'*60}")
            print(f"{agent1.name} vs {agent2.name}")
            print(f"{'-'*60}")

            results = run_match(
                game=game,
                agent1=agent1,
                agent2=agent2,
                num_episodes=10,
                verbose=False,
                render_last_game=False
            )

            print(f"Résultats: {agent1.name}: {results['agent1_wins']}W | "
                  f"Draws: {results['draws']} | {agent2.name}: {results['agent2_wins']}W")


def example_7_mcts():
    """Exemple 7: Test de MCTS sur différents jeux."""
    print("\n" + "="*60)
    print("Exemple 7: Monte Carlo Tree Search (MCTS)")
    print("="*60)

    # Test sur TicTacToe
    print("\n[TicTacToe]")
    print("-"*60)
    game1 = TicTacToe(visual=False)

    print("MCTS(500 sims) vs Random:")
    mcts1 = MCTSAgent(name="MCTS-500", num_simulations=500)
    random1 = RandomAgent(name="Random")
    results1 = run_match(game1, mcts1, random1, 10, verbose=False, render_last_game=False)
    print(f"  {results1['agent1_wins']}W - {results1['draws']}D - {results1['agent2_wins']}L  "
          f"(win rate: {results1['agent1_win_rate']:.0%})")

    print("\nMCTS(500 sims) vs Minimax-D7:")
    mcts2 = MCTSAgent(name="MCTS-500", num_simulations=500)
    minimax1 = MinimaxAgent(name="Minimax-D7", max_depth=7)
    results2 = run_match(game1, mcts2, minimax1, 10, verbose=False, render_last_game=False)
    print(f"  {results2['agent1_wins']}W - {results2['draws']}D - {results2['agent2_wins']}L")

    # Test sur ConnectFour
    print("\n[ConnectFour]")
    print("-"*60)
    game2 = ConnectFour(visual=False)

    print("MCTS(300 sims) vs Random:")
    mcts3 = MCTSAgent(name="MCTS-300", num_simulations=300)
    random2 = RandomAgent(name="Random")
    results3 = run_match(game2, mcts3, random2, 10, verbose=False, render_last_game=True)
    print(f"  {results3['agent1_wins']}W - {results3['draws']}D - {results3['agent2_wins']}L  "
          f"(win rate: {results3['agent1_win_rate']:.0%})")

    print(f"\nRésultats finaux:")
    print(f"  TicTacToe: MCTS montre de bonnes performances")
    print(f"  ConnectFour: MCTS excelle avec {results3['agent1_win_rate']:.0%} de victoires!")


if __name__ == "__main__":
    """Menu principal pour choisir un exemple."""

    examples = {
        '1': ('Random vs Random (TicTacToe)', example_1_random_vs_random),
        '2': ('Minimax vs Random (TicTacToe)', example_2_minimax_vs_random_tictactoe),
        '3': ('Minimax vs Random (ConnectFour)', example_3_minimax_vs_random_connect4),
        '4': ('Minimax-D3 vs Minimax-D2 (ConnectFour)', example_4_minimax_vs_minimax),
        '5': ('Human vs Random (TicTacToe)', example_5_human_vs_random),
        '6': ('Comparaison de plusieurs agents', example_6_comparing_agents),
        '7': ('MCTS - Monte Carlo Tree Search', example_7_mcts),
    }

    print("\n" + "="*60)
    print("Framework MCTS - Exemples")
    print("="*60)
    print("\nChoisissez un exemple:")
    for key, (description, _) in examples.items():
        print(f"  {key}. {description}")
    print("  0. Tous les exemples (sauf Human)")

    choice = input("\nVotre choix: ").strip()

    if choice == '0':
        # Exécuter tous les exemples sauf le Human
        for key, (description, func) in examples.items():
            if key != '5':  # Skip Human example
                func()
    elif choice in examples:
        _, func = examples[choice]
        func()
    else:
        print("Choix invalide!")
