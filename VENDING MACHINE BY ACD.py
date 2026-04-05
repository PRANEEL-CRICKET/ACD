"""
This system accepts coins from user and dispenses items when Rs 20 is reached.
"""
from collections import defaultdict

import graphviz
def get_state_info(state):
    """Get information about a state"""
    descriptions = {
        'q0': 'Initial/Idle State - Waiting for coins',
        'q1': 'State q1 - Rs 5 accumulated',
        'q2': 'State q2 - Rs 10 accumulated',
        'q3': 'State q3 - Rs 15 accumulated',
        'q4': 'Accept State - Item Dispensed (Rs 20+)',
        'q5': 'Refund State - Money returned'
    }
    return descriptions.get(state, 'Unknown state')


class VendingMachineFA:
    """
    Finite Automaton for Vending Machine

    States:
        q0: Initial state (idle, waiting for first coin)
        q1: Rs 5 received
        q2: Rs 10 received
        q3: Rs 15 received
        q4: Rs 20+ received (accepting state - dispense item)
        q5: Refund state

    Input Alphabet: {'5', '10', '20', 'refund'}
    Item Price: Rs 20
    """

    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
        self.start_state = 'q0'
        self.accept_states = {'q4'}
        self.input_alphabet = {'5', '10', '20', 'refund'}

        # Transition table: (current_state, input) -> next_state
        self.transitions = {
            ('q0', '5'): 'q1',  # 5 rupees
            ('q0', '10'): 'q2',  # 10 rupees
            ('q0', '20'): 'q4',  # 20 rupees - item dispensed
            ('q0', 'refund'): 'q5',  # Refund

            ('q1', '5'): 'q2',  # 5+5 = 10
            ('q1', '10'): 'q3',  # 5+10 = 15
            ('q1', '20'): 'q4',  # 5+20 = 25 - item dispensed
            ('q1', 'refund'): 'q5',  # Refund 5 rupees

            ('q2', '5'): 'q3',  # 10+5 = 15
            ('q2', '10'): 'q4',  # 10+10 = 20 - item dispensed
            ('q2', '20'): 'q4',  # 10+20 = 30 - item dispensed
            ('q2', 'refund'): 'q5',  # Refund 10 rupees

            ('q3', '5'): 'q4',  # 15+5 = 20 - item dispensed
            ('q3', '10'): 'q4',  # 15+10 = 25 - item dispensed
            ('q3', '20'): 'q4',  # 15+20 = 35 - item dispensed
            ('q3', 'refund'): 'q5',  # Refund 15 rupees

            ('q4', '5'): 'q4',  # Already dispensed
            ('q4', '10'): 'q4',
            ('q4', '20'): 'q4',
            ('q4', 'refund'): 'q5',  # Refund excess amount

            ('q5', '5'): 'q5',  # Refund state
            ('q5', '10'): 'q5',
            ('q5', '20'): 'q5',
            ('q5', 'refund'): 'q0'  # Return to initial state
        }

        # State to amount mapping for visualization
        self.state_amount = {
            'q0': 0,
            'q1': 5,
            'q2': 10,
            'q3': 15,
            'q4': 20,
            'q5': 0
        }

    def process_input(self, input_string):
        """
        Process input sequence and trace through FA

        Args:
            input_string: Space-separated coins (e.g., "5 10 5")

        Returns:
            Tuple of (trace, current_state, total_amount, accepted)
        """
        coins = input_string.strip().split()
        current_state = self.start_state
        total_amount = 0
        trace = [{
            'step': 0,
            'state': current_state,
            'input': 'START',
            'total': total_amount,
            'description': 'Initial state - Waiting for coins'
        }]

        for step, coin in enumerate(coins, 1):
            if coin not in self.input_alphabet:
                return trace, current_state, total_amount, False, f"Invalid input: {coin}"

            next_state = self.transitions.get((current_state, coin))

            if next_state is None:
                return (trace, current_state, total_amount, False,
                        f"No transition defined for ({current_state}, {coin})")

            # Update total amount
            if coin != 'refund':
                total_amount += int(coin)
            else:
                total_amount = 0

            # Determine description
            if next_state == 'q4':
                description = f"Item dispensed! Amount received: Rs {total_amount}"
            elif next_state == 'q5':
                description = "Processing refund..."
            else:
                description = f"Total amount accumulated: Rs {total_amount}"

            trace.append({
                'step': step,
                'state': next_state,
                'input': coin,
                'total': total_amount,
                'description': description
            })

            current_state = next_state

        accepted = current_state in self.accept_states
        return trace, current_state, total_amount, accepted, "Process completed successfully"

    def create_automaton_diagram(self, filename='vending_machine_fa'):
        """
        Create visual representation of the automaton using Graphviz
        """
        dot = graphviz.Digraph(comment='Vending Machine FA', format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle', style='filled', fillcolor='lightblue')

        # Add start state indicator
        dot.node('start', '', shape='point')
        dot.edge('start', self.start_state)

        # Add all states
        for state in self.states:
            if state in self.accept_states:
                dot.node(state, state, shape='double circle', fillcolor='light green')
            elif state == 'q5':
                dot.node(state, state, fillcolor='light yellow')
            else:
                dot.node(state, state)

        # Add transitions, grouping by source and destination
        edges = defaultdict(list)
        for (src, inp), dst in self.transitions.items():
            edges[(src, dst)].append(inp)

        for (src, dst), inputs in edges.items():
            label = ', '.join(inputs)
            dot.edge(src, dst, label=label)

        dot.render(filename, view=False, cleanup=True)
        return f"{filename}.png"


def print_execution_trace(trace, current_state, total_amount, accepted, message):
    """Print detailed execution trace"""
    print("\n" + "=" * 80)
    print("EXECUTION TRACE - VENDING MACHINE FA")
    print("=" * 80)

    print("\nStep-by-Step Transitions:")
    print("-" * 80)
    print(f"{'Step':<6} {'Current State':<15} {'Input':<10} {'Next State':<15} {'Amount':<10}")
    print("-" * 80)

    for i, entry in enumerate(trace):
        if entry['step'] == 0:
            print(f"{entry['step']:<6} {entry['state']:<15} {'-':<10} {'-':<15} {entry['total']:<10}")
        else:
            prev_state = trace[i - 1]['state']
            print(
                f"{entry['step']:<6} {prev_state:<15} {entry['input']:<10} {entry['state']:<15} Rs {entry['total']:<7}")
            print(f"       {entry['description']}")

    print("-" * 80)
    print(f"\nFinal State: {current_state}")
    print(f"Final Amount: Rs {total_amount}")
    print(f"Status: {'ACCEPTED ✓' if accepted else 'REJECTED ✗'}")
    print(f"Message: {message}")
    print("=" * 80 + "\n")


def display_fa_definition(vm):
    """Display FA definition"""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "VENDING MACHINE IMPLEMENTATION" + " " * 28 + "█")
    print("█" + " " * 25 + "Using Finite Automaton (FA)" + " " * 26 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)

    print("\nFINITE AUTOMATON DEFINITION:")
    print("-" * 80)
    print(f"States (Q): {vm.states}")
    print(f"Start State (q0): {vm.start_state}")
    print(f"Accept States (F): {vm.accept_states}")
    print(f"Input Alphabet (Σ): {vm.input_alphabet}")
    print(f"Item Price: Rs 20")

    print("\nSTATE DESCRIPTIONS:")
    print("-" * 80)
    for state in sorted(vm.states):
        print(f"{state}: {vm.get_state_info(state)}")

    print("\n" + "=" * 80)


def get_user_input():
    """Get input from user"""
    print("\n" + "┌" + "─" * 78 + "┐")
    print("│" + " " * 78 + "│")
    print("│" + "  Enter coins separated by spaces".center(78) + "│")
    print("│" + "  Example: 5 10 5  or  10 10  or  20".center(78) + "│")
    print("│" + "  Use 'refund' to get money back".center(78) + "│")
    print("│" + "  Available coins: 5, 10, 20 rupees".center(78) + "│")
    print("│" + " " * 78 + "│")
    print("└" + "─" * 78 + "┘")

    while True:
        user_input = input("\n💰 Enter coins: ").strip()

        if not user_input:
            print("❌ Please enter at least one coin!")
            continue

        # Validate input
        coins = user_input.split()
        valid = True
        for coin in coins:
            if coin not in {'5', '10', '20', 'refund'}:
                print(f"❌ Invalid coin '{coin}'. Use: 5, 10, 20, or 'refund'")
                valid = False
                break

        if valid:
            return user_input
        else:
            print("❌ Please try again!")


def main():
    """Main interactive function"""
    vending_machine = VendingMachineFA()

    while True:
        user_coins = get_user_input()

        trace, current_state, total_amount, accepted, message = vending_machine.process_input(user_coins)

        print_execution_trace(trace, current_state, total_amount, accepted, message)

        print("\n" + "─" * 80)
        again = input("🔄 Do you want to try again? (yes/no): ").strip().lower()

        if again not in ['yes', 'y']:
            print("\n" + "█" * 80)
            print("█" + " Thank you for using the Vending Machine!".center(78) + "█")
            print("█" * 80 + "\n")
            break


if __name__ == "__main__":
    main()
