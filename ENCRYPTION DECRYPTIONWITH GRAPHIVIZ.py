
from graphviz import Digraph


class EncryptionDecryptionPDA:

    def __init__(self, shift=3):
        self.shift = shift

    def encrypt_char(self, char):
        if char.isalpha():
            if char.islower():
                return chr((ord(char) - ord('a') + self.shift) % 26 + ord('a'))
            else:
                return chr((ord(char) - ord('A') + self.shift) % 26 + ord('A'))
        return char

    def decrypt_char(self, char):
        if char.isalpha():
            if char.islower():
                return chr((ord(char) - ord('a') - self.shift) % 26 + ord('a'))
            else:
                return chr((ord(char) - ord('A') - self.shift) % 26 + ord('A'))
        return char

    def create_dynamic_graph(self, text, mode, filename='pda_dynamic'):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')

        # Start node
        dot.node('start', '', shape='point')
        dot.node('q0', 'q0')
        dot.edge('start', 'q0')

        prev_node = 'q0'
        result_text = ""

        for i, char in enumerate(text):
            state_name = f'q{i+1}'

            # Process character
            if mode == 'encrypt':
                new_char = self.encrypt_char(char)
            else:
                new_char = self.decrypt_char(char)

            result_text += new_char

            dot.node(state_name, state_name)

            # Edge label shows transformation
            dot.edge(prev_node, state_name, label=f"{char} → {new_char}")

            prev_node = state_name

        # Final state
        dot.node('qf', 'qf', shape='double circle')
        dot.edge(prev_node, 'qf', label='end')

        # Render AFTER building graph
        dot.render(filename, view=True, cleanup=True)

        return result_text


def main():
    pda = EncryptionDecryptionPDA()

    while True:
        print("\n1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            text = input("Enter text to encrypt: ")
            result = pda.create_dynamic_graph(text, 'encrypt')
            print("Encrypted Text:", result)

        elif choice == '2':
            text = input("Enter text to decrypt: ")
            result = pda.create_dynamic_graph(text, 'decrypt')
            print("Decrypted Text:", result)

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()