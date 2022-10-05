# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Jordan Gallivan


import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
   
    word_len=len(word)
    
    # if empty string, score is 0
    if word_len==0:     
        return 0
    if ' ' in word:
        print('two words.  Please enter one word at a time')
        return 0
    
    comp1=0
    word=list(word)
    
    # get the first portion of the score product
    for i in word:      
        comp1 += SCRABBLE_LETTER_VALUES[str.lower(i)]
    
    # get second portion of score product - if <1, reset value back to 1
    comp2=(7*word_len)-(3*(n-word_len))
    if comp2<1:
        comp2=1
    
    return(comp1*comp2)

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    print('Current Hand:',end=' ')
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    hand['*']=1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    word=list(word)
    new_hand=hand.copy()
    
    
    for n in word:
        new_hand[str.lower(n)] = new_hand.get(str.lower(n),0) - 1
    
    key_copy=new_hand.copy()
    keys = key_copy.keys()
    
    for i in keys:
        if new_hand[i]<1:
            del(new_hand[i])
    
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    word=list(word)
    
    # set all letters to lowercase
    for pos, letter in enumerate(word): #lower the case of word
        word[pos]=str.lower(letter)
    
    # wildcard
    if '*' in word:
        wild_card_loc=word.index('*')
        vowel_list=[]
        
        # iterate through vowels to verify valid use of wildcard
        for k in list(VOWELS):
            word[wild_card_loc]=k
            if ''.join(word) not in word_list:
                vowel_list.append(False)
            else:
                vowel_list.append(True)
        if True not in vowel_list:
            return False
        word[wild_card_loc]='*'
        
    else:
        if ''.join(word) not in word_list:
            return False
            
    new_hand=hand.copy()    # copy list to avoid mutation
    
    for n in word:
        new_hand[n]=new_hand.get(n,0) - 1
    
    key_copy=new_hand.copy()
    keys = key_copy.keys()
    
    for i in keys:
        if new_hand[i]<0:          
            return False

    return True  

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    hand_keys=hand.keys()
    handlen=0
    for n in hand_keys:
        handlen += hand[n]
    
    return handlen



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
    
    
    total_score=0
    
    # iterate through until all cards played or user enters "!!"
    while calculate_handlen(hand)>0:
    
        display_hand(hand)  # show user their current hand
        word=input(str('Enter word, or "!!" to indicate that you are finished: '))
        
        #score hand        
        if word == '!!':
            break   #end game
            
        else:
            # verify valid word
            if is_valid_word(word, hand, word_list) == True:
                # update scorea and display score
                score=get_word_score(word, calculate_handlen(hand))
                print('"', word, '"', 'earned', str(score), 'points.', end=' ')
                total_score += score
                print('Total:',str(total_score), 'points')

            else:
                print('That is not a valid word. Please choose another word.')
            
            hand=update_hand(hand, word)    # update user hand
      
    # player ended game or ran out of letters   
    if word=='!!':
        print('Total score:', str(total_score))
    else:
        print('Ran out of letters. Total score:', str(total_score))

    return total_score


#
# Problem #6: Playing a game
# 

#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # set all letters to lowercase, initialize variables
    letter=letter.lower()
    substitute_hand=hand.copy()
    old_letters=hand.keys()
    
    # only updates hand if letter chosen is in original hand
    if letter not in old_letters:
        return hand
    
    num_old_letter=hand[letter]     # number of letters to maintain
    
    del(substitute_hand[letter])    # delete the chosen letter
    
    # vowel replacement
    if letter in VOWELS:
        new_letter=random.choice(VOWELS)
        while new_letter in old_letters:
            new_letter=random.choice(VOWELS)
    # consonant replacement
    else:
        new_letter=random.choice(CONSONANTS)
        while new_letter in old_letters:
            new_letter=random.choice(CONSONANTS)
    
    substitute_hand[new_letter]=substitute_hand.get(new_letter,num_old_letter)
    
    return substitute_hand
    
# hand={'a':1, 'j':1, 'e':1, 'f':1, '*':1, 'r':1, 'x':1}
# print(str(hand))
# word_list=load_words()  
# letter=str(input('letter: '))

# print(str(substitute_hand(hand, letter)))
     
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

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
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    replays=1
    num_subs=1
    num_hands=int(input('Enter total number of hands: '))
    num_letters_in_hand=7
    hand = deal_hand(num_letters_in_hand)
    total_score=0
    
    for i in range(num_hands):
        
        display_hand(hand)
        
        if num_subs>0: 
            sub_hand=str(input('Would you like to substitute a letter? '))
            if str.lower(sub_hand) == 'yes':
                letter=str(input('Which letter would you like to replace: '))
                hand = substitute_hand(hand, letter)
                num_subs=0
      
        hand_score = play_hand(hand, word_list)
        print('----------')
        
        if replays>0:
            replay_val=str(input('Would you like to replay the hand? '))
            if str.lower(replay_val) == 'yes':
                replay_score=play_hand(hand, word_list)
                if replay_score > hand_score:
                    hand_score=replay_score
                    print('----------')
                replays=0
        
        total_score += hand_score
        print('Total score for this hand:', hand_score)
        hand = deal_hand(num_letters_in_hand)
        
        
        
    print('Total score over all hands:', str(total_score))
    
    return
                
play_game(load_words())
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
