import tokenize
import os
import sys
import subprocess
from icecream import ic


def pathmaker(first_segment, *in_path_segments, rev=False):
    _path = first_segment

    _path = os.path.join(_path, *in_path_segments)
    if rev is True or sys.platform not in ['win32', 'linux']:
        return os.path.normpath(_path)
    return os.path.normpath(_path).replace(os.path.sep, '/')


MAIN_DIR = pathmaker(subprocess.run("git rev-parse --show-toplevel".split(), check=True, shell=True, capture_output=True, text=True).stdout.strip())


def get_comments(fileObj):
    for toktype, tok, start, end, line in tokenize.generate_tokens(fileObj.readline):
        # we can also use token.tok_name[toktype] instead of 'COMMENT'
        # from the token module
        ic(tokenize(toktype))
        if toktype == tokenize.COMMENT and 'region [' not in tok and 'region[' not in tok and "Imports" not in tok and "import" not in tok:
            pass
            # print(tok + '    ' + str(start))


def get_files():
    for dirname, folderlist, filelist in os.walk(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidAppData\gidappdata"):
        if all(excl_dir.casefold() not in dirname.casefold() for excl_dir in ['.git', '.venv', '.vscode', '__pycache__', '.pytest_cache', "private_quick_scripts", "converted_designer_files"]):
            for file in filelist:
                if file.endswith('.py'):
                    path = pathmaker(dirname, file)
                    with open(path, 'r') as f:
                        get_comments(f)


get_files()
