"""
Run matches between two agents.
"""
from typing import Dict
from mcts.agents.base_agent import Agent
from mcts.games.base_game import GameState, Player


def run_match(
    game: GameState,
    agent1: Agent,
    agent2: Agent,
    num_episodes: int = 10,
    verbose: bool = True,
    render_last_game: bool = True
) -> Dict:
    """
    Run multiple games between two agents.

    Args:
        game: Instance of the game to play (e.g., TicTacToe(visual=False)).
        agent1: First agent (plays as Player 1).
        agent2: Second agent (plays as Player 2).
        num_episodes: Number of games to play.
        verbose: If True, print progress after each game.
        render_last_game: If True, enable visualization for the last game.

    Returns:
        Dictionary with match statistics:
        {
            'agent1_wins': int,
            'agent2_wins': int,
            'draws': int,
            'agent1_win_rate': float
        }
    """
    results = {
        'agent1_wins': 0,
        'agent2_wins': 0,
        'draws': 0,
    }

    agents = {Player.PLAYER1: agent1, Player.PLAYER2: agent2}

    for episode in range(num_episodes):
        # Reset agents
        agent1.reset()
        agent2.reset()

        # Enable visualization for last game if requested
        if render_last_game and episode == num_episodes - 1:
            game.visual = True
            if verbose:
                print(f"\n{'=' * 50}")
                print(f"Game {episode + 1}/{num_episodes} (with visualization)")
                print(f"{'=' * 50}\n")

        # Reset game
        game.reset()
        game.display()

        # Play one game
        done = False
        move_count = 0

        while not done:
            current_player = game.get_current_player()
            current_agent = agents[current_player]

            # Display current player
            if game.visual:
                player_symbol = 'X' if current_player == Player.PLAYER1 else 'O'
                print(f"{current_agent.name} ({player_symbol}) is thinking...")

            # Get action from agent
            action = current_agent.select_action(game)

            # Execute action
            if game.visual:
                print(f"{current_agent.name} plays action: {action}\n")

            reward, done = game.step(action)
            game.display()
            move_count += 1

            # Check for game end
            if done:
                if reward == 1.0:
                    # Current player wins
                    winner = current_player
                    if winner == Player.PLAYER1:
                        results['agent1_wins'] += 1
                        winner_name = agent1.name
                    else:
                        results['agent2_wins'] += 1
                        winner_name = agent2.name

                    if verbose:
                        if game.visual:
                            print(f"{'=' * 50}")
                        print(f"Game {episode + 1}: {winner_name} wins in {move_count} moves!")
                        if game.visual:
                            print(f"{'=' * 50}\n")

                elif reward == 0.0:
                    # Draw
                    results['draws'] += 1
                    if verbose:
                        if game.visual:
                            print(f"{'=' * 50}")
                        print(f"Game {episode + 1}: Draw after {move_count} moves!")
                        if game.visual:
                            print(f"{'=' * 50}\n")

        # Disable visualization after last game
        if game.visual:
            game.visual = False

    # Calculate win rate
    total_decisive_games = results['agent1_wins'] + results['agent2_wins']
    if total_decisive_games > 0:
        results['agent1_win_rate'] = results['agent1_wins'] / total_decisive_games
    else:
        results['agent1_win_rate'] = 0.0

    return results


if __name__ == "__main__":
    """Example usage of the framework."""
    from mcts.games.tictactoe import TicTacToe
    from mcts.games.connect_four import ConnectFour
    from mcts.agents.random_agent import RandomAgent
    from mcts.agents.minimax_agent import MinimaxAgent

    print("=" * 60)
    print("Game Framework: Running Matches Between Agents")
    print("=" * 60)

    game1 = ConnectFour(visual=False)
    agent1 = MinimaxAgent(name="Minimax-D9", max_depth=9)
    agent2 = MinimaxAgent(name="Minimax-D3", max_depth=1)

    results = run_match(
        game=game1,
        agent1=agent1,
        agent2=agent2,
        num_episodes=20,
        verbose=True,
        render_last_game=True
    )

    print(f"\n{'=' * 60}")
    print("Final Results:")
    print(f"  {agent1.name} wins: {results['agent1_wins']}")
    print(f"  {agent2.name} wins: {results['agent2_wins']}")
    print(f"  Draws: {results['draws']}")
    print(f"  {agent1.name} win rate: {results['agent1_win_rate']:.2%}")
    print(f"{'=' * 60}\n")
