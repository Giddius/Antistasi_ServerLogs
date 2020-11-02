import os
import shutil
# from gidtools.gidfiles import pathmaker
import re
from datetime import datetime
example = "arma3server_x64_2020-10-04_02-09-56"
INPUT_FOLDER = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistasi_ServerLog_Statistic\antistasi_serverlog_statistic\input"
date_format = "%Y-%m-%d_%H-%M-%S"
MIN_DATETIME = datetime.strptime("2020-10-04_01-01-01", date_format)


def find_old_logs():
    for dirname, folderlist, filelist in os.walk(INPUT_FOLDER):
        for _file in filelist:
            _filename, _ext = _file.split('.')
            _time = _filename.split('_')[-1]
            _date = _filename.split('_')[-2]
            _date_time = _date + '_' + _time
            _as_datetime = datetime.strptime(_date_time, date_format)
            if _as_datetime < MIN_DATETIME:
                yield os.path.join(dirname, _file)


def del_old_ones():
    for _path in find_old_logs():
        os.remove(_path)


if __name__ == '__main__':
    del_old_ones()
