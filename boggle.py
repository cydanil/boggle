"""
This is a two step program:
- Generate a board:
    - Get the dice from the text file
    - Randomly select a letter from a random die
- Build tools to solve the board as quickly as possible
    - Build a trie from the dictionary.
    - Build all string from the boggle board.
    - Return any string that fits in the trie.


The board is navigated using depth-first via a recursive fuction, but
without being constrained from reusing a given vertex in a word.
In order to avoid that, there is a stack on which the letters currently in use
are stored, and popped when backtracking.

Once all words are generated, use the prefix tree to find and return valid
words.

The english alphabet is constitued of 26 letters.
Given that alphabet, each vertex might have up to 26 childs, which in
turns have 26 children and so on...
Therefore, the order of complexity is:
    - in space, O(W), which is the sum of all characters in
      the dictionary
    - in time, O(AL), which stands for the size A of the alphabet
      multiplied by the length L of the generated string.

To optimize time and space, a regular expression imports only the word
containing the letters from an alphabet created with the board letters.

dice : this is a simple array containing strings from the dice.txt file
board : this array contains five strings made of random characers from
        the dice.
alphabet : a string made from the board where each letter is unique.
criterias : a pattern used to import words from the dictionary file.
            It has a arguments the alphabet, a minimum length of 3,
            ignoring the case.
dictionary : a set of word from the dictionary file fitting the criterias.
parents : this set contains prefixes of the dictionary words, which is
          how I represent my graph.
output : a list containing the words found, each entry is unique.
"""
import random
import re

dice = []

with open('dice.txt', 'r') as fin:
    dice = [l.strip() for l in fin.readlines()]
print(dice)


# Create and return a board in form of five strings in an array.
# You can set you own data by commenting line 97 to 106
# and putting 5 strings of length 5 into the board array.

board = []
for line in range(5):
    board.append('')
    for column in range(5):
        die = random.choice(dice)
        dice.remove(die)
        board[line] += random.choice(die)

for element in board:
    print(element)


# Create an alphabet from the board.
alphabet = ''.join(set(''.join(board)))
print(alphabet)

# Create the criteria we'll be looking for in the dictionary
criterias = re.compile('[' + alphabet + ']{3,}$', re.IGNORECASE)

# Create a dictionary from the dictionary file.
# All imported words match the alphabet.
dictionary = set(word
                 for word in open('words_alpha.txt').read().splitlines()
                 if criterias.match(word))

# Create a set of parents in an array, which is how the trie is stored
parents = set(word[:i] for word in dictionary for i in range(2, len(word)+1))

output = []


def solve():
    """The board is made of five strings.

    First get the next string in the array (coordinate y)
    and then the next letter in the string (coordinate x).
    """
    for y, line in enumerate(board):
        for x, column in enumerate(line):
            for valid_word, route in trie(column, ([y, x],)):
                print(valid_word, route)


def trie(word, route):
    """Look up the prefix tree.

    If the word given as argument is in the dictionary, return it.
    In any case, try to add the next letter to see if it fits as well.
    If is does not, abandon this way and go check the next vertex.

    If you desire to analyse the routes taken by the algorithm,
    replace the yield statement with:
        yield(word, route)
    """
    if word in dictionary:
        yield(word, route)
    for(column, row) in vertices_in_range(*route[-1]):
        if(column, row) not in route:
            prefix2 = word + board[column][row]
            if prefix2 in parents:
                for valid_word in trie(prefix2, route + ([column, row], )):
                    output.append(valid_word)


def vertices_in_range(c, r):
    """Returns the vertices in range according to the rules of boggle.

    The expected input are the coordinates of the letter in the grid
    (column, row).
    """
    for column in range(max(0, c-1), min(5, c+2)):
        for row in range(max(0, r-1), min(5, r+2)):
            yield (column, row)


if __name__ == '__main__':
    solve()

    output = list(set(output))
    for element in output:
        print(element)

    print(len(output))
