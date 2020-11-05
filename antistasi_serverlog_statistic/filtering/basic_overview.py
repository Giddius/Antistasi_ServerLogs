# region [Imports]

# * Standard Library Imports -->
import os
import sys
from datetime import datetime
import re
import argparse
# from collections import namedtuple

# * Third Party Imports -->
from antistasi_serverlog_statistic.utilities.misc import fix_unicode
from antistasi_serverlog_statistic.regex.regex_storage import RegexMachine
from antistasi_serverlog_statistic.filtering.latest_date import LatestDateKeeper

# * PyQt5 Imports -->

# * Gid Imports -->
# import gidlogger as glog
from antistasi_serverlog_statistic.utilities.misc import (pathmaker, writejson, linereadit, get_pickled, loadjson)

# endregion[Imports]

__updated__ = '2020-11-05 13:14:41'

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
fn_logperformance_regex = re.compile(r"(?P<date>\d\d\d\d.\d\d.\d\d).*?(?P<time>[012\s]?\d.[0123456]\d.[0123456]\d).*?(?P<level>(?<=\s\|\s)\w+(?=\s\|\s)).*?(?P<function>(?<=\s\|\s)\w+(?=\s\|\s)).*?(?P<ServerFPS>(?<=ServerFPS:)\d+(\.\d+)).*?(?P<Players>(?<=Players:)\d+).*?(?P<DeadUnits>(?<=DeadUnits:)\d+).*?(?P<AllUnits>(?<=AllUnits:)\d+).*?(?P<UnitsAwareOfEnemies>(?<=UnitsAwareOfEnemies:)\d+).*?(?P<AllVehicles>(?<=AllVehicles:)\d+).*?(?P<WreckedVehicles>(?<=WreckedVehicles:)\d+).*?(?P<Entities>(?<=Entities:)\d+).*?(?P<GroupsRebels>(?<=GroupsRebels:)\d+).*?(?P<GroupsInvaders>(?<=GroupsInvaders:)\d+).*?(?P<GroupsOccupants>(?<=GroupsOccupants:)\d+).*?(?P<GroupsCiv>(?<=GroupsCiv:)\d+).*?(?P<GroupsTotal>(?<=GroupsTotal:)\d+).*?(?P<GroupsCombatBehaviour>(?<=GroupsCombatBehaviour:)\d+).*?(?P<FactionCash>(?<=Faction Cash:)\d+).*?(?P<HR>(?<=HR:)\d+).*?")

# endregion[Constants]


def get_log_performance(in_line_provider):
    if os.path.isfile('fn_logperformance.json') is False:
        writejson({}, 'fn_logperformance.json')
    _json_dict = loadjson('fn_logperformance.json')
    for _folder, _line in in_line_provider.get_line():
        if _folder not in _json_dict:
            _json_dict[_folder] = {}
        _result = fn_logperformance_regex.search(_line)
        if _result:
            _out = _result.groupdict()
            _date = _out['date']
            _time = _out['time'].replace(' ', '0')
            _date_time = _date + '_' + _time
            del _out['date']
            del _out['time']
            _json_dict[_folder][_date_time] = _out

    writejson(_json_dict, 'fn_logperformance.json', indent=2, sort_keys=False)


class FileLogReader:
    def __init__(self, base_dir, regexer: RegexMachine, date_keeper: LatestDateKeeper):
        self.base_dir = base_dir
        self.regexer = regexer
        self.date_keeper = date_keeper
        self.directories = []
        self.files = {}
        self.datetime_template = "{year}-{month}-{day}_{hour}-{minute}-{second}"
        self.datetime_format = "%Y-%m-%d_%H-%M-%S"

    def find_folders(self):
        for dirname, folderlist, filelist in os.walk(self.base_dir):
            for _folder in folderlist:
                if _folder != 'Server':
                    self.directories.append(pathmaker(dirname, _folder))

    def _date_from_filename(self, filename, directory):
        _regex = self.regexer[self.regexer.FilenameDateTimeRegex]
        _search_object = _regex.search(filename)
        if _search_object:
            _date_time_string = self.datetime_template.format(**_search_object.groupdict())
            _datetime = datetime.strptime(_date_time_string, self.datetime_format)
            return self.date_keeper.check_is_newer_date(directory, _datetime), _datetime

    def find_files(self):
        self.find_folders()
        for _directory in self.directories:
            _directory = pathmaker(_directory)
            _reduce_directory = os.path.basename(_directory)
            self.files[_reduce_directory] = []
            for _file in os.scandir(pathmaker(_directory, 'Server')):
                if os.path.isfile(_file.path):
                    is_newer, _new_date = self._date_from_filename(_file.name, _reduce_directory)
                    if _file.name.startswith('arma3server') and is_newer is True:
                        self.files[_reduce_directory].append((_file.path, _new_date))

    def get_line(self):
        for _folder, _value in self.files.items():
            for _file, _date in _value:
                for _line in linereadit(_file, in_errors='replace'):
                    _line = fix_unicode(_line)
                    yield _folder, _line
                self.date_keeper.pickle_date(_folder, _date)


def run_fn_log_parser():
    parser = argparse.ArgumentParser(description='parses fn_logperformance out of all logs from nested folders inside a main folder')
    parser.add_argument('-i', '--input', dest='in_put', type=str, required=True, help="the main folder ie: 'D:\Antistasi_Community_Logs")
    parser.add_argument('-o', '--outfile', type=str, required=False, help="the output folder, the pickles and the final json will be saved there", default=os.getcwd())
    args = parser.parse_args()
    a = RegexMachine()
    c = LatestDateKeeper(save_folder=args.outfile)
    b = FileLogReader(args.in_put, a, c)

    b.find_files()
    get_log_performance(b)
    print('done')
