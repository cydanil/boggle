# boggle

A boggle game solver

This is a two step program:
- Generate a board:
    - Get the dice from the text file
    - Randomly select a letter from a random die

- Build tools to solve the board as quickly as possible
    - Build a trie from the dictionary.
    - Build all string from the boggle board.
    - Return any string that fits in the trie.

There might be as much as 15 septillion words (ie. 25 factorial).

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

The `words_alpha.txt` comes from https://github.com/dwyl/english-words

Dice were compiled from the English listing found here:
https://boardgames.stackexchange.com/questions/29264/boggle-what-is-the-dice-configuration-for-boggle-in-various-languages
