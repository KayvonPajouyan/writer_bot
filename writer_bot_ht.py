"""
    File: writer_bot_ht.py
    Author: Kayvon Pajouyan
    Purpose: Generates random text from a given source text by using the
                markov chain analysis using a hashtable.
"""

import sys
import random

class Hashtable:
    """This class represents a 2d list of keys and their values as
        a list.

       The constructor creates a list that is sized up to an input.

       The class uses the hashing method in order to search for values
        put values in the list.
    """

    def __init__(self, size):
        """Creates the 2d list attribute as _pairs for the Hashtable class.

           Parameters: size is an integer

           Returns: Returns nothing but creates the Hashtable list.
        """
        
        # each element will be a key/value pair
        self._pairs = [None] * size
        self._size = size

    def put(self, key, value):
        """Puts a key and its value into the _pairs list using the 
            hasing method.
  
        Parameters: key is a string. 
                    value is going to be a list of strings for this
                    specfic program.
    
        Returns: Nothing.
        """

        # checks directily the hash key index value
        hash_index = self._hash(key)
        if self._pairs[hash_index] == None:
            self._pairs[hash_index] = [key, value]

        # uses linear probing to place key/value
        else:
            hash_probing = hash_index - 1
            found_empty_slot = False

            while not found_empty_slot:

                # Wrap around to the end of the list
                if hash_probing == -1:
                    hash_probing = self._size - 1

                if hash_probing != hash_index and\
                    self._pairs[hash_probing] == None:
                    self._pairs[hash_probing] = [key, value]
                    found_empty_slot = True

                hash_probing -= 1

    def get(self, key):
        """Searches for a value inside the hashtable based on the given
            key using hasing to find the key.
  
        Parameters: key is a string. 
    
        Returns: Returns the corresponding value of the key.
        """

        # finds directily the hash key index value
        hash_index = self._hash(key)
        if self._pairs[hash_index] is not None and\
            self._pairs[hash_index][0] == key:
            return self._pairs[hash_index][1]
        
        else:
            # uses linear probing to find key/value
            hash_probing = hash_index - 1
            while self._pairs[hash_probing] is not None:
                if self._pairs[hash_probing][0] == key:
                    return self._pairs[hash_probing][1]
                hash_probing -= 1
                if hash_probing == 0:
                    # Wrap around to the end of the list
                    hash_probing = self._size - 1
            return None

    def __contains__(self, key):
        """Looks up key in the hash table and if found returns True
            and otherwise returns False..
  
        Parameters: key is a string. 
    
        Returns: Returns True or False.
        """

        # finds directily the hash key index value
        hash_index = self._hash(key)
        if self._pairs[hash_index] is not None and\
            self._pairs[hash_index][0] == key:
            return True
        else:
            # uses linear probing to find key/value
            hash_probing = hash_index - 1
            while self._pairs[hash_probing] is not None:
                if self._pairs[hash_probing][0] == key:
                    return True
                hash_probing -= 1
                if hash_probing == 0:
                    # Wrap around to the end of the list
                    hash_probing = self._size - 1
            return False

    def _hash(self, key):
        """Creates an index value based of the given key.
  
        Parameters: key is a string. 
    
        Returns: An intger used for the index of the hashtable.
        """

        p = 0
        for c in key:
            p = 31 * p + ord(c)
        return p % self._size

    def __str__(self):
        return "{}".format(self._pairs)

def file_reader(file):
    """Reads a txt file and creates a list of all the words in the file.
  
    Parameters: file is a txt file that is used to create the list of 
                words.
  
    Returns: Returns a list of all the words in the file.
    """
    
    file = open(file, "r")
    words_list = []
    for line in file:
        line_list = line.strip().split()
        words_list += line_list
    file.close()
    return words_list
    

def markov_hashtable_maker(file, prefix_length, size):
    """Creates a hashtable based on the markov chain to later be used 
        for creating a randomaly generated text.
  
    Parameters: file is a txt file that is used to created the markov
                dictionary chain.
                prefix_length is an integer that determines the amount 
                of prefixes used in the key for the markov dictionary.
                size is a integer that determines the size of the hash
                table
  
    Returns: Returns a hashtable of the markov chain.
    """

    NONWORD = "@"
    markov = Hashtable(size) 

    # reads the file to create a list of words
    words_list = file_reader(file)

    # inserts NONEWORD into the begining of the word list
    for i in range(prefix_length):
        words_list.insert(0, NONWORD)

    # creates the markov hashtable
    for i in range(len(words_list) - prefix_length):
        prefix = ""
        for word in words_list[i: prefix_length + i]:
            for char in word:
                prefix += char
            prefix += " "
        if markov.get(prefix) == None:
            markov.put(prefix, [words_list[i + prefix_length]])
        else:
            markov.get(prefix).append(words_list[i + prefix_length])

    return markov

def build_markov_chain(file, prefix_length, size):
    """Creates the markov_chain using a input file and uses it 
        to create a list of randomly generated word ased on the
        markov chain.
  
    Parameters: file is a txt file that is used to created the markov
                dictionary chain.
                prefix_length is an integer that determines the amount 
                of prefixes used in the key for the markov dictionary.
                size is a integer that determines the size of the hash
                table
  
    Returns: Returns a list of randomly generated words.
    """

    # creates the markov dictionary and makes generated word list
    markov = markov_hashtable_maker(file, prefix_length, size)
    text_lst = file_reader(file)
    tlist = text_lst[:prefix_length] 
    prefix = ""
    for word in tlist:
        for char in word:
            prefix += char
        prefix += " "

    # creates the list of generated words
    while prefix in markov:
        # randomly choose a word if there are more than one suffixes
        if len(markov.get(prefix)) > 1:
            next_word = markov.get(prefix)\
                [random.randint(0, len((markov.get(prefix)))-1)]
            tlist.append(next_word)
            prefix = ""
            for word in tlist[-prefix_length:]:
                for char in word:
                    prefix += char
                prefix += " "

        # chooses the only suffix if there is only one suffix 
        else:
            next_word = markov.get(prefix)[0]
            tlist.append(next_word)
            prefix = ""
            for word in tlist[-prefix_length:]:
                for char in word:
                    prefix += char
                prefix += " "

    return tlist

def print_tlist(tlist, number_words):
    """Prints out the randomaly generated words making a maxium
       of 10 words per a line.
  
    Parameters: tlist is a list of the randomly generated words
                number_words is an integer of how many words
                are desired to be printed out.
  
    Returns: Prints out the randomly generated text.
    """

    for i in range(0, number_words, 10):
        # prints every line but the last line
        if (number_words - i) > 10:
            print(" ".join(tlist[i:i+10]))

        # prints the last line
        else:
            print(" ".join(tlist[i:i+(number_words-i)]))

def main():
    """Ties all the funtions together, creating the markov hashtable
        and generating random words into a list, then printing out
        the list of generated words.
  
    Parameters: No paramaters, but does take a user input for the input
                file and inputs for the length of the generated txt, as 
                well as how many prefixes being used in the markov analysis.
  
    Returns: Prints out the generated text.
    """

    SEED = 8
    random.seed(SEED)

    sfile = input()
    hash_size = int(input())
    number_prefix = int(input())
    number_of_words = int(input())

    # The error checker check if the given inputs are correct
    if number_prefix < 1 == True:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    if len(file_reader(sfile)) < 1 == True:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)
    if number_of_words < 1 ==True:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)

    generated_chain = build_markov_chain(sfile, number_prefix, hash_size)
    print_tlist(generated_chain, number_of_words)

main()