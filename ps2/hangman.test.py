import hangman as hg
import string

if __name__ == '__main__':
    # is_word_guessed testing
    assert hg.is_word_guessed('apple', ['a', 'p', 'p', 'l', 'e'])
    assert hg.is_word_guessed('', ['a', 'p', 'p', 'l', 'e'])
    assert hg.is_word_guessed('', [])
    assert not hg.is_word_guessed('apple', [])
    assert not hg.is_word_guessed('apple',
            ['a', 'p', 'l', 'e', 'f', 'z', 'c'])
    # get_guessed_word
    assert hg.get_guessed_word('apple', ['a', 'p', 'p', 'l', 'e']) \
        == 'apple'
    assert hg.get_guessed_word('', ['a', 'p', 'p', 'l', 'e']) \
        == ''
    assert hg.get_guessed_word('', []) \
        == ''
    assert hg.get_guessed_word('apple', []) \
        == '_____'
    assert hg.get_guessed_word('apple',
            ['a', 'p', 'l', 'e', 'f', 'z', 'c']) \
        == 'ap_le'
    # get_avaiable_letters
    assert hg.get_available_letters([]) == string.ascii_lowercase
    assert hg.get_available_letters(list(string.ascii_lowercase)) \
        == ''
    assert hg.get_available_letters(['e', 'i', 'k', 'p', 'r', 's'])  \
        == 'abcdfghjlmnoqtuvwxyz'

