from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)
from timeit import Timer
from datetime import datetime


def pickle_test():
    _datetime = datetime.now()
    pickleit(_datetime, 'pickle_test.pkl')
    x = get_pickled('pickle_test.pkl')


def write_test():
    _datetime = datetime.now()
    with open('write_test.txt', 'w') as ftes:
        ftes.write(str(_datetime))
    with open('write_test.txt', 'r') as fre:
        x = fre.read()


def json_test():
    _datetime = datetime.now()
    writejson(str(_datetime), 'json_test.json')
    x = loadjson('json_test.json')


if __name__ == '__main__':
    n = 100000
    Tp = Timer(pickle_test)
    Tw = Timer(write_test)
    Tj = Timer(json_test)
    rp = Tp.timeit(n)
    rw = Tw.timeit(n)
    rj = Tj.timeit(n)
    with open('results.txt', 'w') as resf:
        resf.write('pickel: \n' + str(rp / n) + '\n###########\n\n')
        resf.write('write: \n' + str(rw / n) + '\n###########\n\n')
        resf.write('json: \n' + str(rj / n) + '\n###########\n\n')
