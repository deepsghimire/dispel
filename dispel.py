#!/usr/bin/env python3

import argparse
import os
import bisect
import sys
import logging

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
            words = open(self.words_file).read().split('\n')
            logging.info(f"Words file contains {len(words)} words")
        else:
            logging.critical(f"{self.words_file} is not a file")
            raise WordsFileError(f"Cannot read word file {self.words_file}")
        return words

    def _word_exists(self,word):
        i = bisect.bisect_left(self.all_words,word)
        if i != len(self.all_words) and self.all_words[i] == word:
            return True
        return False
            

    def correct(self,input_word):
        
        logging.info(f"The input text is: {input_word}")

        if self._word_exists(input_word):
            return [input_word]
        else:
            return []





def main():
    #parse arguments
    #word is the only argument for now
    configure_logs()
    args = parse_args()
    wordfile = "words.txt"
    
    input_word = args.word
    

    corrector = Corrector(wordfile)

    possible_corrections = corrector.correct(input_word)
    for each in possible_corrections:
        print(each)

    # correctly exit

    logging.info(f" 10 possible_corrections: {possible_corrections[:10]}")
    if len(possible_corrections) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
        



if __name__ == '__main__':
    main()
    
