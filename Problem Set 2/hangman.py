# Problem Set 2, hangman.py
# Name: Jordan Gallivan
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
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

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word = list(secret_word)     # convert secret word to a string
    secret_clone=secret_word[:]         # clone secret word for iteration
    for n in secret_clone:
        if n in letters_guessed:
            secret_word.remove(n)       # remove letters guessed from secret word
    return len(secret_word)==0          # no letters left = word guessed


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: (string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.)
      & (If last guess was a miss.  True if Miss, False if correct guess)
    '''
    secret_word = list(secret_word)     # convert secret word to a string
    secret_clone=secret_word[:]         # clone secret word for iteration
    
    # iterate through secret clone with pos=position in the list
    for pos, value in enumerate(secret_clone):  
        if value not in letters_guessed:        
            secret_word[pos]='_ '   # replace missed letters with _
    # test if letter guessed not in word
    if len(letters_guessed)>0 and (letters_guessed[-1] not in secret_clone):    
        misguess=True
    else:
        misguess=False
    return(''.join(secret_word),misguess)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alpha=string.ascii_lowercase
    alpha=list(alpha)
    letters_clone=letters_guessed[:]
    for letter in letters_clone:
        alpha.remove(letter)
    return ''.join(alpha)

def already_guessed(letters_guessed):
    '''
    Input is letters guessed.  Evaluates the letters guessed to determine if 
    inputted letter has been guessed
    return: been guessed, boolean.  True if letter has been previously guessed

    '''
    
    if len(letters_guessed)!=1 and (letters_guessed[-1] in letters_guessed[0:(len(letters_guessed)-1)]):
        been_guessed=True
    else:
        been_guessed=False
    
    return been_guessed    
    
def warn_func(num_miss,num_warn,type_warn):
    '''
    inputs are the number of misses, the number of warnings remaining AFTER it has been decremented, and the type of warning
    return is a Tuple with remaining number of misses and warnings

    '''
    warnings=['\n Your input was not a letter.','\n You have already guessed that letter.']
    if num_warn>0:
        print(warnings[type_warn], 'You have:', str(num_warn), 'warnings remaining')
    else:
        num_warn=3
        num_miss+=1
        print(warnings[type_warn],'You have used all 3 warnings, and therefore lose a guess.', 'You have:', str(num_warn), 'warnings remaining')
    
    return(num_miss,num_warn)

def cons_or_vowel(letters_guessed,num_miss):
    vowels=['a','e','i','o','u']
    if letters_guessed[-1] in vowels:
        num_miss+=2
    else:
        num_miss+=1
    return(num_miss)

def letter_count(secret_word):
    '''
    Takes the secret_word and counts unique letters
    by deleting the evaluated letter and checking if that letter is in the word still
    '''
    
    secret_word=list(secret_word)
    num_letters=0
    while len(secret_word)>0:       
        num_letters+=1
        eval_letter=secret_word[0]
        del(secret_word[0])
        while eval_letter in secret_word:
            secret_word.remove(eval_letter)
    
    return num_letters

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
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
    '''
    letters_guessed=[]
    num_miss = 0
    num_guess=0
    num_warn=3
    type_warn=0 # 0=input not a letter; 1=input was already guessed
    blanks=get_guessed_word(secret_word, letters_guessed)   # convert secret word to _'s

    num_letters=letter_count(secret_word)

    print(blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
    print('\n You can guess one of the following letters:', get_available_letters(letters_guessed))
    
    while num_miss <6:
        letters_guessed.append(input('Please guess a letter: '))    
        num_guess+=1
        str.lower(letters_guessed[-1])
        
        # testing if a letter
        if str.isalpha(letters_guessed[-1])==False:         
            num_warn-=1
            del(letters_guessed[-1])
            type_warn=0
            (num_miss,num_warn)=warn_func(num_miss,num_warn,type_warn)  # runs the warning function for Not a Letter Input
            print(blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
        
        # input was a letter
        elif already_guessed(letters_guessed)==True:        
            num_warn-=1
            del(letters_guessed[-1])
            type_warn=1
            (num_miss,num_warn)=warn_func(num_miss,num_warn,type_warn)  # runs the warning function for Not a Letter Input        
            print(blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
        
        else:
            if is_word_guessed(secret_word, letters_guessed)==False:
                blanks=get_guessed_word(secret_word, letters_guessed)
                if blanks[1] == True:
                    num_miss = cons_or_vowel(letters_guessed, num_miss)
                    if num_miss>=6:
                        break
                    else:
                        print('\n oops, that letter is not in the word. \n ', blanks[0],'you have',str(6-num_miss), 'guesses remaining.')
                else:
                    print('\n Nice job!: \n ',blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
            else:
                print('\n Congratulations! You correctly guessed the word:', secret_word, 'in',str(num_guess),'guesses')
                print('Your total score for this game is:', str(num_letters*(6-num_miss)),'points')
                break
        
        print('You can guess one of the following letters:',get_available_letters(letters_guessed))
        
        
    if num_miss>=6:
        print("\n I'm sorry, you've run out of guesses.  The correct word was:", secret_word)

    

wordlist = load_words()
# secret_word=choose_word(wordlist)

# # hangman(secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

def remove_spaces(my_word):
    my_word_clone=list(my_word)
    my_word_length=0
    pos_=[]
    while len(my_word_clone)>0:
        my_word_length+=1
        if my_word_clone[0]=='_':
            del(my_word_clone[0:2])
            pos_=pos_+[my_word_length-1]
        else:
            del(my_word_clone[0])
    word_no_space=list(my_word)
    for n in pos_:
        del(word_no_space[n+1])
    
    return ''.join(word_no_space)

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
############### need to check ALL the letters
    word_no_space=remove_spaces(my_word)
    guess=True
    
    if len(word_no_space) != len(other_word):
        guess=False
    else:
        for pos, val in enumerate(word_no_space):
            if val=='_':
                if other_word[pos] in word_no_space:
                    guess=False
                    break
            else:
                if other_word[pos] != val:
                    guess=False
                    break
        
    return guess


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    word_no_space=remove_spaces(my_word)
    answers=[]

    # find first letter
    for pos, i in enumerate(word_no_space):       
        if i != '_':
            pos_first_letter=pos
            break
    # find last letter    
    for lastpos, j in enumerate(word_no_space[::-1]):   
        if j != '_':
            pos_last_letter=len(word_no_space)-lastpos-1
            break
        
    for n in wordlist:
        if (len(n)==len(word_no_space)): 
            for i in range(pos_first_letter, (pos_last_letter+1)):
                if (word_no_space[i] != '_'):
                    if (word_no_space[i]!=n[i]):
                        break
                    elif (i==pos_last_letter) and (word_no_space[i]==n[i]):
                        answers.append(n)
            
    return answers



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed=[]
    num_miss = 0
    num_guess=0
    num_warn=3
    type_warn=0 # 0=input not a letter; 1 = input was already guessed
    blanks=get_guessed_word(secret_word, letters_guessed)   #c onvert secret word to _'s

    num_letters=letter_count(secret_word)

    print(blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
    print('\n You can guess one of the following letters:', get_available_letters(letters_guessed))
    
    while num_miss <6:
        letters_guessed.append(input('Please guess a letter: '))    
        if letters_guessed[-1]=='*':
            print('Possible word matches are:')
            print(' '.join(show_possible_matches(blanks[0])))
            letters_guessed.remove('*')
        else:
            num_guess+=1
            str.lower(letters_guessed[-1])
            
            # testing if a letter
            if str.isalpha(letters_guessed[-1])==False:         
                num_warn-=1
                del(letters_guessed[-1])
                type_warn=0
                (num_miss,num_warn)=warn_func(num_miss,num_warn,type_warn)  # runs the warning function for Not a Letter Input
                print(blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
            
            # input was a letter 
            elif already_guessed(letters_guessed)==True:       
                num_warn-=1
                del(letters_guessed[-1])
                type_warn=1
                (num_miss,num_warn)=warn_func(num_miss,num_warn,type_warn)  # runs the warning function for Not a Letter Input        
                print(blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
            else:
                if is_word_guessed(secret_word, letters_guessed)==False:
                    blanks=get_guessed_word(secret_word, letters_guessed)
                    if blanks[1] == True:
                        num_miss = cons_or_vowel(letters_guessed, num_miss)
                        if num_miss>=6:
                            break
                        else:
                            print('\n oops, that letter is not in the word. \n ', blanks[0],'you have',str(6-num_miss), 'guesses remaining.')
                    else:
                        print('\n Nice job!: \n ',blanks[0], 'you have' , str(6-num_miss), 'guesses remaining.')
                else:
                    print('\n Congratulations! You correctly guessed the word:', secret_word, 'in',str(num_guess),'guesses')
                    print('Your total score for this game is:', str(num_letters*(6-num_miss)),'points')
                    break
            
            print('You can guess one of the following letters:',get_available_letters(letters_guessed))
        
        
    if num_miss>=6:
        print("\n I'm sorry, you've run out of guesses.  The correct word was:", secret_word)
    return



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


#if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
secret_word = choose_word(wordlist)
hangman_with_hints(secret_word)
