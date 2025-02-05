
import pickle

class TrieNode:
    def __init__(self):
        """Initialize a trie node with children and end-of-word marker."""
        self.children = {}  # Dictionary to store child nodes (key: letter, value: TrieNode)
        self.is_end_of_word = False  # Indicates if this node marks the end of a word

class Trie:
    def __init__(self):
        """Initialize the root of the trie."""
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the trie.

        Args:
            word (str): The word to insert.
        """
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()  # Create a new node if letter is not in children
            node = node.children[letter]
        node.is_end_of_word = True  # Mark the end of the word

    def search(self, prefix):
        """Search for a prefix in the trie.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            Tuple[bool, bool]:
                - The first boolean indicates if the prefix is a valid word.
                - The second boolean indicates if the prefix can lead to other words.
        """
        node = self.root
        for letter in prefix:
            if letter not in node.children:
                return False, False  # Prefix does not exist
            node = node.children[letter]
        return node.is_end_of_word, bool(node.children)  # Check if it's a word and/or has children

    def save(self, filename):
        """Save the trie to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        """Load a trie from a file."""
        with open(filename, 'rb') as f:
            return pickle.load(f)

# Example usage
if __name__ == "__main__":
    # Initialize the trie
    trie = Trie()

    # Load words from a file (e.g., "smallwordlist")
    with open("smallwordlist", "r") as f:
        words = [line.strip().lower() for line in f.readlines()]

    # Insert words into the trie
    for word in words:
        trie.insert(word)

     # Save the trie to a file
    trie.save("smalllistprefixtree.pkl")
    print("Trie saved!")


    # Test the trie
    test_prefix = "tango"
    is_word, has_children = trie.search(test_prefix)
    print(f"'{test_prefix}' is a word: {is_word}")
    print(f"'{test_prefix}' can lead to other words: {has_children}")
