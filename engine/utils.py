import string

comma_separator = (lambda x, y:  f"{x}, {y}")
newline_comma_separator = (lambda x, y: f"{x},\n\t{y}")
plus_separator = (lambda x, y: f"{x} + {y}")
newline_separator = (lambda x, y: f"{x}\n{y}")

class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

def my_format(**kwargs):
    formatter = string.Formatter()
    mapping = FormatDict(kwargs)
    return formatter.vformat(kwargs["s"], (), mapping)

strings = []
number_of_strings = -1

def top_level_split(s):
    """
    Split `s` by top-level commas only. Commas within parentheses are ignored.
    """
    
    # Parse the string tracking whether the current character is within
    # parentheses.
    balance = 0
    parts = []
    part = ""
    
    for i in range(len(s)):
        c = s[i]
        part += c
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
        elif c == ',' and balance == 0 and not s[i+1] == ',':
            part = part[:-1].strip()
            parts.append(part)
            part = ""
    
    # Capture last part
    if len(part):
        parts.append(part.strip())
    
    return parts

def unpack_by_chars(s, left, right):
    l = s.find(left)
    r = s.rfind(right)
    return s[l+1:r]