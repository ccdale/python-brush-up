#!/usr/bin/env python3
""" password generator

Passwords generated from a word list with one added symbol
and one or more capitalised letter.

I found it increasingly difficult to type a system generated
password into a phone, so after a couple of iterations I came
up with this method:
    randomly pick 4 words from a word list

    pass it through the sha256 hashing function
    to generate 64 chars

    randomly pick 15 of those chars, ensure you
    have at least 2 letters

    capitalise 1 of the letters - ensure it cannot
    be mistaken for a numeral

    randomly add a symbol somewhere into the string

result is a 16 character string of mostly numbers and letters
with one symbol - the whole looks like line noise, but is
fairly easy to type into a phone.

output is in 4 character blocks which can be used as is
if the system accepts spaces in passwords or can be
concatenated if not.
"""
import hashlib
import random

# initialise the random number generator
random.seed()

def pwgen():

    # acceptable list of chars that can be capitalised
    capl = "acdefghjklmnpqrstuvwxyz"

    # list of acceptable symbols
    symbols = "=-!$%^&*(){}[]"

    # read the words into a list (note: each word will still have the
    # trailing newline)
    with open("wordlist.txt", "r") as wl:
        wlist = wl.readlines()

    # pick 4 random words from the list
    words = [word.rstrip() for word in random.choices(wlist, k=4)]

    # join the words into a phrase
    phrase = " ".join(words)

    # convert to bytes and hash into 64 chars.
    hphrase = hashlib.sha256(phrase.encode()).hexdigest()

    # pick 15 random characters from the hashed phrase
    ch = "".join(random.choices(hphrase, k=15))

    # pick a letter in the string to capitalise
    # filter out letters that are not in our acceptable list
    pos = [ch.index(c) for c in ch if c in capl]
    pi = random.choice(pos)

    # split the string apart at our chosen letter
    # capitalise the letter and re-combine the string
    left = ch[:pi -1] if pi > 0 else ""
    c = ch[pi].upper()
    right = ch[pi + 1:] if pi < len(ch) -1 else ""
    pw = f"{left}{c}{right}"

    # pick a random position within that password
    # where we can insert a symbol
    pi = random.randint(0, len(pw) - 1)

    # string slicing again
    left = pw[:pi] if pi > 0 else ""
    right = pw[pi:] if pi < len(pw) - 1 else ""

    # pick a random symbol
    symbol = random.choice(symbols)
    # create the final password
    pw = f"{left}{symbol}{right}"

    # split the password into blocks of 4 chars.
    xpw = [pw[i:i + 4] for i in range(0, len(pw), 4)]

    # join them together into one string seperated by a space
    op = " ".join(xpw)

    # display our work to the world
    print(op)

if __name__ == "__main__":
    pwgen()
