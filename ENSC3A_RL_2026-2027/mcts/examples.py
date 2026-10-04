"""
Exemples d'utilisation du framework MCTS.

Ce fichier contient différents exemples pour comprendre
comment utiliser le framework : on choisit d'abord les adversaires, puis le jeu.
"""

from mcts.games import TicTacToe, ConnectFour
from mcts.games.base_game import GameState
from mcts.agents import Agent, RandomAgent, MinimaxAgent, HumanAgent, MCTSAgent
from mcts.run_match import run_match

MCTS_SIMULATIONS = 1000
NUM_EPISODES = 10  # parties par match entre agents (une seule partie contre un humain)


def choose_game() -> type:
    """Demande le jeu à utiliser et renvoie sa classe."""
    choice = input("Jeu ? 1. TicTacToe  2. ConnectFour : ").strip()
    return ConnectFour if choice == '2' else TicTacToe


def minimax_depth(game: GameState) -> int:
    """Profondeur de recherche de Minimax selon le jeu."""
    # Sans heuristique, Minimax évalue à 0 toute position non terminale à la profondeur max :
    # jeu parfait au TicTacToe (profondeur 9 = toute la partie), mais au ConnectFour
    # il ne voit que les victoires à moins de max_depth coups.
    return 9 if isinstance(game, TicTacToe) else 4


def make_agent(kind: str, game: GameState) -> Agent:
    """Crée un agent ("Human", "Random", "Minimax" ou "MCTS") réglé pour le jeu."""
    if kind == "Human":
        return HumanAgent(name="You")
    if kind == "Random":
        return RandomAgent(name="Random")
    if kind == "Minimax":
        depth = minimax_depth(game)
        return MinimaxAgent(name=f"Minimax-D{depth}", max_depth=depth)
    return MCTSAgent(name=f"MCTS-{MCTS_SIMULATIONS}", num_simulations=MCTS_SIMULATIONS)


def results_line(agent1: Agent, agent2: Agent, results: dict) -> str:
    """Résumé d'un match sur une ligne."""
    return (f"{agent1.name}: {results['agent1_wins']}W | Draws: {results['draws']} | "
            f"{agent2.name}: {results['agent2_wins']}W")


def play(kind1: str, kind2: str, game: GameState) -> None:
    """Match entre deux types d'agents : une partie contre un humain, sinon NUM_EPISODES parties."""
    print("\n" + "="*60)
    print(f"{kind1} vs {kind2} ({type(game).__name__})")
    print("="*60)

    human = "Human" in (kind1, kind2)
    game.visual = human  # contre un humain, le plateau est aussi affiché dans le terminal
    agent1 = make_agent(kind1, game)
    agent2 = make_agent(kind2, game)

    results = run_match(
        game=game,
        agent1=agent1,
        agent2=agent2,
        num_episodes=1 if human else NUM_EPISODES,
        verbose=True,
        render_last_game=not human  # visualiser la dernière partie
    )

    print(f"\nRésultats finaux: {results_line(agent1, agent2, results)}")


def minimax_vs_minimax(game: GameState) -> None:
    """Minimax de différentes profondeurs s'affrontent."""
    depth = minimax_depth(game)
    print("\n" + "="*60)
    print(f"Minimax-D{depth} vs Minimax-D2 ({type(game).__name__})")
    print("="*60)

    agent1 = MinimaxAgent(name=f"Minimax-D{depth}", max_depth=depth)
    agent2 = MinimaxAgent(name="Minimax-D2", max_depth=2)
    results = run_match(
        game=game,
        agent1=agent1,
        agent2=agent2,
        num_episodes=NUM_EPISODES,
        verbose=True,
        render_last_game=True
    )

    print(f"\nRésultats finaux: {results_line(agent1, agent2, results)}")


def tournament(game: GameState) -> None:
    """Chaque paire d'agents parmi Random, Minimax et MCTS s'affronte."""
    print("\n" + "="*60)
    print(f"Tournoi : Random, Minimax et MCTS ({type(game).__name__})")
    print("="*60)

    agents = [make_agent(kind, game) for kind in ("Random", "Minimax", "MCTS")]

    # Faire jouer chaque paire d'agents
    for i, agent1 in enumerate(agents):
        for agent2 in agents[i + 1:]:
            results = run_match(
                game=game,
                agent1=agent1,
                agent2=agent2,
                num_episodes=NUM_EPISODES,
                verbose=False,
                render_last_game=False
            )

            print(f"{agent1.name} vs {agent2.name}: {results_line(agent1, agent2, results)}")


if __name__ == "__main__":
    """Menu principal : choisir les adversaires, puis le jeu."""

    matches = [
        ("Human", "Random"),
        ("Human", "Minimax"),
        ("Human", "MCTS"),
        ("Random", "Minimax"),
        ("Random", "MCTS"),
        ("Minimax", "MCTS"),
    ]
    examples = {
        str(i): (f"{kind1} vs {kind2}", lambda game, k1=kind1, k2=kind2: play(k1, k2, game))
        for i, (kind1, kind2) in enumerate(matches, start=1)
    }
    examples['7'] = ('Minimax vs Minimax (profondeurs différentes)', minimax_vs_minimax)
    examples['8'] = ('Tournoi : Random, Minimax et MCTS', tournament)
    human_examples = {'1', '2', '3'}

    print("\n" + "="*60)
    print("Framework MCTS - Exemples")
    print("="*60)
    print("\nChoisissez un exemple:")
    for key, (description, _) in examples.items():
        print(f"  {key}. {description}")
    print("  0. Tous les exemples (sauf Human)")

    choice = input("\nVotre choix: ").strip()

    if choice == '0':
        game_class = choose_game()
        for key, (description, func) in examples.items():
            if key not in human_examples:
                func(game_class(visual=False))
    elif choice in examples:
        _, func = examples[choice]
        func(choose_game()(visual=False))
    else:
        print("Choix invalide!")
