#!/usr/bin/env python
# CCDCPass by Grant Hernandez for the University of Florida
# No license. Public domain
import random
import sys
import string
import argparse
import math
from hashlib import sha512

NAME="CCDCPass"
VERSION="1.1"
MIN_WORD_LENGTH=4

# TODO: parameterize this function (i.e min length, max length, etc)
def readWordlist(filename, allowed):
    l = open(filename, 'r').read()

    l = l.split('\n')
    a = []

    vowels = set(['a', 'e', 'i', 'o', 'u'])
    allowedSet = set(allowed)
    possibleWords = 0

    # parse the wordlist
    for i in l:
        # TODO: make it so we can select words in different columns
        word = i

        # keep track of ALL of the possible words
        possibleWords += 1

        # avoid empty words
        if len(word) == 0:
            continue

        # Make sure the word has at least one vowel
        if len(set(word) - vowels) == len(word):
            continue

        # make sure the word doesn't have any disallowed characters
        if len(set(word) - allowedSet) != 0:
            continue

        # assert a minimum length
        if len(word) < MIN_WORD_LENGTH:
            continue

        # disallow words with just one character repeating
        if len(set(word)) <= 1:
            continue

        a.append(word)

    return a, possibleWords

def main(args):
    if args.format == "text":
        driver = driver_text
    elif args.format == "latex":
        driver = driver_latex
    else:
        sys.stderr.write("invalid driver type\n")
        return

    title = args.title
    numPassphrase = args.n

    if numPassphrase <= 0:
        sys.stderr.write("Invalid word count\n")
        sys.exit(1)

    # TODO: make these as inputs to the program
    minWords = 2
    maxWords = 4
    minNumbers = 1
    maxNumbers = 3
    minLength = 14
    maxLength = 20

    # seed can be any string or number. it is converted to a single number
    # for usage
    seedString = args.seed
    seedNumber = int(sha512(seedString).hexdigest(), 16)

    random.seed(seedNumber)

    # read wordlist with some character restrictions
    wordlist, possibleWords = readWordlist(args.wordlist, string.ascii_letters)

    # Write some stats
    sys.stderr.write("Wordlist stats %d/%d words\n" % (len(wordlist), possibleWords))

    if len(wordlist) == 0:
        sys.stderr.write("ERROR: Failed to read wordlist\n")
        sys.exit(1)

    passphrases = []
    word_freq = {}

    i = 0
    skippedStreak = 0
    tries = 0

    while i < numPassphrase:
        words = []
        numbers = []
        special = []
        tries += 1

        # notify if the requirements are too strong
        if skippedStreak >= 800:
            sys.stderr.write("ERROR: could not generate a valid passphrase %d times in a row\n" % skippedStreak)
            sys.exit(1)

        # gogogogo
        for j in range(random.randint(minWords, maxWords)):
            g = wordlist[random.randint(0, len(wordlist)-1)]
            c = list(g)
            c[0] = c[0].upper()
            g = "".join(c)
            words.append(g)

        # add some numbers
        numNumbers = random.randint(minNumbers,maxNumbers)
        for k, val in enumerate(range(numNumbers)):
            lrange = 0

            # dont start with 0
            if k == 0:
                lrange = 1

            # fire some numbers
            numbers.append(str(random.randint(lrange, 9)))

        special += '!'
        passphrase = "".join(words) + "".join(numbers) + "".join(special)

        # ensure that the passphrase meets our requirements
        if len(passphrase) < minLength or len(passphrase) > maxLength:
            skippedStreak += 1
            continue

        # calculate word frequency
        for word in words:
            if word not in word_freq:
                word_freq[word] = 0
            word_freq[word] += 1

        i += 1
        skippedStreak = 0
        passphrases.append(passphrase)

    if tries >= numPassphrase:
        sys.stderr.write("Success Ratio: %.2f%%\n" % (float(numPassphrase)/tries*100))
    else:
        sys.stderr.write("Number of tries %d\n" % (tries))

    # Calculate some stats
    duplicates = 0
    for k,v in word_freq.iteritems():
        if v > 1:
            duplicates += 1

    sys.stderr.write("Unique words: %d\n" % len(word_freq))

    tries = (possibleWords**minWords)*(10**minNumbers)
    tries_str = list(str(tries))
    lenner = len(tries_str)
    for i in range(1, len(tries_str)/3+1):
        if lenner-i*3 > 0:
            tries_str.insert(lenner-i*3, ',')

    sys.stderr.write("Min brute-forcing required: %s tries\n" % ("".join(tries_str)))
    sys.stderr.write("Duplicate words: %d\n" % (duplicates))

    # send the words to the output driver
    driver(passphrases, title, seedString, args.showseed)

def driver_latex(words, title, seed, showseed):
    output = open('template.tex').read()

    column = r"""\begin{minipage}[t]{.33\textwidth}
		\raggedright
		\begin{enumerate}
                \setcounter{enumi}{@@START@@}
                \itemsep-1em
		@@CONTENT@@
		\end{enumerate}
		\end{minipage}"""

    wordsPerPage = 90
    wordsPerCol = 30
    numColumns = int(math.ceil(float(len(words))/wordsPerCol))

    renderedColumns = []
    for i in range(numColumns):
        lindex = i*wordsPerCol
        rindex = min(lindex+wordsPerCol, len(words))
        colWords = words[lindex:rindex]

        if i and i % 3 == 0:
            renderedColumns.append(r"\newpage")

        lines = []
        for j, v in enumerate(colWords):
            if (j+1) % (10) == 0:
                lines.append("\item " + v + " \\\\[1.0cm]")
                #lines.append(r"\noindent\hspace{-1.5cm}\makebox[0.9\textwidth]{\rule{0.9\textwidth}{0.4pt}} \\[0.75cm]")
            else:
                lines.append("\item " + v + " \\\\[0.70cm]")

        renderedColumn = column.replace("@@CONTENT@@", "\n".join(lines))
        renderedColumn = renderedColumn.replace("@@START@@", str(lindex))
        renderedColumns.append(renderedColumn)

    output = output.replace('@@CONTENT@@', "\n".join(renderedColumns))
    output = output.replace('@@TITLE@@', title)

    if showseed:
        output = output.replace('@@AUTHOR@@',
            "Generated by %s %s with seed `%s'" % (NAME, VERSION, seed))
    else:
        output = output.replace('@@AUTHOR@@',
            "Generated by %s %s" % (NAME, VERSION))

    output = output.replace('UF CCDC Password List', "\n".join(words))

    print output

def driver_text(words, title, seed, showseed):
    for i in words:
        print i

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=NAME + ' ' + VERSION)
    parser.add_argument('seed', help='a password seed value')
    parser.add_argument('title', help='document title')

    parser.add_argument('-n', type=int, help='number of words', required=True)
    parser.add_argument('--wordlist', help='an input wordlist', required=True)
    parser.add_argument('--format', help='output format (\'text\' or \'latex\')', default="text" )
    parser.add_argument('--show-seed',
            dest='showseed', action='store_true',
            help='print the seed in output formats')
    parser.add_argument('--hide-seed',
            dest='showseed', action='store_false',
            help='hide the seed in output formats (default)')
    parser.set_defaults(showseed=False)

    args = parser.parse_args()

    main(args)
