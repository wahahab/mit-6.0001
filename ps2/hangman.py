# Problem Set 2, hangman.py
# Name: 
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

from collections import Counter

WORDLIST_FILENAME = "words.txt"

def test():
    print 'foobarfootest'

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
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return len(set(secret_word) & set(letters_guessed)) == len(set(secret_word))

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    out_string = ''
    guessed_letters = set(letters_guessed)
    for l in secret_word:
        if l in guessed_letters:
            out_string += l
        else:
            out_string += '_'
    return out_string

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    guessed_set = set(letters_guessed)
    return ''.join([l for l in list(string.ascii_lowercase)
        if l not in guessed_set])
    
def hangman(secret_word, hint=False):
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
    guesses_left = 6
    warning_left = 3
    letters_guessed = []
    print 'Welcome to the game Hangman!'
    #secret_word = 'tact'
    secret_word_letters = set(secret_word)
    print 'I am thinking of a word that is %s letters long.' % len(secret_word)
    while guesses_left > 0 and not is_word_guessed(secret_word, letters_guessed):
        use_warning = False
        available_letters = get_available_letters(letters_guessed)
        print '-------------'
        print 'You have %s guesses left.' % guesses_left
        print 'Available letters: %s' % available_letters
        input_letter = raw_input('Please guess a letter:')
        if hint and input_letter == '*':
            print 'Possible word matches are:'
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        if not (len(input_letter) == 1 and input_letter in string.ascii_lowercase):
            use_warning = True  
        else:
            use_warning = input_letter in letters_guessed
        if use_warning:
            if warning_left > 0:
                warning_left -= 1
                print 'Oops! You\'ve already guessed that letter. You have %s warnings left:' % warning_left
            else:
                guesses_left -= 1
            continue
        letters_guessed.append(input_letter)
        if input_letter in secret_word_letters:
            message = 'Good guess: %s'
        else:
            message = 'Oops! That letter is not in my word: %s'
            guesses_left -= 1
        print message % get_guessed_word(secret_word, letters_guessed)
    if is_word_guessed(secret_word, letters_guessed):
        print 'Congratulations! You win!!!'
        return
    print '-----------'
    print 'Sorry, you ran out of guesses. The word was %s.' % secret_word

        
        
        



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.strip()
    other_word = other_word.strip()
    if len(my_word) != len(other_word):
        return False
    for i, l in enumerate(my_word):
        if l == '_':
            continue
        if other_word[i] != l:
            return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matched_words = []
    for w in wordlist:
        if match_with_gaps(my_word, w):
            matched_words.append(w)
    print ' '.join(matched_words)


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
    hangman(secret_word, True)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    # hangman(secret_word)
    hangman_with_hints(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
