""" The LZW logic module. """

from archiver_package.core import AbcEncoder
from archiver_package.file_operations import FileOperator, OneFileTaker


class CodingLZW(AbcEncoder):
    """
    The LZW algorithm for coding and decoding a file defined by user.

        Attributes:

        compressed_data: list
            Storing the final compressed data after the algorithm is finished
        decompressed_data: str
            Storing the final compressed data after the algorithm is finished
        table_size_rate: int
            Number of bits defining the size of table

    """

    def __init__(self, input_data):

        super().__init__(input_data)

        self.compressed_data = []
        self.decompressed_data = ""
        self.table_size_rate = 64

    def compress_data(self):
        """ Makes the necessary data package for file compression. """

        maximum_table_size = 2 ** self.table_size_rate
        data = FileOperator.prepare_file_compress(self, 'r')

        # Building and initializing the dictionary.
        dictionary_size = 256
        dictionary = {chr(i): i for i in range(dictionary_size)}
        string = ""

        # LZW compression algorithm, iterating through the input symbols.

        for symbol in data:
            string_plus_symbol = string + symbol  # get input symbol.
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                self.compressed_data.append(dictionary[string])
                if len(dictionary) <= maximum_table_size:
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol

        if string in dictionary:
            self.compressed_data.append(dictionary[string])

        return self

    def decompress_data(self):
        """ Makes the necessary data package for file decompression. """

        FileOperator.prepare_file_decompress(self)
        raw_data = self.file_taker.the_data_raw
        self.compressed_data = OneFileTaker.convert_base64_to_dict(raw_data)

        next_code = 256
        string = ""

        # Building and initializing the dictionary.
        dictionary_size = 256
        dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

        # Iterating through the compressed data by LZW decompression algorithm

        for code in self.compressed_data:
            if code not in dictionary:
                dictionary[code] = string + (string[0])
            self.decompressed_data += dictionary[code]
            if len(string) != 0:
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]

        return self
