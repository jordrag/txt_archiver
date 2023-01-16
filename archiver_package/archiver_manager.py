"""
The manager of the archiver, it prepares all the needed arguments for the work ahead, manages the
right action which to be taken and prints the final result.

"""

import os
from archiver_package.huffman import HuffmanCoding
from archiver_package.lzw import CodingLZW
from archiver_package.file_operations import FileOperator


class ArchiveManager(object):
    """
    Prepare all needed data for every kind of compression.

        Args:
        compression: str
            The chosen compression method (LZW or HUffman).
        source: str
            The source file to deal with, the path to it.

        Attributes:

        compression_key: str
            The key defining preferred algorithm.
        action_key: str
            Action to be done depending on the file extension.
        path: str
            The path to the file for compress/decompress.
        archive_extension: str
            Defines archive file extension.
        original_names: dict
            A dictionary containing info about original file names, extensions and paths.
        filepath_name: str
            Contains path and filename without file extension.
        file_extension: str
            The file extension.
        output_path: str
            The output path where to save the archive file with the chosen extension.
        file_path: str
            The file path.
        filename: str
            The file name.

    """

    def __init__(self, compression, source):
        self.compression_key = compression
        self.path = source
        self.archive_extension = ".dar"
        self.original_names = {}
        self.filepath_name, self.file_extension = os.path.splitext(self.path)
        self.output_path = self.filepath_name + self.archive_extension
        file_split = self.filepath_name.split("/")
        self.file_path = "/".join(file_split[0:len(file_split)-1])
        self.filename = file_split[len(file_split)-1]
        self.original_names[self.filepath_name] = self.file_extension

    def manage_compression(self):
        """
        Take the right compression method and action depending on user's command and file
        extension.
        """
        work_object = None
        match self.compression_key:
            case "huff":
                work_object = HuffmanCoding(self)
            case "lzw":
                work_object = CodingLZW(self)

        if self.file_extension == self.archive_extension:
            # Decompressing file
            work_object = work_object.decompress_data()
            final_result = FileOperator.decompress_file(work_object)
        else:
            # Compressing file
            work_object = work_object.compress_data()
            final_result = FileOperator.compress_file(work_object, self.compression_key)

        return final_result

    @staticmethod
    def final_result_visual(final_data, spent_time):
        """
        Forming and representing the final info about compression ratio and the time spent for
        the operation.

        Args:
            final_data: list
            A list of final data for reporting.

            spent_time: float
            Calculated time between start and final of the operation in secs.

        """

        print(final_data[0])
        if len(final_data) > 1:
            print(f"\nBefore: {final_data[1]} bytes, after: {final_data[2]} bytes, "
                  f"compression ratio {final_data[3]} %")

        print(f"\nTime spent on the operation: {spent_time:.2f} s")
