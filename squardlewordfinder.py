
import pickle

class TrieNode:
    def __init__(self):
        #Initialize a trie node with children and end-of-word marker.
        self.children = {}  # Dictionary to store child nodes (key: letter, value: TrieNode)
        self.is_end_of_word = False  # Indicates if this node marks the end of a word

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        #Insert a word into the trie.
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()  # Create a new node if letter is not in children
            node = node.children[letter]
        node.is_end_of_word = True  # Mark the end of the word

    def search(self, prefix):
        #Search for a prefix in the trie.
        node = self.root
        for letter in prefix:
            if letter not in node.children:
                return False, False  # Prefix does not exist
            node = node.children[letter]
        return node.is_end_of_word, bool(node.children)  # Check if it's a word and/or has children

    @staticmethod
    def load(filename):
        #Load a trie from a file.
        with open(filename, 'rb') as f:
            return pickle.load(f)


class SquaredleSolver:
    def __init__(self, matrix, trie):
        self.matrix = matrix  # The 4x4 matrix of letters
        self.trie = trie  # The Trie object containing valid words
        self.dimension = len(matrix)
        self.words_found = set()  # Set to store the words found

        self.visited = [[False for _ in range(self.dimension)] for _ in range(self.dimension)]  # 4x4 visited grid to track letters

    # Directions for neighbors (horizontal, vertical, and diagonal)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Up, Down, Left, Right
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals

    def dfs(self, row, col, current_word):
        #Perform DFS to search for valid words in the matrix.
        # Check if the current word is valid and has at least 4 characters
        is_word, has_children = self.trie.search(current_word)
        if len(current_word) >= 4:
            if is_word and current_word not in self.words_found:
                self.words_found.add(current_word)

        # If there are no children for the current word, stop searching further
        if not has_children:
            return

        # Explore neighbors
        for dr, dc in self.directions:
            new_row, new_col = row + dr, col + dc
            # Check if the new position is within bounds and not visited
            if 0 <= new_row < self.dimension and 0 <= new_col < self.dimension and not self.visited[new_row][new_col]:
                self.visited[new_row][new_col] = True
                # Recursively search from the neighbor
                self.dfs(new_row, new_col, current_word + self.matrix[new_row][new_col])
                self.visited[new_row][new_col] = False  # Unmark the cell after visiting

    def solve(self):
        #Solve the Squaredle puzzle by searching all possible words.
        for row in range(self.dimension):
            for col in range(self.dimension):
                # Start DFS from each letter in the matrix
                self.visited[row][col] = True
                self.dfs(row, col, self.matrix[row][col])
                self.visited[row][col] = False

        return self.words_found


# Load the trie from the saved file
trie = Trie.load('largelistprefixtree.pkl')

# Example 4x4 matrix of letters
matrix = [
    ['d', 'i', 'c', 'o'],
    ['i', 'n', 'm', 'p'],
    ['v', 'x', 'e', 'l'],
    ['i', 'd', 'u', 'a'],
]

# Solve the Squaredle puzzle
solver = SquaredleSolver(matrix, trie)
found_words = solver.solve()

# Print the found words
print("Found " + str(len(found_words)) + " words:", sorted(found_words))

