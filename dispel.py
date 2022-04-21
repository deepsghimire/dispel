#!/usr/bin/env python3

import argparse
import os
import bisect
import sys
def parse_args():
    parser = argparse.ArgumentParser(description="prints possible correction of word")
    parser.add_argument("word",type=str)
    return parser.parse_args()

class  WordsFileError(Exception):
    pass

class Corrector:
    """description"""
    def __init__(self,words_file):
        self.words_file = words_file
        self.all_words = self._read_words()

    def _read_words(self):
        if os.path.isfile(self.words_file):
            words = open(self.words_file).read().split('\n')
        else:
            raise WordsFileError(f"Cannot read word file {self.words_file}")
        return words

    def _word_exists(self,word):
        i = bisect.bisect_left(self.all_words,word)
        if i != len(self.all_words) and self.all_words[i] == word:
            return True
        return False
            

    def correct(self,input_word):
        if self._word_exists(input_word):
            return [input_word]
        else:
            return []





def main():
    #parse arguments
    #word is the only argument for now
    args = parse_args()
    wordfile = "words.txt"
    
    input_word = args.word
    corrector = Corrector(wordfile)

    possible_corrections = corrector.correct(input_word)
    for each in possible_corrections:
        print(each)

    # correctly exit
    if len(possible_corrections) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
        



if __name__ == '__main__':
    main()
    
