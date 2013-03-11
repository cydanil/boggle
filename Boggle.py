#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  untitled.py
#
#  Copyright 2011 Cyril Danilevski <cydanil@shiftout.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

"""
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
"""

import random
import re

# The following, till the line, is designed to get & build the data.

dice = []
for line in open('dices.txt'):
    line = str.strip(line)
    dice.append(line)


""" creates and returns us a board in form of five strings enclosed
    in an array. You can set you own data by commenting line 97 to 106
    and putting 5 strings of length 5 into the board array."""

board = []
for line in range(5):
    board.append('')
    for column in range(5):
        die = random.choice(dice)
        dice.remove(die)
        board[line] += random.choice(die)

for element in board:
    print element


""" creates an alphabet from the board."""
alphabet = ''.join(set(''.join(board)))
print alphabet


""" creates the criterias we'll be looking for in the dictionary"""
criterias = re.compile('[' + alphabet + ']{3,}$', re.IGNORECASE)

""" creates a dictionary from the dictionary file. All the imported
    words are to match the alphabet previously created"""
dictionary = set(word
                    for word in open('dictionary.txt').read().splitlines()
                    if criterias.match(word))
"""creates a set of parents in an array, which is how I store my trie"""
parents = set(word[:i]
                for word in dictionary
                for i in range(2, len(word)+1))

############# The bit of magic you're looking for #############
output = []


def fightTime():
    """ To make my very own life easier, my board is made of five strings
        Therefore I first get the next string in the array (coordinate y)
        and then the next letter in the string (coordinate x).
    """
    for y, line in enumerate(board):
        for x, column in enumerate(line):
            for validWord in trie(column, ([y, x], )):
                print 'check'


def trie(word, route):
    """
        Looks up the prefix tree.
        If the word given as argument is in the dictionary, return it.
        In any case, try to add the next letter to see if it fits as well.
        If is does not, abandon this way and go check the next vertex.

        If you desire to analyse the routes taken by the algorithm,
        replace the yield statement with:
        yield (word, route)
    """
    if word in dictionary:
        yield(word)

    for(column, row) in verticesInRange(route[-1]):
        if(column, row) not in route:
            prefix2 = word + board[column][row]
            if prefix2 in parents:
                for validWord in trie(prefix2, route + ([column, row], )):
                    output.append(validWord)


def verticesInRange((c, r)):
    """ Returns the vertices in range according to the rules of boggle.
        The expected input are the coordinates of the letter in the grid
        (column, row).
    """
    for column in range(max(0, c-1), min(5, c+2)):
        for row in range(max(0, r-1), min(5, r+2)):
            yield (column, row)


if __name__ == '__main__':
    fightTime()

    output = list(set(output))
    for element in output:
        print element

    print len(output)
