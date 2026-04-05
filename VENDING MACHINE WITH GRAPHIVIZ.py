
from graphviz import Digraph


class VendingMachineFA:
    """
    States represent total money inserted:
    q0 = 0, q5 = 5, q10 = 10, q15 = 15 (accepting state)
    """

    def __init__(self):
        self.states = [0, 5, 10, 15]
        self.accept_state = 15

    def process_input(self, inputs, filename='vending_machine'):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')

        # Start node
        dot.node('start', '', shape='point')
        dot.node('q0', '₹0')
        dot.edge('start', 'q0')

        current = 0
        prev_node = 'q0'

        for i, coin in enumerate(inputs):
            next_amount = current + coin

            # Cap at 15 (machine limit)
            if next_amount > 15:
                next_amount = current
                label = f"+₹{coin} (invalid)"
            else:
                label = f"+₹{coin}"

            state_name = f'q{next_amount}'

            # Create node
            if next_amount == self.accept_state:
                dot.node(state_name, f'₹{next_amount}', shape='doublecircle')
            else:
                dot.node(state_name, f'₹{next_amount}')

            dot.edge(prev_node, state_name, label=label)

            prev_node = state_name
            current = next_amount

        # Final result inside graph
        if current == self.accept_state:
            dot.node('qf', 'ITEM', shape='doublecircle')
            dot.edge(prev_node, 'qf', label='Dispense Item')
            result = "Item Dispensed ✅"
        else:
            dot.node('qf', f'₹{current}', shape='circle')
            dot.edge(prev_node, 'qf', label='Insufficient')
            result = f"Not enough money ❌ (₹{current})"

        dot.render(filename, view=True, cleanup=True)

        return result


def main():
    vm = VendingMachineFA()

    print("Enter coins (allowed: 5, 10)")
    print("Example input: 5 5 5")

    while True:
        user_input = input("\nEnter coins sequence or 'exit': ")

        if user_input.lower() == 'exit':
            break

        try:
            coins = list(map(int, user_input.split()))

            for c in coins:
                if c not in [5, 10]:
                    print("Only 5 and 10 are allowed!")
                    raise ValueError

            result = vm.process_input(coins)
            print(result)

        except ValueError:
            print("Invalid input! Enter numbers like: 5 10 5")


if __name__ == "__main__":
    main()