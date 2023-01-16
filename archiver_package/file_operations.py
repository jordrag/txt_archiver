""" This module makes all needed operations with files for compressing and decompressing. """

import os.path
import json
import base64
from archiver_package.core import *


class FileOperator(AbcFilesWork):
    """
    Summary class for file operations despite method.

    """

    def __init__(self):

        super().__init__(self)

    def prepare_file_compress(self, data_type_read):
        """ Takes data from source file for compression."""

        with open(self.path, data_type_read) as input_file:
            data = input_file.read()
            data = data.rstrip()
        return data

    def prepare_file_decompress(self):
        """ Takes the necessary data from input file for file decompression logic. """

        self.file_taker = OneFileTaker(self.path)
        self.original_names = self.file_taker.file_path

        self.output_path = self.filepath_name + "_decompressed" + \
                                                self.original_names[self.output_path.split(".")[0]]

        return self

    @staticmethod
    def compress_file(data_package, compression_key):
        """
        Saves the compressed data into file by the chosen method.

        Args:
            compression_key: str
            Depends on the chosen method and manages the future actions in the archiver.
        """

        with open(data_package.output_path, 'wb') as output_file:
            match compression_key:
                case "huff":
                    tree = data_package.reverse_mapping
                    bytes_list = data_package.bytes_list
                case "lzw":
                    tree = 0
                    bytes_list = OneFileMaker.hex_dict_factory(data_package.compressed_data)

            end_data = OneFileMaker(tree, data_package.original_names, bytes_list)
            output_file.write(end_data.end_string)

            # Compression rate calculation
            data_package.output_size = os.path.getsize(data_package.output_path)
            compression_percent = round(100 - data_package.output_size / data_package.input_size * 100, 1)

        final_note = "File compressed !"
        return [final_note, data_package.input_size, data_package.output_size, compression_percent]

    def decompress_file(self):
        """ Saves the decompressed data into file. """

        with open(self.output_path, "w", encoding="UTF-8") as output_file:
            for data in self.decompressed_data:
                output_file.write(data)

        final_note = "File decompressed !"
        return [final_note]


# ******************************************************************************

class OneFileMaker(object):
    """
    Makes a complex data packet ready to save in archive file.

        Attributes:

        dictlen_plus_pathlen: str
            Makes a string of dictionary length and data in BIN format.
        file_path: dict
            Original files info.
        data: list
            Prepared to be saved data, it is the original file content made by the chosen algorithm.
        dict_hex: list
            A base64 list representing converted tree if there is one like in Huffman logic.
        file_path_hex: dict
            The original file path info converted to HEX format.
        four_bytes_dict_len: str
            The key for tree length in four bytes format.
        four_bytes_path_len: str
            The key for path length in four bytes format.
        end_string: str
            The final serialized string ready to be written in compressed file.
    """

    def __init__(self, work_tree, file_path, data):
        self.dictlen_plus_pathlen = None
        self.file_path = file_path
        self.data = data
        self.dict_hex = self.hex_dict_factory(work_tree)
        self.file_path_hex = self.hex_dict_factory(file_path)
        self.four_bytes_dict_len = self.bin_len_string(self.dict_hex)
        self.four_bytes_path_len = self.bin_len_string(self.file_path_hex)
        self.end_string = self.final_data()

    @staticmethod
    def hex_factory(data):
        """
        Makes something in BIN to HEX format.

        args:
            data: str
            A string in BIN format (00010110) to be transformed to HEX format.
        """

        byte_array = bytearray()
        for i in range(0, len(data), 8):
            byte = data[i:i + 8]
            byte_array.append(int(byte, 2))
        return byte_array

    @staticmethod
    def hex_dict_factory(data):
        """
        Makes some dict to base64 format.

        args:
            data: dict
            A dictionary to be transformed to base64 format.
        """

        data_str = str(data).encode('ascii')
        test_data_bytes = base64.b64encode(data_str)

        return test_data_bytes

    @staticmethod
    def bin_len_string(data):
        """
        Calculates tree(dictionary) length and shape it in 4 bytes BIN string.

        args:
            data: dict
            The tree in dictionary format to be transformed in BIN, four bytes format.

        """

        dict_len = len(data)  # Dictionary length
        result = dict_len.to_bytes(length=4, byteorder="big")

        return result

    def final_data(self):
        """ Makes the final data packet to save in file. """

        # Makes a string of dictionary length and data in BIN format
        self.dictlen_plus_pathlen = self.four_bytes_path_len + self.four_bytes_dict_len

        # Makes the common string in HEX format

        keys_plus_data_hex = self.dictlen_plus_pathlen + self.data
        file_path_hex = self.hex_dict_factory(self.file_path)
        end_string = keys_plus_data_hex + self.dict_hex + file_path_hex

        return end_string


class OneFileTaker(object):
    """
    Reads a complex data packet from archive file and unsplit it to necessary data.

        Arguments:

        file_to_read: str
            The input file to read from.

        Attributes:

        file_path_len: int
            A key for the length of file path info saved in the end of the compressed file.
        dict_len: int
            A key for the length of tree info saved in the end of the compressed file.
        loaded_file_path: str
            The loaded file path in base64 format.
        loaded_dict: str
            The loaded tree for Huffman logic in base64 format.
        the_data_raw: str
            The raw data loaded from compressed file.
        the_data: str
            The extracted data in original format.
        file_to_read: str
            The source file to be decompressed.
        tree: dict
            The converted from base64 to dictionary Huffman tree if it's applicable.
        file_path: dict
            The converted from base64 to dictionary file path info.
    """

    def __init__(self, file_to_read):
        self.file_path_len = None
        self.dict_len = None
        self.loaded_file_path = None
        self.loaded_dict = None
        self.the_data_raw = None
        self.the_data = None
        self.file_to_read = file_to_read
        self.read_file_info()
        self.tree = self.convert_base64_to_dict(self.loaded_dict)
        self.file_path = self.convert_base64_to_dict(self.loaded_file_path)

    bit_string = ""

    @staticmethod
    def convert_hex_to_bin(data):
        """
        Converts HEX data string to BIN format.

        Args:
            data: str
            A string represented in HEX format for transformation in BIN.

        """

        bit_string = ""
        for byte in data:
            byte = bin(byte)
            bit_string += byte

        bit_string_final = ""
        bit_string_split = bit_string.split("0b")
        for i in range(1, len(bit_string_split)):
            if len(bit_string_split[i]) != 8:
                to_add = 8 - len(bit_string_split[i])
                bit_string_split[i] = to_add * "0" + bit_string_split[i]
            bit_string_final += bit_string_split[i]

        return bit_string_final

    @staticmethod
    def convert_base64_to_dict(data):
        """
        Converts a base64 data to dictionary.

        Args:
            data: str
            A string in base64 format to be converted to simple dictionary.

        """

        data_loaded = base64.b64decode(data)  # Decode from Base64
        data_str = data_loaded.decode("ascii")
        temp_dict = data_str.replace("'", "\"")  # Prepare to convert string dict to dict
        result = json.loads(temp_dict)

        return result

    def read_file_info(self):
        """ Read and split all needed info from the compressed file."""

        # Reading all info from file
        with open(self.file_to_read, "rb") as file_read:
            read_all = file_read.read()

        # Splitting the summary info to separate functions.

        self.file_path_len = int(self.convert_hex_to_bin(read_all[:4]), 2)
        self.dict_len = int(self.convert_hex_to_bin(read_all[4:8]), 2)
        self.loaded_file_path = read_all[-self.file_path_len:]
        self.loaded_dict = read_all[-(self.dict_len + self.file_path_len):-self.file_path_len]
        self.the_data_raw = read_all[8:-(self.dict_len + self.file_path_len)]
        the_data = bytearray(self.the_data_raw)
        self.the_data = self.convert_hex_to_bin(the_data)

        return self
