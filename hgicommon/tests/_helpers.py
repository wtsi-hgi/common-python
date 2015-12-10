from tempfile import mkdtemp, mkstemp
from typing import Any, List, Callable

from math import ceil


def write_data_to_files_in_temp_directory(data: List[Any], spread_over_n_files: int, separator: str='\n',
                                          temp_directory: str=None, file_prefix="") -> str:
    """
    Writes the given data over the given number of files in a temporary directory.
    :param data: the data that is to be written to the files
    :param spread_over_n_files: the number of files in which the data is to be spread over
    :param separator: the separator between data items in each file
    :param temp_directory: the specific temp directory to use
    :param file_prefix: prefix to the files created
    :return: the location of the temp directory
    """
    if temp_directory is None:
        temp_directory = mkdtemp(suffix=write_data_to_files_in_temp_directory.__name__)

    datum_per_file = ceil(len(data) / spread_over_n_files)
    for i in range(spread_over_n_files):
        start_at = i * datum_per_file
        end_at = start_at + datum_per_file
        to_write = separator.join([str(x) for x in data[start_at:end_at]])

        file_location = mkstemp(dir=temp_directory, prefix=file_prefix)[1]
        with open(file_location, 'w') as file:
            file.write(to_write)

    return temp_directory


def extract_data_from_file(file_location: str, parser: Callable[[str], Any]=lambda data: data, separator: str=None) \
        -> List[Any]:
    """
    TODO
    :param file_location:
    :param parser:
    :param separator:
    :return:
    """
    with open(file_location, 'r') as file:
        contents = file.read()

    if separator is not None:
        raw_data = contents.split(separator)
    else:
        raw_data = [contents]

    extracted = []
    for item in raw_data:
        parsed = parser(item)
        extracted.append(parsed)

    return extracted
