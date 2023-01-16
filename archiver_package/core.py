""" Core module for parent classes. """

import os.path
from abc import ABCMeta, abstractmethod
from six import with_metaclass


class AbcEncoder(with_metaclass(ABCMeta)):
    """
    A parent class for all encoding methods.
    """

    def __init__(self, input_data):
        self.filepath_name = input_data.filepath_name
        self.file_path = input_data.file_path
        self.filename = input_data.filename
        self.path = input_data.path
        self.original_names = input_data.original_names
        self.output_path = input_data.output_path
        self.input_size = os.path.getsize(self.path)
        self.compression_key = input_data.compression_key
        self.file_taker = None

    @abstractmethod
    def compress_data(self):
        """ Makes the necessary data package for file compression. """

    @abstractmethod
    def decompress_data(self):
        """ Makes the necessary data package for file decompression. """


class AbcFilesWork(with_metaclass(ABCMeta)):
    """
    A parent class for work with files.
    """

    def __init__(self, data_package):
        self.filepath_name = data_package.filepath_name
        self.file_path = data_package.file_path
        self.filename = data_package.filename
        self.path = data_package.path
        self.original_names = data_package.original_names
        self.output_path = data_package.output_path
        self.input_size = data_package.input_size
        self.compression_key = data_package.compression_key
        self.file_taker = None
        self.decompressed_data = data_package.decompressed_data

    @abstractmethod
    def prepare_file_decompress(self):
        """ Takes the necessary data from input file for file decompression logic. """

    @abstractmethod
    def prepare_file_compress(self, data_type_read):
        """ Takes data from source file for compression."""

    @staticmethod
    def compress_file(data_package, compression_key):
        """ Saves the compressed data into file by the chosen method. """

    @abstractmethod
    def decompress_file(self):
        """ Saves the decompressed data into file. """
