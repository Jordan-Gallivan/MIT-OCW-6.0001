# Problem Set 4A
# Name: Jordan Gallivan

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    perms=[]
    
    if len(sequence)== 1:
        perms.append(sequence)
    
    else:
        initial_letter=sequence[0]
        temp_perms = get_permutations(sequence[1:]) # temporary permutations after first letter
        
        # iterate through temporary permuations
        for n in range(len(temp_perms)):  
            # iterate through each permutation
            for i in range(len(sequence)):  
                perms.append(temp_perms[n][0:i] + initial_letter + temp_perms[n][i:])
       
    return perms


if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'aeiou'
    print('Input:', example_input)
    # print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here

