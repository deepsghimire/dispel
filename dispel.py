#!/usr/bin/env python3

import argparse
import os
import bisect
import sys
import logging
from collections import Counter
import re

def parse_args():
    parser = argparse.ArgumentParser(description="prints possible correction of word")
    parser.add_argument("word",type=str)
    return parser.parse_args()


def configure_logs():
    logging.basicConfig(filename='dispel.log',filemode='w',encoding='utf-8',level=logging.DEBUG)


class  WordsFileError(Exception):
    pass

class Corrector:
    """description"""
    def __init__(self,words_file):
        self.words_file = words_file
        self.all_words = self._read_words()

    def _read_words(self):

       
        logging.info(f"the words  are in {self.words_file}")

        if os.path.isfile(self.words_file):
            words = Counter(re.findall(r'\w+',open(self.words_file).read()))
            logging.info(f"Words file contains {len(words)} words")
        else:
            logging.critical(f"{self.words_file} is not a file")
            raise WordsFileError(f"Cannot read word file {self.words_file}")
        return words


    def known(self,words):
        return set(w for w in words if w in self.all_words)

    def edits1(self,word):
        "All edits that are one edit away from 'word'."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i],word[i:]) for i in range(len(word)+1) ]
        deletes = [L + R[1:] for L,R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L,R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L,R in splits if R for c in letters]
        inserts = [L + c + R for L,R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self,word):
        "All edits that are two edits away from 'word'."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
        


    def _prob(self,word):
        return self.all_words[word]/sum(self.all_words.values())

    def candidates(self,word):
        return self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word))
            

    def correct(self,input_word):
        
        logging.info(f"The input text is: {input_word}")

        candidates = self.candidates(input_word)
        if candidates:
            return max(candidates,key=self._prob)
        else:
            return ''






def main():
    #parse arguments
    #word is the only argument for now
    configure_logs()
    args = parse_args()
    wordfile = "big.txt"
    
    input_word = args.word
    

    corrector = Corrector(wordfile)

    possible_correction = corrector.correct(input_word)
    print(possible_correction)

    # correctly exit

    logging.info(f" possible_correction: {possible_correction}")
    if len(possible_correction) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
        



if __name__ == '__main__':
    main()
    
