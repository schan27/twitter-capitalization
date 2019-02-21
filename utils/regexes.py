import re

# define regular expressions
lengthened_word_re = re.compile(r"""
    ^                   # string start
    [A-Za-z-]*          # 0 or more characters
    ([A-Za-z-])\1{1,}   # 2 or more of the same character
    [A-Za-z-]*          # 0 or more characters
    $                   # string end
    """, re.VERBOSE)

two_char_re = re.compile(r'([A-Za-z-])\1{1,}')  # sequence of 2 or more repeated
three_char_re = re.compile(r'([A-Za-z-])\1{2,}')
caps_seq_re = re.compile(r"([A-Z]{2,}(?:\s[A-Z-'0-9]{2,})*)")  # matches one or more consecutive capitalized words