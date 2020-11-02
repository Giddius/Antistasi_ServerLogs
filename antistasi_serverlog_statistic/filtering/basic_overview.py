# region [Imports]

# * Standard Library Imports -->
import os
import sys
from datetime import datetime
# from collections import namedtuple

# * Third Party Imports -->
from antistasi_serverlog_statistic.utilities.misc import fix_unicode
from antistasi_serverlog_statistic.regex.regex_storage import RegexMachine
from antistasi_serverlog_statistic.filtering.latest_date import LatestDateKeeper

# * PyQt5 Imports -->

# * Gid Imports -->
# import gidlogger as glog
from antistasi_serverlog_statistic.utilities.misc import (pathmaker, writejson, linereadit, get_pickled)

# endregion[Imports]

__updated__ = '2020-11-01 16:27:10'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

# log = glog.aux_logger(__name__)
# log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

INPUT_DIR = pathmaker(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistasi_ServerLog_Statistic\antistasi_serverlog_statistic\input")
# TempTuple = namedtuple('TempTuple', ['date', 'time', 'level', 'function', 'rest'])
DATE_FORMAT = "%Y/%m/%d_%H:%M:%S"

# endregion[Constants]


class FileLogReader:
    def __init__(self, regexer: RegexMachine, date_keeper: LatestDateKeeper):
        self.regexer = regexer
        self.date_keeper = date_keeper
        self.directories = []
        self.files = {}
        self.datetime_template = "{year}-{month}-{day}_{hour}-{minute}-{second}"
        self.datetime_format = "%Y-%m-%d_%H-%M-%S"

    def add_directory(self, directory):
        directory = pathmaker(directory)
        if directory not in self.directories:
            self.directories.append(directory)
        else:
            raise FileExistsError(f'directory "{directory}" already in list of directories')

    def _date_from_filename(self, filename, directory):
        _regex = self.regexer[self.regexer.FilenameDateTimeRegex]
        _search_object = _regex.search(filename)
        if _search_object:
            _date_time_string = self.datetime_template.format(**_search_object.groupdict())
            _datetime = datetime.strptime(_date_time_string, self.datetime_format)
            return self.date_keeper.check_is_newer_date(directory, _datetime), _datetime

    def find_files(self):
        for _directory in self.directories:
            _directory = pathmaker(_directory)
            _reduce_directory = os.path.basename(_directory)
            self.files[_reduce_directory] = []
            for _file in os.scandir(pathmaker(_directory, 'Server')):
                is_newer, _new_date = self._date_from_filename(_file.name, _reduce_directory)
                if _file.name.startswith('arma3server') and is_newer is True:
                    self.files[_reduce_directory].append((_file.path, _new_date))

    def get_line(self, directory):
        directory = directory if '/' not in pathmaker(directory) else os.path.basename(directory)
        for _file, _date in self.files[directory]:
            for _line in linereadit(_file, in_errors='replace'):
                _line = fix_unicode(_line)
                yield _line
            self.date_keeper.pickle_date(directory, _date)


if __name__ == '__main__':
    _list = []
    a = RegexMachine()
    c = LatestDateKeeper()
    b = FileLogReader(a, c)

    b.add_directory(pathmaker(sys.argv[1]))
    b.find_files()
    _re = a[a.LineCombinedRegex]
    for line in b.get_line('Mainserver_1'):
        _match = _re.search(line)
        if _match:
            x = _match.groupdict()
            x['message'] = x['message'].split('"')[0]
            x['time'] = x['time'].replace(' ', "0")

            _list.append(x)
    last_date = get_pickled(f'{os.path.basename(pathmaker(sys.argv[1]))}_latest_date.pkl').strftime("%Y-%m-%d_%H-%M-%S")
    writejson(_list, f'logs_until_[{last_date}].json', sort_keys=False, indent=2)
    print(len(_list))
