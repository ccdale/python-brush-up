# Python List Comprehension Tutorial
We will be writing a password generator. Along the way we will encounter
certain patterns that crop up time and again that are more elagently
described using Pythons List Comprehension paragigm.

There is one major caveat with the methods described below to generate
passwords - during the course of the computation the output is encoded to
hexadecimal, the letter range of the final password is only [a-fA-F].

## Password Generator
Generate passwords from a word list, with one added symbol and
one capitalised letter.

It is annoying to have to type system generated passwords when using an
interface such as a mobile phone.  Therefore, try to make passwords that are
comprised mostly of numbers and lowercase letters with one letter
capitalised and one symbol.

### Method
* pick 4 random words from a wordlist
* pass it through the sha256 hash algorhythm to generate 64 characters
* randomly pick 15 of those characters
* capitalise one of the letters
* add a symbol in a random position

Result is a 16 character password comprising mostly numbers and lowercase
letters with one capitalised letter and one symbol.

Output the password as blocks of 4 characters for ease of use.


### pwgen.py
From the Python standard library we will need the
[random](https://docs.python.org/3/library/random.html) and
[hashlib](https://docs.python.org/3/library/hashlib.html) packages.

```
import hashlib
import random

# initialise the random number generator
random.seed()

def pwgen():
    pass

if __name__ == "__main__":
    pwgen()
```

### Obtain some Data
We will need to read a file of words into a python list and also define a
string of acceptable letters that can be capitalised - letters that when
capitalised can not be confused for numbers or other letters.  We'll also
require a string of acceptable symbols.

```
def pwgen():
    # acceptable list of chars that can be capitalised
    capl = "acdefghjklmnpqrstuvwxyz"

    # list of acceptable symbols
    symbols = "=-!$%^&*(){}[]"

    # wordlist.txt is a file of one word per line that is in the same dir as
    # this python file.
    # read the words into a list (note: each word will still have the
    # trailing newline)
    with open("wordlist.txt", "r") as wl:
        wlist = wl.readlines()
```

### Pick 4 Random Words from the List
We now want to pick 4 random words from the wordlist and make a phrase of
them. We'll be using the
[range](https://docs.python.org/3/library/functions.html#func-range)
function to count how many we currently have.  We'll also be using the
`choice` function of the random library to pick a random word from the
list.

```
# pick 4 random words
# init a new list
words = []
for i in range(4):
    xword = random.choice(wlist)
    word = xword.strip()
    words.append(word)
```
To be more pythonic we can use list comprehension to create the 4 word list
```
words = [random.choice(wlist) for i in range(4)]
```
However, the random module also has a `choices` function that can return a
list of items:
```
words = random.choices(wlist, k=4)
```
Also, each of our words still has the trailing newline so one more
comprehension is still needed. `rstrip` removes trailing whitespace from the
end of a string (newline chars. are counted as whitespace)
```
words = [word.rstrip() for word in random.choices(wlist, k=4)]
```

### Make a 4 word phrase
We now want to merge the list of words we have picked into a string,
seperating them with a `space`. We don't need to add a space at the start of
the string, which is why we check the length of the string before we append
the word to it.
```
phrase = ""
for word in words:
    if len(phrase) == 0:
        phrase = word
    else:
        phrase += " " + word
```
We can use the `join` string function to make that more pythonic.
```
phrase = " ".join(words)
```

Now our pwgen function code looks like this
```
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

if __name__ == "__main__":
    pwgen()
```

### Hashing the String
Lets add some line noise to our password by hashing the phrase string with
the sha256 hash function.  This will produce 64 characters of seeming
randomness. We'll use the `hexdigest` function to output a hexadecimal
string representation of the hash.

The hashlib functions all work on byte arrays not on strings, so we have to
convert our string first with the `encode()` function
```
bphrase = phrase.encode()
h256 = hashlib.sha256(bphrase)
hprase = h256.hexdigest()
```
Though that'll be best all on one line, methinks.
```
hphrase = hashlib.sha256(phrase.encode()).hexdigest()
```

### Pick 15 random chars. from the hashed phrase
Our final password will be 16 characters long, so lets grab 15 random
characters from the hashed password to use as our password base.
```
ch = ""
for i in range(16):
    ch += random.choice(hprase)
```
Once again we make that a tad more pythonic using the `join` string function
and the `choices` function of the random module
```
ch = "".join(random.choices(hphrase, k=15))
```
We *could* go all-in by combining the hashing and picking steps together
into one line, however that then becomes unreadable, so I don't recommend
this
```
ch = "".join(random.choices(hashlib.sha256(phrase.encode()).hexdigest(), k=15))
```

Our script is starting to take shape now.
```
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


if __name__ == "__main__":
    pwgen()
```

### Pick a letter to capitalise
Our password string is now combined of numbers and lowercase letters - lets
pick a random letter from that string and capitalise it.

To do that we'll need to now where in the string the letters are, and filter
out any that are not in our acceptable list of letters to capitalise.

```
# create a list to hold the char. positions
pos = []
# iterate through the string
for c in ch:
    # check to see if the current char is in the acceptable list
    if c in capl:
        # it is, so append it's position in the string to the list of
        # positions
        pos.append(ch.index(c))
```
We can use a list comprehension here as well (anytime you find yourself
writing `for x in y` you'll probably be able to simplify things using
comprehensions).
```
pos = [ch.index(c) for c in ch if c in capl]
```
So now we know where in the string all the letters are (for now we'll assume
that there are actually letters, there may not be, but we'll add some
checking in later). Lets pick a random letter to capitalise.
```
pi = random.choice(pos)
```
We now want to split our string into three parts.  The sub-string to the
left of our chosen letter, the chosen letter itself and the sub-string to
the right of that letter.

We do that using Pythons string slicing - `string[start:length]`. We also
check that the chosen letter isn't the first or last one, if it is we set
left or right to be the empty string respectively. Remember that `pi` here
is the position in the string of our chosen letter and character positions
are zero-based. We also upper case the chosen letter using Pythons.  We are
left with a password that is 15 characters long with one uppercase letter.
`string.upper()` function.
```
left = ch[:pi -1] if pi > 0 else ""
c = ch[pi].upper()
right = ch[pi + 1:] if pi < len(ch) -1 else ""
pw = f"{left}{c}{right}"
```

### Add in a random symbol
We now want to pick a random symbol from our symbol string and pick a random
position to insert it into the string.  We use the `randint` function from
the random library to pick a random integer that is guaranteed to be less
than the length of the string. (remember string positions are zero-based).

```
# pick a random position within that password
# where we can insert a symbol
pi = random.randint(0, len(pw) - 1)
```
We need to split the string apart at that position as we did above, though
we only need 2 parts this time.
```
# string slicing again
left = pw[:pi] if pi > 0 else ""
right = pw[pi:] if pi < len(pw) - 1 else ""
```
Now we pick a random symbol from our symbol string
```
symbol = random.choice(symbols)
```
and insert it into our string, joining all three parts together
```
pw = f"{left}{symbol}{right}"
```

So, we are almost there, we could at this point just print the password to
the terminal and exit, however, this is a 16 character password of random
noise, so will still be quite difficult to remember and type.  Therefore
lets make things a little easier by outputting the password as 4 blocks of 4
characters each.

```
xpw = []
for i in range(4):
    ci = i * 4
    xpw.append(pw[ci:ci + 4])
```
Remember what I said above about `for x in y`? Yes, this is ripe for another
spot of comprehension.  The python standard function `range` takes either 1
parameter or 3.  If one, it is taken as the `stop` parameter (produces a
list of numbers from zero to stop - 1), if 3 the params are `start`, `stop`
and `step`. We also add a spot of string slicing into the mix to spice
things up a bit, and to make you look twice before comprehension dawns!
```
xpw = [pw[i:i + 4] for i in range(0, len(pw), 4)]
```
Now we have a list of 4 sets of 4 characters.

We can join them together, seperating them with a space thusly:
```
op = ""
for zpw in xpw:
    op += " " + zpw if len(op) > 0 else zpw
```
Or, as we are becoming Python Divas now, we use the `join` string function
once again to join them together seperated by a space.
```
op = " ".join(xpw)
```

All that remains is to output the password to the teminal.  Our script is
complete.
```
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
```
