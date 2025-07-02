#!/usr/bin/env python3

import argparse
import os
import re


delimiter_patterns = r"[ ;,\"\':\n=\[\]]"
tokens_to_skip = [ 'true','false',' ', '[', ']', '', '-' ] 

def highlight(word: str, sentence: str) -> str:
    return re.sub(re.escape(word), f"\033[91m{word}\033[0m", sentence, flags=re.IGNORECASE)

if __name__ == "__main__":

    # List of allowed positional arguments and function to call
    # command_map = {'input-file': download_saved_searches, } 

    # Setup argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument('command', choices=command_map.keys())
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output.")
    parser.add_argument("-f", "--input-file", help="Input file to process.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    #command_map[args.command]( splunkClient )

    with open(args.input_file, 'r') as file:
        for log in file:

            tokenDict = {}
            tokenized = re.split(delimiter_patterns,log)
            for token in tokenized:
                if token  in tokens_to_skip:
                    continue
                if tokenDict.get(token) is not None:
                    tokenDict[token] += 1
                else:
                    tokenDict[token] = 1

            highlighted_log = log.strip() 
            duplicates = ""

            for k,v in tokenDict.items():
                if v > 1:
                    highlighted_log = highlight(k,highlighted_log)
                    duplicates += f"\tDuplicate found {k} : ({v})\n"
            print(highlighted_log)
            if args.verbose:
                print(duplicates)
