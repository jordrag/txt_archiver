""" The Huffman logic module. """

import heapq
import json
from archiver_package.core import AbcEncoder
from archiver_package.file_operations import FileOperator


class HeapNode(object):
    """ Help class for calculating node frequency in the tree. """

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # defining comparators less_than and equals
    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, HeapNode):
            return False
        return self.freq == other.freq


class HuffmanCoding(AbcEncoder):
    """
    The Huffman algorithm for coding and decoding common file defined by user.

        Attributes:

        heap: list
            Supports the list of made nodes(heaps) by Huffman algorithm
        codes: dict
            The draft of "The tree" needed for decoding info taken from compressed file.
        reverse_mapping: dict
            "The tree" needed for decoding info taken from compressed file.
        bytes_list: list
            List of bytes representing the compressed info by Huffman logic and ready to be written
            in archive file.
        decompressed_data: list
            The decoded info ready to be saved in decompressed file.
        full_tree: bool
            A flag for length of Huffman tree keys, preventing the popular Huffman logic problem
            with only one symbol to compress.

    """
    def __init__(self, input_data):

        super().__init__(input_data)

        self.tree_bytes_list = None
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.bytes_list = None
        self.decompressed_data = None
        self.full_tree = False

    # ********** methods for compression *********************

    @staticmethod
    def make_frequency_dict(text):
        """
        Calculate the frequency of each letter in the file.

        Args:

        text: str
            The input text string to deal with.

        """

        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        """
        Fill the heap queue with tree nodes.

        Args:
            frequency: dict
            A dictionary with calculated frequencies of each met character.

        """

        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)
        if len(self.heap) > 1:
            self.full_tree = True

    def merge_nodes(self):
        """ Merge each two nodes in one new, equal to the sum of them. """

        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        """
        A help method for each node code making.

        Args:
            root: object
                A node of tree to be processed.
            current_code: str
                A string in BIN format coding the text.
        """

        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        """ Make binary code for each node. """

        root = heapq.heappop(self.heap)
        current_code = ""
        if not self.full_tree:
            current_code = "0"
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        """
        Make the string for archived file.

        Args:
            text: str
            The input string for encoding.

        """

        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    @staticmethod
    def pad_encoded_text(encoded_text):
        """ Pads necessary quantity of bits to the end of encoded text so its length to be multiple
        of 8 (one byte has 8 bits).
        The key for number of padded symbols in the end is added to the beginning of the encoded
        text as <padded info>.

        Args:
            encoded_text: str
            The whole text from source file encoded concerning Huffman method.

        """

        extra_padding = 8 - len(encoded_text) % 8
        for _ in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text

        return encoded_text

    @staticmethod
    def get_byte_array(padded_encoded_text):
        """
        Makes encoded string in bits to a new encoded string in bytes.

        Args:
            padded_encoded_text: str
            The encoded and padded with additional info text.

        """

        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        byte_array = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            byte_array.append(int(byte, 2))
        return byte_array

    # ***************** methods for decompression *******************

    @staticmethod
    def remove_padding(padded_encoded_text):
        """
        Removes the padded bits from the string taken off the archived file.

        Args:
            padded_encoded_text: str
            The whole encoded string taken from the archive file.

        """

        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        """
        Decode the input text string from compressed file.

        Args:
            encoded_text: str
            The encoded text cleaned up from the padded info.

        """

        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += chr(character)
                current_code = ""

        return decoded_text

    # ************** final data for saving compressed and help files **********************

    def compress_data(self):
        """ Makes the necessary data package for file compression. """

        text = FileOperator.prepare_file_compress(self, "rb")

        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        byte_array = self.get_byte_array(padded_encoded_text)
        self.bytes_list = bytes(byte_array)
        self.tree_bytes_list = json.dumps(self.reverse_mapping).encode("utf-8")

        return self

    # ******************* final data for saving decompressed file **********************

    def decompress_data(self):
        """ Makes the necessary data package for file decompression. """

        FileOperator.prepare_file_decompress(self)
        self.reverse_mapping = self.file_taker.tree
        bit_string = self.file_taker.the_data

        encoded_text = self.remove_padding(bit_string)
        self.decompressed_data = self.decode_text(encoded_text)

        return self
