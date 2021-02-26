import os
import subprocess
import shutil
import importlib.util
import pkgutil
import sys
import logging
from inspect import getmembers, isclass, isfunction
logging.disable(logging.CRITICAL)
from pprint import pprint
import json

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def pathmaker(first_segment, *in_path_segments, rev=False):
    _path = first_segment

    _path = os.path.join(_path, *in_path_segments)
    if rev is True or sys.platform not in ['win32', 'linux']:
        return os.path.normpath(_path)
    return os.path.normpath(_path).replace(os.path.sep, '/')


def writejson(in_object, in_file, sort_keys=True, indent=4):
    with open(in_file, 'w') as jsonoutfile:
        print(f"writing json '{in_file}'")
        json.dump(in_object, jsonoutfile, sort_keys=sort_keys, indent=indent)


MAIN_DIR = pathmaker(subprocess.run("git rev-parse --show-toplevel".split(), check=True, shell=True, capture_output=True, text=True).stdout.strip())
MAIN_MODULE_DIR = pathmaker(MAIN_DIR, 'antipetros_discordbot')


missing_dict = {}


def load_module(path):
    mod_path = pathmaker(path).casefold().replace(MAIN_DIR.casefold() + '/', '')
    import_path = mod_path.split('.')[0].replace('/', '.')
    try:
        module = importlib.import_module(import_path)
        return mod_path, module
    except Exception as error:
        # print(f"{error.__class__.__name__}  |  {path=}")
        return None


def get_files(in_dir):
    for dirname, folderlist, filelist in os.walk(in_dir):
        if all(excl_dir.casefold() not in dirname.casefold() for excl_dir in ['.git', '.venv', '.vscode', '__pycache__', '.pytest_cache', "private_quick_scripts", "dev_tools_and_scripts"]):
            for file in filelist:
                if file.endswith('.py'):
                    path = pathmaker(dirname, file)
                    module = load_module(path)
                    if module is not None:
                        yield module[0], module[1]


def get_missing_module_docstring(modules):
    global missing_dict
    with open('missing_module_docstrings.txt', 'w') as f:
        for module_path, module in modules:
            module_name = module.__name__.split('.')[-1]
            if module_name not in missing_dict:
                missing_dict[module_name] = {'missing_docstring': False, 'classes': {}, 'functions': {}}
            if module.__doc__ is None and os.path.basename(module_path) != "__init__.py":
                missing_dict[module_name]['missing_docstring'] = True
                with open('missing_module_docstrings.txt', 'a') as ft:
                    f.write(f"Missing Docstring for module '{module_name}', with path '{module_path}'\n\n")

            yield module_path, module


def get_missing_class_docstring(modules):
    global missing_dict
    with open('missing_class_docstrings.txt', 'w') as f:
        for module_path, module in modules:
            module_name = module.__name__.split('.')[-1]
            for name, _object in getmembers(module, predicate=isclass):

                if _object.__module__ == module.__name__:
                    missing_dict[module_name]['classes'][name] = {'missing_docstring': False, 'methods': {}}
                    if _object.__doc__ is None:
                        missing_dict[module_name]['classes'][name]['missing_docstring'] = True
                        f.write(f"Missing Docstring for Class '{name}', in module '{module_name}', with path '{module_path}'\n\n")
            yield module_path, module


def get_missing_function_docstring(modules):
    global missing_dict
    with open('missing_function_docstrings.txt', 'w') as f:
        for module_path, module in modules:
            module_name = module.__name__.split('.')[-1]
            for name, _object in getmembers(module, predicate=isfunction):

                if _object.__module__ == module.__name__:
                    missing_dict[module_name]['functions'][name] = {'missing_docstring': False}
                    if _object.__doc__ is None:
                        missing_dict[module_name]['functions'][name]['missing_docstring'] = True
                        f.write(f"Missing Docstring for function '{name}', in module '{module.__name__.split('.')[-1]}', with path '{module_path}'\n\n")
            yield module_path, module


def get_missing_method_docstring(modules):
    global missing_dict
    with open('missing_methods_docstrings.txt', 'w') as f:
        for module_path, module in modules:
            module_name = module.__name__.split('.')[-1]
            for name, _object in getmembers(module, predicate=isclass):
                if _object.__module__ == module.__name__:
                    for meth_name, meth_object in getmembers(_object, predicate=isfunction):
                        if not meth_name.startswith('__') and not meth_name.endswith('__'):
                            missing_dict[module_name]['classes'][name]['methods'][meth_name] = {'missing_docstring': False}
                            if meth_object.__doc__ is None:
                                missing_dict[module_name]['classes'][name]['methods'][meth_name]['missing_docstring'] = True
                                f.write(f"Missing Docstring for method '{meth_name}',in Class '{name}', in module '{module.__name__.split('.')[-1]}', with path '{module_path}'\n\n")
            yield module_path, module


def run(in_dir):
    print('files')
    m = get_files(in_dir)
    print("modules")
    m = get_missing_module_docstring(m)
    print("classes")
    m = get_missing_class_docstring(m)
    print('functions')
    m = get_missing_function_docstring(m)
    print('methods')
    m = get_missing_method_docstring(m)
    mx = list(m)
    print(len(mx))
    print('DONE')
    os.chdir(THIS_FILE_DIR)
    writejson(missing_dict, 'docstring_data.json')


run(MAIN_MODULE_DIR)
