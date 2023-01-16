"""
This is the input module for the entire archiver. Here it accepts the entry parameters
and what the user wants to make. The entry could be made from console (by default) or from this
module with different test scenarios.

"""

import argparse
import random


class UserInput(object):
    """ Takes the necessary data from console with commands from user. """

    @staticmethod
    def command_args():
        """ Getting arguments from command line. """

        parser = argparse.ArgumentParser()
        parser.add_argument('--comp', type=str, required=True,
                            help='Compression type Huffman(huff) or LZW(lzw)')
        parser.add_argument('--src', type=str, required=True,
                            help='Source path for the chosen action')
        args = parser.parse_args()

        compression = args.comp
        source = args.src

        # ************ Test scenarios with defined or random generated list. **************

        # compression = "huff"

        # Use this part for "White noise" simulation
        # plain_text = ""
        # for i in range(10000000):
        #     chr_code = random.randrange(32,126)
        #     chr_to_add = chr(chr_code)
        #     plain_text += chr_to_add

        # For use in generic way
        # plain_text = "The computer usually has a motherboard hosting a variaty of chips such " \
        #              "as the CPU." * 500000

        # Unlock this part when want to test compress and lock it when decompress

        # source = "examples/sample.txt"
        # with open(source, "w", encoding="UTF-8") as text_sample:
        #     text_sample.write(plain_text)

        # Unlock this when want to decompress
        # source = "examples/sample.dar"

        # ********************************************************************

        return compression, source
