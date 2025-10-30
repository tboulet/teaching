"""
Tests progressifs pour valider l'implémentation MCTS des étudiants.

Exécutez ce fichier pour tester votre implémentation étape par étape.
"""
from mcts.games import TicTacToe, ConnectFour
from mcts.agents import MCTSAgent, RandomAgent, MinimaxAgent
from mcts.agents.mcts_agent import MCTSNode
from mcts.run_match import run_match


def test_1_node_creation():
    """Test 1: Création de nœuds et méthodes de base."""
    print("\n" + "="*70)
    print("TEST 1: Création de nœuds et méthodes de base")
    print("="*70)

    game = TicTacToe(visual=False)
    root = MCTSNode(state=game)

    print(f"✓ Nœud racine créé")
    print(f"  - Visites: {root.visits}")
    print(f"  - Valeur: {root.value}")
    print(f"  - Actions non essayées: {len(root.untried_actions)}")

    # Test is_fully_expanded
    try:
        is_expanded = root.is_fully_expanded()
        print(f"✓ is_fully_expanded() fonctionne: {is_expanded}")
        assert is_expanded == False, "Le nœud racine ne devrait pas être complètement développé"
    except:
        print("✗ is_fully_expanded() à implémenter ou incorrect")
        return False

    # Test is_terminal
    try:
        is_term = root.is_terminal()
        print(f"✓ is_terminal() fonctionne: {is_term}")
        assert is_term == False, "Le nœud racine ne devrait pas être terminal"
    except:
        print("✗ is_terminal() à implémenter ou incorrect")
        return False

    print("\n✅ Test 1 RÉUSSI!\n")
    return True


def test_2_expansion():
    """Test 2: Expansion de nœuds."""
    print("\n" + "="*70)
    print("TEST 2: Expansion de nœuds")
    print("="*70)

    game = TicTacToe(visual=False)
    root = MCTSNode(state=game)

    try:
        initial_untried = len(root.untried_actions)
        child = root.expand()

        print(f"✓ expand() fonctionne")
        print(f"  - Actions non essayées avant: {initial_untried}")
        print(f"  - Actions non essayées après: {len(root.untried_actions)}")
        print(f"  - Enfants créés: {len(root.children)}")
        print(f"  - Action de l'enfant: {child.action}")

        assert len(root.children) == 1, "Un enfant devrait être créé"
        assert len(root.untried_actions) == initial_untried - 1, "Une action devrait être retirée"
        assert child.parent == root, "Le parent de l'enfant devrait être root"

    except Exception as e:
        print(f"✗ expand() à implémenter ou incorrect: {e}")
        return False

    print("\n✅ Test 2 RÉUSSI!\n")
    return True


def test_3_simulation():
    """Test 3: Simulation (rollout)."""
    print("\n" + "="*70)
    print("TEST 3: Simulation (rollout)")
    print("="*70)

    game = TicTacToe(visual=False)
    root = MCTSNode(state=game)

    try:
        rewards = []
        for i in range(10):
            reward = root.simulate()
            rewards.append(reward)

        print(f"✓ simulate() fonctionne")
        print(f"  - 10 simulations effectuées")
        print(f"  - Récompenses: {[f'{r:+.1f}' for r in rewards]}")
        print(f"  - Moyenne: {sum(rewards)/len(rewards):.2f}")

        # Vérifications
        assert all(r in [-1.0, 0.0, 1.0] for r in rewards), "Les récompenses doivent être -1, 0 ou 1"
        assert len(set(rewards)) > 1, "Les simulations devraient donner des résultats variés"

    except Exception as e:
        print(f"✗ simulate() à implémenter ou incorrect: {e}")
        return False

    print("\n✅ Test 3 RÉUSSI!\n")
    return True


def test_4_backpropagation():
    """Test 4: Backpropagation."""
    print("\n" + "="*70)
    print("TEST 4: Backpropagation")
    print("="*70)

    game = TicTacToe(visual=False)
    root = MCTSNode(state=game)
    child = root.expand()

    try:
        # Test backpropagation
        reward = 1.0
        child.backpropagate(reward)

        print(f"✓ backpropagate() fonctionne")
        print(f"  - Visites root: {root.visits}")
        print(f"  - Valeur root: {root.value}")
        print(f"  - Visites child: {child.visits}")
        print(f"  - Valeur child: {child.value}")

        # Vérifications
        assert root.visits == 1, "Root devrait avoir 1 visite"
        assert child.visits == 1, "Child devrait avoir 1 visite"
        assert child.value == reward, f"Child devrait avoir valeur {reward}"
        assert root.value == -reward, f"Root devrait avoir valeur {-reward} (inversée)"

    except Exception as e:
        print(f"✗ backpropagate() à implémenter ou incorrect: {e}")
        return False

    print("\n✅ Test 4 RÉUSSI!\n")
    return True


def test_5_ucb1():
    """Test 5: Sélection UCB1."""
    print("\n" + "="*70)
    print("TEST 5: Sélection avec UCB1")
    print("="*70)

    game = TicTacToe(visual=False)
    root = MCTSNode(state=game)

    try:
        # Créer plusieurs enfants avec des statistiques différentes
        for i in range(3):
            child = root.expand()
            child.backpropagate((-1) ** i)  # Alterner récompenses

        # Tester best_child
        best = root.best_child(exploration_constant=1.41)

        print(f"✓ best_child() fonctionne")
        print(f"  - Nombre d'enfants: {len(root.children)}")
        print(f"  - Meilleur enfant (action): {best.action}")
        print("\n  Statistiques des enfants:")
        for i, child in enumerate(root.children):
            avg = child.value / child.visits if child.visits > 0 else 0
            print(f"    Enfant {i} (action {child.action}): visits={child.visits}, "
                  f"value={child.value:.2f}, avg={avg:.2f}")

        assert best in root.children, "Le meilleur enfant devrait être dans la liste"

    except Exception as e:
        print(f"✗ best_child() à implémenter ou incorrect: {e}")
        return False

    print("\n✅ Test 5 RÉUSSI!\n")
    return True


def test_6_best_action():
    """Test 6: Sélection de la meilleure action."""
    print("\n" + "="*70)
    print("TEST 6: Sélection de la meilleure action")
    print("="*70)

    game = TicTacToe(visual=False)
    root = MCTSNode(state=game)

    try:
        # Créer des enfants avec différents nombres de visites
        for i in range(3):
            child = root.expand()
            for _ in range(i + 1):  # Visites croissantes
                child.backpropagate(0.5)

        # Tester best_action
        best_action = root.best_action()

        print(f"✓ best_action() fonctionne")
        print(f"  - Meilleure action: {best_action}")
        print("\n  Visites par enfant:")
        for child in root.children:
            print(f"    Action {child.action}: {child.visits} visites")

        # Le dernier enfant devrait avoir le plus de visites
        most_visited = max(root.children, key=lambda c: c.visits)
        assert best_action == most_visited.action, "L'action devrait être celle de l'enfant le plus visité"

    except Exception as e:
        print(f"✗ best_action() à implémenter ou incorrect: {e}")
        return False

    print("\n✅ Test 6 RÉUSSI!\n")
    return True


def test_7_mcts_agent():
    """Test 7: Agent MCTS complet."""
    print("\n" + "="*70)
    print("TEST 7: Agent MCTS complet")
    print("="*70)

    game = TicTacToe(visual=False)

    try:
        mcts = MCTSAgent(name="MCTS", num_simulations=50)
        action = mcts.select_action(game)

        print(f"✓ MCTSAgent.select_action() fonctionne")
        print(f"  - Action choisie: {action}")
        print(f"  - Actions légales: {game.get_legal_actions()}")

        assert action in game.get_legal_actions(), "L'action devrait être légale"

    except Exception as e:
        print(f"✗ MCTSAgent.select_action() à implémenter ou incorrect: {e}")
        return False

    print("\n✅ Test 7 RÉUSSI!\n")
    return True


def test_8_performance():
    """Test 8: Performance contre Random."""
    print("\n" + "="*70)
    print("TEST 8: Performance de MCTS vs Random")
    print("="*70)

    print("Ce test peut prendre ~30 secondes...\n")

    game = TicTacToe(visual=False)
    mcts = MCTSAgent(name="MCTS", num_simulations=200)
    random = RandomAgent(name="Random")

    try:
        results = run_match(game, mcts, random, num_episodes=20, verbose=False, render_last_game=False)

        print(f"✓ MCTS peut jouer des parties complètes")
        print(f"  - MCTS: {results['agent1_wins']}W - {results['draws']}D - {results['agent2_wins']}L")
        print(f"  - Win rate: {results['agent1_win_rate']:.0%}")

        if results['agent1_win_rate'] >= 0.6:
            print("\n✅ Excellente performance! MCTS bat Random facilement.")
        elif results['agent1_win_rate'] >= 0.4:
            print("\n⚠️  Performance acceptable mais peut être améliorée.")
            print("   Vérifiez bien la formule UCB1 et la backpropagation.")
        else:
            print("\n❌ Performance insuffisante. Vérifiez votre implémentation:")
            print("   - La formule UCB1 (n'oubliez pas le signe négatif!)")
            print("   - La backpropagation (inversion de la récompense)")
            print("   - La gestion des perspectives dans simulate()")
            return False

    except Exception as e:
        print(f"✗ Erreur pendant les matchs: {e}")
        return False

    print("\n✅ Test 8 RÉUSSI!\n")
    return True


def run_all_tests():
    """Exécute tous les tests."""
    print("\n" + "="*70)
    print("SUITE DE TESTS MCTS - VALIDATION DE VOTRE IMPLÉMENTATION")
    print("="*70)

    tests = [
        test_1_node_creation,
        test_2_expansion,
        test_3_simulation,
        test_4_backpropagation,
        test_5_ucb1,
        test_6_best_action,
        test_7_mcts_agent,
        test_8_performance,
    ]

    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"\n⚠️  Corrigez ce test avant de continuer.\n")
                break
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}\n")
            break

    print("\n" + "="*70)
    print(f"RÉSULTATS: {passed}/{len(tests)} tests réussis")
    print("="*70)

    if passed == len(tests):
        print("\n🎉 FÉLICITATIONS! Votre implémentation MCTS est complète et correcte!")
        print("\nVous pouvez maintenant:")
        print("  - Tester sur ConnectFour")
        print("  - Expérimenter avec différents nombres de simulations")
        print("  - Comparer avec Minimax")
    else:
        print(f"\n📚 Continuez! Il reste {len(tests) - passed} test(s) à réussir.")


if __name__ == "__main__":
    run_all_tests()
