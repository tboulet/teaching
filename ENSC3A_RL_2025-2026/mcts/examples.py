"""
Exemples d'utilisation du framework MCTS.

Ce fichier contient différents exemples pour comprendre
comment utiliser le framework.
"""

from mcts.games import TicTacToe, ConnectFour
from mcts.agents import RandomAgent, MinimaxAgent, HumanAgent
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
        MinimaxAgent(name="Minimax-D3", max_depth=3),
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

            print(f"Résultats: {agent1.name} gagne {results['agent1_wins']}/10 "
                  f"({results['agent1_win_rate']:.1%})")


if __name__ == "__main__":
    """Menu principal pour choisir un exemple."""

    examples = {
        '1': ('Random vs Random (TicTacToe)', example_1_random_vs_random),
        '2': ('Minimax vs Random (TicTacToe)', example_2_minimax_vs_random_tictactoe),
        '3': ('Minimax vs Random (ConnectFour)', example_3_minimax_vs_random_connect4),
        '4': ('Minimax-D3 vs Minimax-D2 (ConnectFour)', example_4_minimax_vs_minimax),
        '5': ('Human vs Random (TicTacToe)', example_5_human_vs_random),
        '6': ('Comparaison de plusieurs agents', example_6_comparing_agents),
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
