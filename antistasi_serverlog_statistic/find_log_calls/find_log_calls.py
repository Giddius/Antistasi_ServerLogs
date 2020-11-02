# region [Imports]

# * Standard Library Imports -->
import os
import re
from pprint import pformat

# * Third Party Imports -->
import regex

# * Gid Imports -->
import gidlogger as glog
from antistasi_serverlog_statistic.utilities.misc import readit, pathmaker, appendwriteit

# endregion[Imports]

__updated__ = '2020-11-02 21:24:23'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# Path to the Antistasi repo base folder, here my local path for example, this has to be changend if used elsewhere than my pc...
ANTISTASI_FOLDER = pathmaker(r"D:\Dropbox\hobby\Modding\Programs\Github\Foreign_Repos\A3-Antistasi")

# The regex pattern to get a multiline log call, it is not compiled as it is used with the "regex" 3rd party package and not the Stdlib "re"
LOG_REGEX = r"(?<=.*?)\[[^;]*?(?!\n\n)\]\scall A3A_fnc_log"

# regex to just find all calls to the log function, actually compiled, because it is used with the "re" Stdlib Package
AMOUNT_REGEX = re.compile(r"A3A_fnc_log")

# endregion[Constants]


def find_files():
    """
    generator to find all "sqf" files recursively.

    Yields:
        str: the full filepath to the sqf file
    """
    for dirname, folderlist, filelist in os.walk(ANTISTASI_FOLDER):
        for _file in filelist:
            if _file.endswith('.sqf') and 'Navigation' not in dirname:
                yield pathmaker(dirname, _file)


def read_files():
    """
    generator that reads the contents of each file and yields them, calls the find_files-function itself

    if a file can't be read in, it prints the file with the error message to stdout, but excepts the error. This happend with 4 UPSMON FILES

    Yields:
        tuple: a tuple consisting of the file_path[str] and the file_content[str]
    """
    for _path in find_files():
        try:
            _content = readit(_path, in_errors='replace', in_encoding='utf-8')
            yield (_path, _content)
        except UnicodeDecodeError as error:
            print(_path + ' ---> ' + str(error))
            yield(_path, "")


def get_line_number(target, line_list: list):
    """
    helper function to determine the line number of the last line of the log call.

    goes through the file content line by line and checks if the log call is in there. if the log call is multiline,
    it checks if the last line of the call is in the line of the file. returns the index of the line + 1.
    (as linenumbers start at 1, but python indexes start at 0)

    Args:
        target (str): the actual log call string
        line_list (list): the content of the file split by newlines into list of lines

    Returns:
        int: the line number of the log call, or line number of last line of log call in multiline calls
    """
    for index, line in line_list:
        if len(target.splitlines()) > 1:
            if target.splitlines()[-1] in line:
                return index + 1
        else:
            if target in line:
                return index + 1


def find_log_calls(path_content_tuple):
    """
    main function to find all log calls with the call variables.

    takes in an tuple of "path" and "content" like from the "read_files" function and tries to use regex to get all log calls.

    Args:
        path_content_tuple(tuple): a tuple consisting of the file_path[str] and the file_content[str]

    Returns:
        tuple: a tuple of _path and a list of log_calls with the line number already added.
    """
    _out_list = []
    path, content = path_content_tuple
    # checking the file for the general amount of calls to "A3A_fnc_Log", needed to filter all regex matches.
    _amount = len(AMOUNT_REGEX.findall(content))

    # creating a list of lines split by newline from the content for later finding the line number
    _line_list = [(index, line) for index, line in enumerate(content.splitlines())]

    # finding all "LOG_REGEX" matches, including overlapse, this is important, to actually be able to match multiline log calls
    _result = regex.findall(LOG_REGEX, content, re.DOTALL, overlapped=True)
    print("searched: " + path)
    if _result:

        # sorting the result by lenght, as to be able to filter out the false positive matches that match half the file
        _result = sorted(_result, key=len)

        # getting the shortest matches out, up to the amount of overall matches to "A3A_fnc_log"
        for i in range(_amount):
            try:
                _number = get_line_number(_result[i], _line_list)

                # adding line number to the match ,as just adding it as tuple didn't work
                _out_list.append(str(_result[i]) + ' \n## Line Number: ' + str(_number))
            except IndexError:

                # if we ever have less matches than overall calls to "A3A_fnc_log" this will be triggered and write the filepath and all findall matches for that file to the error file
                appendwriteit('error.txt', path.replace('D:/Dropbox/hobby/Modding/Programs/Github/Foreign_Repos/', '') + ' +++++++ ' + pformat(_result, indent=2))
        return path, _out_list
    else:

        # if we don't match anything returning a tuple of _path and None, so not to break the map algorithm
        return path, None


# region[Main_Exec]
if __name__ == '__main__':

    # cleaning the previously generated files
    for _file in ['log_calls.txt', 'error.txt']:
        if os.path.isfile(_file):
            os.remove(_file)

    _fin = map(find_log_calls, read_files())
    print("################################################ finished searching ################################################")

    for _path, result in _fin:
        if result:
            _path = _path.replace('D:/Dropbox/hobby/Modding/Programs/Github/Foreign_Repos/', '')
            appendwriteit('log_calls.txt', f"\n\n\n\n#######################################\n{_path} ----->\n\n")
            for item in result:
                appendwriteit('log_calls.txt', str(item) + '\n\n-------------------\n')


# endregion[Main_Exec]
