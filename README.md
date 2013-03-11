boggle
======

A boggle game solver

This is a two step program:
- Generate a board:
    - Get the dice from the text file
    - Randomly select a letter from a random die

- Build tools to solve the board as quickly as possible
    - Build a trie from the dictionary.
    - Build all string from the boggle board.
    - Return any string that fits in the trie.


I chose to work with python because it is light & flexible.
When considering such a program, where I potentially have to deal with
15 septillion words (ie. 25 factorial), I want it to be fast.

To go through the board, I use depth first via a recursive fuction, but
that does not prevent me from reusing a given vertex in a word.
In order to avoid that, I implemented a stack on which I put the letter
currently in use and remove them whenever I backtrace.

Once I have generated all the words from the board, I use the prefix
tree to find and return the existing words.

Here is an example:
http://www.shiftout.net/~cydanil/cs2011/sample.html
http://www.shiftout.net/~cydanil/cs2011/bogglesample.dot

The english alphabet is constitued of 26 letters.
Given that alphabet, each vertex might have up to 26 childs, which in
turns have 26 children and so on...
Therefore, the order of complexity is:
    - in space, O(W), which is the sum of all characters in
      the dictionary
    - in time, O(AL), which stands for the size A of the alphabet
      multiplied by the length L of the generated string.

To optimize the need of time, but space mainly. I chose to create a
regular expression object which imports only the word containing the
letters from an alphabet created with the board letters.

I however haven't implemented a proper graph structure, but instead use
a combination of sets and stacks.

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
