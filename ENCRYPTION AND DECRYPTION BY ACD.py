"""
This system encrypts and decrypts text using Caesar cipher with a PDA.
"""

import graphviz


class EncryptionDecryptionPDA:
    """
    Pushdown Automaton for Encryption/Decryption

    States:
        q0: Initial state
        q1: Encryption mode
        q2: Decryption mode
        q3: Output state
        q4: Accept state

    Input Alphabet: All printable characters
    Stack Alphabet: {'Z', character, number}

    Algorithm: Caesar Cipher with shift = 3
    """

    def __init__(self, shift=3):
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4'}
        self.start_state = 'q0'
        self.accept_states = {'q4'}
        self.shift = shift  # Caesar cipher shift value

        # Stack symbols
        self.stack_alphabet = {'Z', 'a', 'n'}  # Z=marker, a=letter, n=number

        # Input alphabet - we'll accept any printable character
        self.input_alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ')

    def encrypt_text(self, text):
        """
        Encrypt text using Caesar cipher

        Args:
            text: Plain text to encrypt

        Returns:
            Encrypted text with step-by-step trace
        """
        encrypted = []
        trace = [{
            'step': 0,
            'state': 'q0',
            'input': 'START',
            'char': '-',
            'encrypted_char': '-',
            'stack': ['Z'],
            'description': 'Initial state'
        }]

        current_state = 'q1'  # Move to encryption state

        trace.append({
            'step': 1,
            'state': current_state,
            'input': 'encrypt',
            'char': '-',
            'encrypted_char': '-',
            'stack': ['Z'],
            'description': 'Enter encryption mode'
        })

        for step, char in enumerate(text, 2):
            if char.isalpha():
                if char.islower():
                    # Shift lowercase letter
                    shifted = chr((ord(char) - ord('a') + self.shift) % 26 + ord('a'))
                else:
                    # Shift uppercase letter
                    shifted = chr((ord(char) - ord('A') + self.shift) % 26 + ord('A'))
            else:
                shifted = char  # Non-alphabetic characters remain unchanged

            encrypted.append(shifted)

            trace.append({
                'step': step,
                'state': current_state,
                'input': char,
                'char': char,
                'encrypted_char': shifted,
                'stack': ['Z'],
                'description': f"Encrypt '{char}' → '{shifted}' (shift={self.shift})"
            })

        # Finalization
        final_step = len(text) + 2
        trace.append({
            'step': final_step,
            'state': 'q4',
            'input': 'finalize',
            'char': '-',
            'encrypted_char': '-',
            'stack': ['Z'],
            'description': 'Encryption complete - Accept state reached'
        })

        return ''.join(encrypted), trace

    def decrypt_text(self, text):
        """
        Decrypt text using Caesar cipher (reverse shift)

        Args:
            text: Encrypted text to decrypt

        Returns:
            Decrypted text with step-by-step trace
        """
        decrypted = []
        trace = [{
            'step': 0,
            'state': 'q0',
            'input': 'START',
            'char': '-',
            'decrypted_char': '-',
            'stack': ['Z'],
            'description': 'Initial state'
        }]

        current_state = 'q2'  # Move to decryption state

        trace.append({
            'step': 1,
            'state': current_state,
            'input': 'decrypt',
            'char': '-',
            'decrypted_char': '-',
            'stack': ['Z'],
            'description': 'Enter decryption mode'
        })

        for step, char in enumerate(text, 2):
            if char.isalpha():
                if char.islower():
                    # Reverse shift lowercase letter
                    shifted = chr((ord(char) - ord('a') - self.shift) % 26 + ord('a'))
                else:
                    # Reverse shift uppercase letter
                    shifted = chr((ord(char) - ord('A') - self.shift) % 26 + ord('A'))
            else:
                shifted = char  # Non-alphabetic characters remain unchanged

            decrypted.append(shifted)

            trace.append({
                'step': step,
                'state': current_state,
                'input': char,
                'char': char,
                'decrypted_char': shifted,
                'stack': ['Z'],
                'description': f"Decrypt '{char}' → '{shifted}' (shift=-{self.shift})"
            })

        # Finalization
        final_step = len(text) + 2
        trace.append({
            'step': final_step,
            'state': 'q4',
            'input': 'finalize',
            'char': '-',
            'decrypted_char': '-',
            'stack': ['Z'],
            'description': 'Decryption complete - Accept state reached'
        })

        return ''.join(decrypted), trace

    def create_automaton_diagram(self, filename='encryption_decryption_pda'):
        """
        Create visual representation of the PDA using Graphviz
        """
        dot = graphviz.Digraph(comment='Encryption/Decryption PDA', format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle', style='filled', fillcolor='lightcyan')

        # Add start state indicator
        dot.node('start', '', shape='point')
        dot.edge('start', self.start_state)

        # Add all states
        for state in self.states:
            if state in self.accept_states:
                dot.node(state, state, shape='double circle', fillcolor='light green')
            else:
                dot.node(state, state)

        # Add key transitions
        transitions_to_show = [
            ('q0', 'q1', 'encrypt, Z/Z'),
            ('q0', 'q2', 'decrypt, Z/Z'),
            ('q1', 'q1', 'a-z, A-Z, Z/Z'),
            ('q2', 'q2', 'a-z, A-Z, Z/Z'),
            ('q1', 'q4', 'ε, Z/Z'),
            ('q2', 'q4', 'ε, Z/Z'),
        ]

        for src, dst, label in transitions_to_show:
            if src == dst:
                dot.edge(src, dst, label=label, _attributes={'style': 'curved'})
            else:
                dot.edge(src, dst, label=label)

        dot.render(filename, view=False, cleanup=True)
        return f"{filename}.png"


def print_encryption_trace(original_text, encrypted_text, trace):
    """Print encryption trace"""
    print("\n" + "=" * 100)
    print("ENCRYPTION EXECUTION TRACE")
    print("=" * 100)

    print(
        f"\n{'Step':<6} {'State':<6} {'Input':<10} {'Character':<12} {'Encrypted':<12} {'Stack':<10} {'Description':<40}")
    print("-" * 100)

    for entry in trace:
        stack_repr = ''.join(entry['stack']) if entry['stack'] else 'ε'
        print(f"{entry['step']:<6} {entry['state']:<6} {str(entry['input']):<10} {str(entry['char']):<12} "
              f"{str(entry['encrypted_char']):<12} {stack_repr:<10} {entry['description']:<40}")

    print("-" * 100)
    print(f"\nOriginal Text:  {original_text}")
    print(f"Encrypted Text: {encrypted_text}")
    print(f"Final State: ACCEPTED ✓")
    print("=" * 100 + "\n")


def print_decryption_trace(encrypted_text, decrypted_text, trace):
    """Print decryption trace"""
    print("\n" + "=" * 100)
    print("DECRYPTION EXECUTION TRACE")
    print("=" * 100)

    print(
        f"\n{'Step':<6} {'State':<6} {'Input':<10} {'Character':<12} {'Decrypted':<12} {'Stack':<10} {'Description':<40}")
    print("-" * 100)

    for entry in trace:
        stack_repr = ''.join(entry['stack']) if entry['stack'] else 'ε'
        print(f"{entry['step']:<6} {entry['state']:<6} {str(entry['input']):<10} {str(entry['char']):<12} "
              f"{str(entry['decrypted_char']):<12} {stack_repr:<10} {entry['description']:<40}")

    print("-" * 100)
    print(f"\nEncrypted Text: {encrypted_text}")
    print(f"Decrypted Text: {decrypted_text}")
    print(f"Final State: ACCEPTED ✓")
    print("=" * 100 + "\n")


def display_pda_definition(pda):
    """Display PDA definition"""
    print("\n" + "█" * 100)
    print("█" + " " * 98 + "█")
    print("█" + " " * 20 + "ENCRYPTION/DECRYPTION USING PUSHDOWN AUTOMATON" + " " * 32 + "█")
    print("█" + " " * 30 + "Caesar Cipher Implementation" + " " * 40 + "█")
    print("█" + " " * 98 + "█")
    print("█" * 100)

    print("\nPUSHDOWN AUTOMATON DEFINITION:")
    print("-" * 100)
    print(f"States (Q): {pda.states}")
    print(f"Start State: {pda.start_state}")
    print(f"Accept States (F): {pda.accept_states}")
    print(f"Input Alphabet (Σ): All printable characters")
    print(f"Stack Alphabet (Γ): {pda.stack_alphabet}")
    print(f"Cipher Type: Caesar Cipher with shift = {pda.shift}")
    print("=" * 100)


def get_user_input_for_encryption():
    """Get text from user for encryption"""
    print("\n" + "┌" + "─" * 98 + "┐")
    print("│" + " " * 98 + "│")
    print("│" + "  Enter text to ENCRYPT".center(98) + "│")
    print("│" + "  (Use letters, numbers, spaces - only letters will be encrypted)".center(98) + "│")
    print("│" + " " * 98 + "│")
    print("└" + "─" * 98 + "┘")

    while True:
        text = input("\n📝 Enter text to encrypt: ").strip()

        if not text:
            print("❌ Please enter some text!")
            continue

        return text


def get_user_input_for_decryption():
    """Get text from user for decryption"""
    print("\n" + "┌" + "─" * 98 + "┐")
    print("│" + " " * 98 + "│")
    print("│" + "  Enter text to DECRYPT".center(98) + "│")
    print("│" + "  (Use letters, numbers, spaces)".center(98) + "│")
    print("│" + " " * 98 + "│")
    print("└" + "─" * 98 + "┘")

    while True:
        text = input("\n🔓 Enter text to decrypt: ").strip()

        if not text:
            print("❌ Please enter some text!")
            continue

        return text


def display_menu():
    """Display menu options"""
    print("\n" + "┌" + "─" * 50 + "┐")
    print("│" + "  MENU OPTIONS".center(50) + "│")
    print("│" + "─" * 50 + "│")
    print("│" + "  1. Encrypt Text".ljust(50) + "│")
    print("│" + "  2. Decrypt Text".ljust(50) + "│")
    print("│" + "  3. Both (Encrypt then Decrypt)".ljust(50) + "│")
    print("│" + "  4. Exit".ljust(50) + "│")
    print("└" + "─" * 50 + "┘")

    while True:
        choice = input("\n🔤 Choose option (1-4): ").strip()

        if choice in ['1', '2', '3', '4']:
            return choice
        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")


def main():
    """Main interactive function"""
    pda = EncryptionDecryptionPDA(shift=3)

    display_pda_definition(pda)

    while True:
        choice = display_menu()

        if choice == '1':
            # Encrypt only
            text = get_user_input_for_encryption()
            encrypted_text, enc_trace = pda.encrypt_text(text)
            print_encryption_trace(text, encrypted_text, enc_trace)
            print(f"✓ Result: '{text}' → '{encrypted_text}'")

        elif choice == '2':
            # Decrypt only
            text = get_user_input_for_decryption()
            decrypted_text, dec_trace = pda.decrypt_text(text)
            print_decryption_trace(text, decrypted_text, dec_trace)
            print(f"✓ Result: '{text}' → '{decrypted_text}'")

        elif choice == '3':
            # Both encrypt and decrypt
            text = get_user_input_for_encryption()
            encrypted_text, enc_trace = pda.encrypt_text(text)
            print_encryption_trace(text, encrypted_text, enc_trace)
            print(f"✓ Encryption Result: '{text}' → '{encrypted_text}'")

            # Now decrypt
            decrypted_text, dec_trace = pda.decrypt_text(encrypted_text)
            print_decryption_trace(encrypted_text, decrypted_text, dec_trace)
            print(f"✓ Decryption Result: '{encrypted_text}' → '{decrypted_text}'")

            # Verify
            if decrypted_text == text:
                print("✓✓✓ VERIFICATION SUCCESSFUL - Decrypted text matches original! ✓✓✓\n")
            else:
                print("✗ VERIFICATION FAILED - Mismatch detected!\n")

        elif choice == '4':
            print("\n" + "█" * 100)
            print("█" + " Thank you for using the Encryption/Decryption System!".center(98) + "█")
            print("█" * 100 + "\n")
            break

        # Ask if user wants to continue
        print("\n" + "─" * 100)
        again = input("🔄 Do you want to perform another operation? (yes/no): ").strip().lower()

        if again not in ['yes', 'y']:
            print("\n" + "█" * 100)
            print("█" + " Thank you for using the Encryption/Decryption System!".center(98) + "█")
            print("█" * 100 + "\n")
            break


if __name__ == "__main__":
    main()
