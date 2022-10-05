# Problem Set 4C
# Name: Jordan Gallivan

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text=text
        self.word_list=load_words("words.txt")
        
        text_words=list(self.message_text)
        self.valid_words=[]
        
        for j in range(len(text_words)):
            if is_word(self.word_list, text_words[j])==True:
                self.valid_words.append(text_words[j])
            
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        self.vowels_permutation= vowels_permutation
        self.transpose_dict={}
        # VOWELS_LOWER = 'aeiou'
        # VOWELS_UPPER = 'AEIOU'
        # CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
        # CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'
        
        for i in range(len(VOWELS_LOWER)):  #add vowels to dictionary
            self.transpose_dict[VOWELS_LOWER[i]]=str.lower(self.vowels_permutation[i])
            self.transpose_dict[VOWELS_UPPER[i]]=str.upper(self.vowels_permutation[i])
        
        for j in range(len(CONSONANTS_LOWER)):
            self.transpose_dict[CONSONANTS_LOWER[j]]=CONSONANTS_LOWER[j]
            self.transpose_dict[CONSONANTS_UPPER[j]]=CONSONANTS_UPPER[j]
        
        return self.transpose_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        self.transpose_dict=transpose_dict
        self.message_text_encrypted=''

        # iterate through len of message text
        for n in range(len(self.message_text)): 
            # O nly apply dictionary to letters
            if str.isalpha(self.message_text[n])==True:     
                self.message_text_encrypted += self.transpose_dict[self.message_text[n]]    # Encrypt at n = dict value of message letter
            else:
                self.message_text_encrypted += self.message_text[n]
        
        return self.message_text_encrypted 
        
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        SubMessage.__init__(self, text)
        
        
    # def get_permutations(self,sequence):
    #     '''
    #     Enumerate all permutations of a given string

    #     sequence (string): an arbitrary string to permute. Assume that it is a
    #     non-empty string.  
    #     '''
    #     self.perms=[]
    #     self.sequence=sequence
        
    #     if len(self.sequence)== 1:      #base case
    #         self.perms.append(self.sequence)
        
    #     else:
    #         initial_letter=self.sequence[0]
    #         temp_perms = self.get_permutations(self.sequence[1:]) #temporary permutations after first letter
    #         for n in range(len(temp_perms)):  #iterate through temporary permuations
    #             for i in range(len(self.sequence)):  #iterate through each permutation
    #                 self.perms.append(temp_perms[n][0:i] + initial_letter + temp_perms[n][i:])
           
    #     return self.perms        
        
    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        permutations=get_permutations('aeiou')  # list of permutations
        # print(str(permutations))



        for pos, k in enumerate(permutations): # iterate through all permutations
            temp_valid_words=[]     # shell for the comparrison of total number of valid words
            
            transpose_dict=self.build_transpose_dict(k)     # build the transpose dictionary
            
            temp_encrypted=self.apply_transpose(transpose_dict) # apply the transpose dictionary
            temp_encrypted=temp_encrypted.split()   # convert the string into a list for testing valid words
            
            # if pos in [0,1,2,3,4]:
                # print(str(temp_encrypted))
            
            for l in temp_encrypted:
                if is_word(self.word_list, l) == True:
                    temp_valid_words.append(l)

            if pos == 0:        # establish a base case
                best_valid=temp_valid_words
                best_permutation=k
                best_case=temp_encrypted
            else:
                if len(temp_valid_words)>len(best_valid):
                    best_valid=temp_valid_words
                    best_permutation=k
                    best_case=temp_encrypted
                    # print(best_case)
        
        return best_permutation, ' '.join(best_case)
                    
                
            
        
    

if __name__ == '__main__':
    text = 'Do you, have the Time? To listen to me whine. About nothing'
    # Example test case
    message = SubMessage(text)
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
