#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 17:00:16 2020

Hangman game with hints.

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

wordlist = load_words()   


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

def match_with_gaps( my_word, other_word):
    """
    

    Parameters
    ----------
    my_word : string
       guessed letters of the word in the game of Hangman
    other_word : string
        a complete word

    Returns
    -------
    True if the corresponding letters in my_word match letters in other_word
    False if the two words are not the same lenght or if a guessed letter in my_word
    does not match the corresponding character in other_word.
    """
    # removes all blank spaces and tells the real length of the word to be guessed
    my_word_blank = my_word.replace(' ','') 
    # removes underscores 
    my_word_under = my_word_blank.replace('_','') # no spaces no underscores
    
    if len(my_word_blank) == len(other_word):
       for char1, char2 in zip(my_word_blank,other_word):
           if (char1 != '_' and char1 != char2) or (char1 == '_' and char2 in my_word_under):
               return False
       return True
 
    else:
        return False
  
def show_possible_matches( my_word ):
    """
    

    Parameters
    ----------
    my_word : string.
        It's an instance of a guessed word (it could contain _ in it) in the game
        Hangman

    Returns
    -------
    Prints out all the words in wordlist that match my_word

    """
    matched_words = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matched_words.append(word)
    if not matched_words:
        print('no matches found')
    else:
        #print(matched_words) # si le doy la opcion de imprimir, cuando la llame
        # va a imprimir lo pedido
        return matched_words # si le doy la opcion de return, cuando la llame 
    #tengo que especificar que imprima lo que devuelve la funcion

#secret_word = choose_word(wordlist)
def hangman_with_hints( secret_word ):
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
    guesses = 0
    letters = ''
    list_letters_guesed = []
    available_letters = get_available_letters(letters)

    print('Welcome to the game Hangman!')
    print('I''m thinking of a word that is '+str(len(secret_word))+ ' letters long')
    print('You have ' + str(warnings) + ' warnings letf.')


    while True:
        print('\nyou have ' + str(num_guesses-guesses) + ' guesses left.')
        print('Available leters: ', available_letters)
        letter = input('Please guess a letter: ')

 
        # converts the input letter to lower case
        if letter.isupper():
            letter = str.lower(letter)
        

       # This is a penalization in case letter in nos alphabet
        if not letter.isalpha():
            if letter == '*':
                print(show_possible_matches(guessed_word))
                letter = input('Please guess a letter: ')

            elif warnings >= 1:
                warnings -= 1
                print('\nYou have' + str(warnings) + 'warnings left.')
                letter = input('Please enter only alphabet: ')

            
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
#     # pass

#     # To test part 2, comment out the pass line above and
#     # uncomment the following two lines.
    
#     # secret_word = choose_word(wordlist)
#     # hangman(secret_word)

# ###############
    
#     # To test part 3 re-comment out the above lines and 
#     # uncomment the following two lines. 
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
     
