#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 17:00:16 2020
Let's play the Hangman game with the computer!

@author: Juliana
"""

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


def is_word_guessed( W, g):
    """
    

    Parameters
    ----------
    W : string
        DESCRIPTION: string containing the secret word in the game HANGMAN
    g : list of strings
        DESCRIPTION: letters guessed in the game

    Returns
    -------
    True if secret word has been guessed other wise returns False

    """
    
    W_list = list(W) # a copy of th e list g
    W_list_copy = W_list[:]
    for char1 in g:
        for i,char2 in enumerate(W_list):
            if char1==char2:
                W_list_copy.remove(char1)
           
    
    return not W_list_copy


def get_guessed_word ( W, g):
    """
    

    Parameters
    ----------
     W : string
        DESCRIPTION: string containing the secret word in the game HANGMAN
    g : list of strings
        DESCRIPTION: letters guessed in the game
        
    Returns
    -------
    A string that is comprised of letters and underscores, based on what letters
    in letters_guessed​ are in ​secret_word​. 

    """
    #letters = ''
    list_letters = [' _ ' for _ in range(len(W))]
    for char1 in g:
        for i, char2 in enumerate(W):
            if char1 == char2:
                list_letters[i] = char1
    
    # list_letters is a list with the letters and blank spaces, we need to return a string
    # it can be done by this for loop or using join method
    # for j in range(len(list_letters)):
    #     letters = letters + list_letters[j]
    
    return ''.join(list_letters)
        
            
def get_available_letters( guessed ):
    """
    

    Parameters
    ----------
    guessed : list of strings
        DESCRIPTION: contains all guessed letters

    Returns
    -------
    A string of all the english lowercase letters that are not in guessed, ordered
    in alphabetical order

    """
    all_letters = string.ascii_lowercase
    
    available_letters = all_letters.translate({ord(char): None for char in guessed})
        
        
    return available_letters



def is_vowel(letter):
    """
    

    Parameters
    ----------
    letter (string): string in alphabet

    Returns
    -------
    True if letter is either a,e,i,o,u. Returns False otherwise

    """
    vowels = 'aeiou'
    return letter in vowels

#secret_word = choose_word(wordlist)
def hangman( secret_word ):
    """
    

    Parameters
    ----------
    secret_word : string, the secret word to be guessed
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.

    Returns
    -------
    None.

    """
    warnings = 3
    len_uniq_secret_word = len(set(secret_word))
    num_guesses = len_uniq_secret_word + 2
    letters = ''
    list_letters_guesed = []
    available_letters = get_available_letters(letters)

    print('Welcome to the game Hangman!')
    print('I''m thinking of a word that is '+str(len(secret_word))+ ' letters long')
    print('You have ' + str(warnings) + ' warnings letf.')


    while True:
        guesses = 0
        print('\nyou have ' + str(num_guesses-guesses) + ' guesses left.')
        print('Available leters: ', available_letters)
        letter = input('Please guess a letter: ')

 
        # converts the input letter to lower case
        if letter.isupper():
            letter = str.lower(letter)
                
       # This is a penalization in case letter in nos alphabet
        if not letter.isalpha():
            if warnings >= 1:
                warnings -= 1
                print('\nYou have' + str(warnings) + 'warnings left.')
            
            else :
                guesses += 1
                print('\nYou have' + str(num_guesses-guesses) + 'guesses left') 
                       
            letter = input('Please enter only alphabet: ')
       
        # This is a penalization in case user says an already guessed letter  
        if letter in list_letters_guesed:
            if warnings >= 1:
                warnings -= 1
                print('Oops! You''ve already guessed that letter. You have '
                      + str(warnings) + ' warnings left.')
            
            else :
                guesses += 1
                print('\nYou have' + str(num_guesses-guesses) + 'guesses left') 
                       
            letter = input('Please enter only alphabet: ')
         
        list_letters_guesed.append(letter)
        letters = ''.join(list_letters_guesed)
        available_letters = get_available_letters(letters)

###################### Let's play:    
        if letter in secret_word:
            guessed_word = get_guessed_word( secret_word, list_letters_guesed)
            print('\nGood guess: ', guessed_word)

           
        else:
            if is_vowel(letter) :
                guessed_word = get_guessed_word( secret_word, list_letters_guesed)
                guesses += 2
                print('\nOops! that letter is not in may word: ', guessed_word)
            else:
                guessed_word = get_guessed_word( secret_word, list_letters_guesed)
                guesses += 1
                print('\nOops! that letter is not in may word: ', guessed_word)
                


        if is_word_guessed(secret_word,list_letters_guesed) or guesses  >=num_guesses:
            break
        
        
        
    
    if  is_word_guessed(secret_word,list_letters_guesed):
        print('\nCongratulations you won!. \nTotal score is:' +\
              str((num_guesses-guesses)*len_uniq_secret_word) )
    else :
        print('\nSorry, you run out of guesses. Secret word is: ', secret_word)
                    
        
    
if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    hangman(secret_word)

    
    
    
    
    
    
    
    
    
    