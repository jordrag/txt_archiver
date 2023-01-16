from archiver_package.archiver_input import *
from archiver_package.archiver_manager import *
import time


# *************************************************************************

def run_archiver():
    """ Application to coordinate the relationships between the modules."""

    try:
        print("Please wait....")
        start_time = time.time()

        input_data = UserInput.command_args()
        compression = input_data[0]
        source = input_data[1]

        manager = ArchiveManager(compression, source)
        result = manager.manage_compression()

        end_time = time.time()
        spent_time = end_time - start_time

        ArchiveManager.final_result_visual(result, spent_time)

    except Exception:
        print("\n**** I can't handle with this. "
              "Please check your input data or chosen options ! ****\n")


# *************************************************************************

run_archiver()
