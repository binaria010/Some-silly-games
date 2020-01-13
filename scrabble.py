#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:48:50 2020

Word Game:
This game is a lot like Scrabble or Words With Friends. Letters are dealt to 
players, who then construct one or more words using their letters.
Each ​valid​ word earns the user points, based on the length of the word and the
letters in that word.


@author: Juliana
"""


import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 
    'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 
    'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


def load_words():
    """
    

    Returns
    -------
    A list of all the words for the game Word Game

    """
    print("Loading word list from file...")
    in_File = open('words.txt','r')
    wordlist = []
    for line in in_File:
        wordlist.append(line.strip().lower())
    
    print(" ",len(wordlist),'words loaded')
    
    return wordlist

def get_frequency_dict(s):
    """
    Parameters
    ----------
    s : string

    Returns
    A dictionary with keys the letters in string s and values are the number of times
    that letter is represented in the input string.    """
    
    freq = {}
    for letter in s:
        freq[letter] = freq.get(letter,0) + 1
    
    return freq


def get_word_score ( word, n ):
    """
    Parameters
    ----------
    word : string. A word formed with letters provided in the hand.
    n : int>=0. The number of letters in the hand
    Returns: int >=0
    The score of the word computed as a product of two factors. 
    First factor is the sum of the points of the letters according to their values
    given in SCRABBLE_LETTER_VALUES dict.
    Second factor is the max between (7*len(word) - 3*(n-len(word))) and 1.

    """
    word = word.lower()
    factor1 = sum(SCRABBLE_LETTER_VALUES[letter] for letter in word)
    factor2 = max(7*len(word) - 3*(n- len(word)),1)
    
    return factor1*factor2

def display_hand( hand ):
    """
    Parameters
    ----------
    hand : dict(string -> int). The dealt hand represented as a dict

    Returns: None
    Displays the letters currently in the hand.
    
    Example: 
    display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    """
    
    for letter in hand.keys():
        for i in range(hand[letter]):
            print(letter, end=' ') # prints the letter with a space in between
    print()   # prints an empy line why?
    
    
def deal_hand( n ):
    """
    Parameters
    ----------
    n : int. The number of leeters delivered in the hand
    Returns
    -------
    A dict with the n letters as keys and values the number of times each letter 
    appears.
    Condition on the hand:
    ceil(n/3) letters in the hand should be VOWELS 
    """
   
    VOWELS = 'aeiou'
    CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
    hand = {}
    
    # gnenerate ceil(n/3) random vowels
    for i in range(math.ceil(n/3)-1):
        vowel = random.choice(VOWELS)
        hand[vowel] = hand.get(vowel, 0) + 1
            
    hand['*'] = 1 # add always a wildcard
    # generate the rest of the letters to be consonants:
    for i in range(math.ceil(n/3),n):
        cons = random.choice(CONSONANTS)
        hand[cons] = hand.get(cons,0) + 1
    
    return hand

def update_hand(hand, word):
    """
    hand : dict(string->int) the given hand
    word : string. The word formed with letters from hand

    Returns
    A new hand with letters left in hand after building te word word. Do not
    modify the dict hand.
    """
    
    # We could have used fnc get_frequency_dict to update hand
    word = word.lower()
    new_hand = hand.copy()
    for key in hand.keys():
        if key in word:
            new_hand[key] = hand[key] - word.count(key)

    # this piece of code removes entries with negative or zeor values 
    new_Hand = {}
    for char in new_hand.keys():
          if new_hand[char] > 0:
              new_Hand[char] = new_hand[char]
            
    return new_Hand


def letters_in_hand(word, hand)  :
    """
    word : string. Assmued lower case
    hand : Dict (string -> int)

    Returns True if each letter in word is in the dict hand, otherwise False.
    """  
    # We could have used fnc get_frequency_dict to implement this funciton
        
    for char in word:
        if word.count(char) > hand.get(char,0):
            return False
    return True
    
    





def is_valid_word(word, hand, word_list):
    """
    Parameters
    ----------
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    
    Returns: True if word is in word_list and it's entirely composed of letters
    (including *) in the hand. Otherwise, returns False. 
    Does not mutate hand or word_list
    -------
    boolean
    """
    
    word = word.lower()
    wild_idx = word.find('*') # index position for the wildcard * in word
    WORD = list(word)
    
    if wild_idx  <=-1: # if true, word does not contain the wildcard
        if word in word_list : # checks if in word_list
            return letters_in_hand(word, hand) # True if it uses only letters in hand
                
    else:
        for vowel in VOWELS:
            WORD[wild_idx] = vowel
            if ''.join(WORD) in word_list:
                return letters_in_hand(word,hand)
        return False
            
        
# Playing a hand
        
def calculate_handlen(hand):
    """
    Parameters
    ----------
    hand : dict(string -> int)

    Returns: int. The number of letters in the hand
    """
    return sum(hand[key] for key in hand.keys())


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    n =  calculate_handlen(hand)
    print('Current Hand:', end = ' ')
    display_hand(hand)
    
    word = input('Enter word, or "!!" to indicate that ypu are finished: ')
    total_score = 0
    
    while True:
        if word == "!!":
            print('Total score: ' + str(total_score) + ' points')
            #return total_score
            break
    
        else :
            if is_valid_word(word,hand,word_list):
                total_score += get_word_score(word, n)
                print(word, 'earned " ' + str(get_word_score(word, n))+  ' " points. ',
                      'Total: ' + str(total_score))
                if not update_hand(hand, word):
                    print('Run out of letters. Total score: ' + str(total_score) + 
                          ' points')
                    break
                print('Current Hand:', end = ' ') 
                hand = update_hand(hand,word)
                display_hand(hand)
                n = calculate_handlen(hand)


 

            else :
                print('That is not a valid word. Please choose another word: ')
                if not update_hand(hand, word):
                    print('Run out of letters. Total score: ' + str(total_score) + 
                          ' points')
                    break
                print('Currend Hand:', end=' ')
                hand = update_hand(hand, word)
                display_hand(hand)
                n = calculate_handlen(hand)


                
            word = input('Enter word, or "!!" to indicate that ypu are finished: ')
            
    return total_score      

    # Playing a game
            
def substitute_hand(hand,letter):
    """
    This function allows the user to replace all copies of a letter (chosen by the user)
    in hand with a new letter chosen randomly from the constants VOWELS and CONSONANTS.
    The new letter should be different from user's choice and it should not be any of
    the letters already in the hand.
    
    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    Parameters
    ----------
    hand : dict(str -> int). The dealt hand
    letter : string. A letter to be replaced in hand

    Returns
    -------
    new_hand: dictionary(str ->int)
    """
    
    new_hand = hand.copy()
    letter.lower()
    if letter not in hand.keys():
        return hand
    
    
    letter_value = hand[letter]
    del new_hand[letter]
    
    while True:
        new_letter = random.choice(VOWELS+CONSONANTS)
        if new_letter not in hand.keys():
            new_hand[new_letter] = letter_value
            return new_hand

            break
    

def play_game(word_list):
    """
    Allows the user to play a series of hands.
    
    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    Parameters
    word_list : list. The list of admissible words

    Returns: int. The total score of the series of hands
    """
    
    n = int(input('Enter total number of hands: '))
    replays = 0
    replace = 0
    Total_score = 0
    hand = deal_hand(HAND_SIZE)
    print('Current Hand:', end=' ')
    display_hand(hand)


    for h in range(n):
        
        if replace>=0:
            substitute = input('Would you like to substitute a letter? ')
            if substitute == 'yes':
                replace -= 1
                print(replace)
                letter = input('Which letter would you like to replace: ')
                new_hand = substitute_hand(hand, letter)
                total_score_hand = play_hand(new_hand, word_list)
                if replays>=0:
                    replay = input('Would you like to replay hand? ')
                    if replay == 'yes':
                        replays -= 1
                        total_score_hand = play_hand(new_hand, word_list)
                print('Total score for this hand: ', total_score_hand)


            else :
                total_score_hand = play_hand(hand, word_list)
                if replays>=0:
                    replay = input('Would you like to replay hand? ')
                    if replay == 'yes':
                        replays -= 1
                        total_score_hand = play_hand(new_hand, word_list)

                print('Total score for this hand: ', total_score_hand)
                
        else : 
            new_hand = substitute_hand(hand, letter)
            total_score_hand = play_hand(new_hand, word_list)
            if replays>=0:
                replay = input('Would you like to replay hand? ')
                if replay == 'yes':
                    replays -= 1
                    total_score_hand = play_hand(new_hand, word_list)
            print('Total score for this hand: ', total_score_hand)

        
            
        Total_score += total_score_hand 
        
    print('Total score over all hands: ', Total_score)    
    return Total_score

    
## Testing some functions
    

def test_get_word_score():
    """
    Unit test for get_word_score
    """
    failure=False
    # dictionary of words and scores
    words = {("", 7):0, ("it", 7):2, ("was", 7):54, ("weed", 6):176,
             ("scored", 7):351, ("WaYbILl", 7):735, ("Outgnaw", 7):539,
             ("fork", 7):209, ("FORK", 4):308}
    for (word, n) in words.keys():
        score = get_word_score(word, n)
        if score != words[(word, n)]:
            print("FAILURE: test_get_word_score()")
            print("\tExpected", words[(word, n)], "points but got '" + \
                  str(score) + "' for word '" + word + "', n=" + str(n))
            failure=True
    if not failure:
        print("SUCCESS: test_get_word_score()")

# end of test_get_word_score


def test_update_hand():
    """
    Unit test for update_hand
    """
    # test 1
    handOrig = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
    handCopy = handOrig.copy()
    word = "quail"

    hand2 = update_hand(handCopy, word)
    expected_hand1 = {'l':1, 'm':1}
    expected_hand2 = {'a':0, 'q':0, 'l':1, 'm':1, 'u':0, 'i':0}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tReturned: ", hand2, "\n\t-- but expected:", expected_hand1, "or", expected_hand2)

        return # exit function
    if handCopy != handOrig:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tOriginal hand was", handOrig)
        print("\tbut implementation of update_hand mutated the original hand!")
        print("\tNow the hand looks like this:", handCopy)
        
        return # exit function
        
    # test 2
    handOrig = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    handCopy = handOrig.copy()
    word = "Evil"

    hand2 = update_hand(handCopy, word)
    expected_hand1 = {'v':1, 'n':1, 'l':1}
    expected_hand2 = {'e':0, 'v':1, 'n':1, 'i':0, 'l':1}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")        
        print("\tReturned: ", hand2, "\n\t-- but expected:", expected_hand1, "or", expected_hand2)

        return # exit function

    if handCopy != handOrig:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tOriginal hand was", handOrig)
        print("\tbut implementation of update_hand mutated the original hand!")
        print("\tNow the hand looks like this:", handCopy)
        
        return # exit function

    # test 3
    handOrig = {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    handCopy = handOrig.copy()
    word = "HELLO"

    hand2 = update_hand(handCopy, word)
    expected_hand1 = {}
    expected_hand2 = {'h': 0, 'e': 0, 'l': 0, 'o': 0}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")                
        print("\tReturned: ", hand2, "\n\t-- but expected:", expected_hand1, "or", expected_hand2)
        
        return # exit function

    if handCopy != handOrig:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tOriginal hand was", handOrig)
        print("\tbut implementation of update_hand mutated the original hand!")
        print("\tNow the hand looks like this:", handCopy)
        
        return # exit function

    print("SUCCESS: test_update_hand()")

# end of test_update_hand

def test_is_valid_word(word_list):
    """
    Unit test for is_valid_word
    """
    failure=False
    # test 1
    word = "hello"
    handOrig = get_frequency_dict(word)
    handCopy = handOrig.copy()

    if not is_valid_word(word, handCopy, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected True, but got False for word: '" + word + "' and hand:", handOrig)

        failure = True

    # Test a second time to see if word_list or hand has been modified
    if not is_valid_word(word, handCopy, word_list):
        print("FAILURE: test_is_valid_word()")

        if handCopy != handOrig:
            print("\tTesting word", word, "for a second time - be sure you're not modifying hand.")
            print("\tAt this point, hand ought to be", handOrig, "but it is", handCopy)

        else:
            print("\tTesting word", word, "for a second time - have you modified word_list?")
            wordInWL = word in word_list
            print("The word", word, "should be in word_list - is it?", wordInWL)

        print("\tExpected True, but got False for word: '" + word + "' and hand:", handCopy)

        failure = True


    # test 2
    hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u':1}
    word = "Rapture"

    if  is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)

        failure = True        

    # test 3
    hand = {'n': 1, 'h': 1, 'o': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "honey"

    if  not is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected True, but got False for word: '"+ word +"' and hand:", hand)

        failure = True                        

    # test 4
    hand = {'r': 1, 'a': 3, 'p': 2, 't': 1, 'u':2}
    word = "honey"

    if  is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        
        failure = True

    # test 5
    hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    word = "EVIL"
    
    if  not is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected True, but got False for word: '" + word + "' and hand:", hand)
        
        failure = True
        
    # test 6
    word = "Even"

    if  is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        print("\t(If this is the only failure, make sure is_valid_word() isn't mutating its inputs)")        
        
        failure = True        

    if not failure:
        print("SUCCESS: test_is_valid_word()")

# end of test_is_valid_word

def test_wildcard(word_list):
    """
    Unit test for is_valid_word
    """
    failure=False

    # test 1
    hand = {'a': 1, 'r': 1, 'e': 1, 'j': 2, 'm': 1, '*': 1}
    word = "e*m"

    if is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)

        failure = True

    # test 2
    hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "honey"

    if is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected False, but got True for word: '"+ word +"' and hand:", hand)

        failure = True

    # test 3
    hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "h*ney"

    if not is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected True, but got False for word: '"+ word +"' and hand:", hand)

        failure = True

    # test 4
    hand = {'c': 1, 'o': 1, '*': 1, 'w': 1, 's':1, 'z':1, 'y': 2}
    word = "c*wz"

    if is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected False, but got True for word: '"+ word +"' and hand:", hand)

        failure = True    

    # dictionary of words and scores WITH wildcards
    words = {("h*ney", 7):290, ("c*ws", 6):176, ("wa*ls", 7):203}
    for (word, n) in words.keys():
        score = get_word_score(word, n)
        if score != words[(word, n)]:
            print("FAILURE: test_get_word_score() with wildcards")
            print("\tExpected", words[(word, n)], "points but got '" + \
                  str(score) + "' for word '" + word + "', n=" + str(n))
            failure=True      

    if not failure:
        print("SUCCESS: test_wildcard()")


word_list = load_words()
print("----------------------------------------------------------------------")
print("Testing get_word_score...")
test_get_word_score()
print("----------------------------------------------------------------------")
print("Testing update_hand...")
test_update_hand()
print("----------------------------------------------------------------------")
print("Testing is_valid_word...")
test_is_valid_word(word_list)
print("----------------------------------------------------------------------")
print("Testing wildcards...")
test_wildcard(word_list)
print("All done!")

    