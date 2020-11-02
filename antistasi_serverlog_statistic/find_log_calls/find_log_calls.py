# region [Imports]

# * Standard Library Imports -->
import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import logging
import platform
import subprocess
from enum import Enum, Flag, auto
from time import sleep
from pprint import pprint, pformat
from typing import Union
from datetime import tzinfo, datetime, timezone, timedelta
from functools import wraps, lru_cache, singledispatch, total_ordering, partial
from contextlib import contextmanager
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import regex
# * Third Party Imports -->
# import requests
# import pyperclip
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from github import Github, GithubException
# from jinja2 import BaseLoader, Environment
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process

# * PyQt5 Imports -->
# from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator
# from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
#                           QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)
# from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox,
#                              QGroupBox, QLineEdit, QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog,
#                              QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton,
#                              QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage, QApplication, QButtonGroup, QRadioButton,
#                              QFontComboBox, QStackedWidget, QListWidgetItem, QTreeWidgetItem, QDialogButtonBox, QAbstractItemView,
#                              QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator, QAction, QSystemTrayIcon)
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file, QuickFile)

from antistasi_serverlog_statistic.utilities.misc import fix_unicode
# endregion[Imports]

__updated__ = '2020-11-02 17:18:44'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

ANTISTASI_FOLDER = pathmaker(r"D:\Dropbox\hobby\Modding\Programs\Github\Foreign_Repos\A3-Antistasi")

LOG_REGEX = r"(?<=.*?)\[[^;]*?(?!\n\n)\]\scall A3A_fnc_log"
AMOUNT_REGEX = re.compile(r"A3A_fnc_log")

# endregion[Constants]


def find_files():
    for dirname, folderlist, filelist in os.walk(ANTISTASI_FOLDER):
        for _file in filelist:
            if _file.endswith('.sqf') and 'Navigation' not in dirname:
                yield pathmaker(dirname, _file)


def read_files():
    for _path in find_files():
        try:
            _content = readit(_path)
            yield (_path, _content)
        except UnicodeDecodeError as error:
            print(_path + ' ---> ' + str(error))
            yield(_path, "")


def get_line_number(target, line_list):
    for index, line in line_list:
        if len(target.splitlines()) > 1:
            if target.splitlines()[-1] in line:
                return index + 1
        else:
            if target in line:
                return index + 1


def find_log_calls(in_tup):
    _out_list = []

    path, content = in_tup
    _amount = len(AMOUNT_REGEX.findall(content))
    _line_list = [(index, line) for index, line in enumerate(content.splitlines())]
    _result = regex.findall(LOG_REGEX, content, re.DOTALL, overlapped=True)
    print("searched: " + path)
    if _result:

        _result = sorted(_result, key=len)
        for i in range(_amount):
            try:
                _number = get_line_number(_result[i], _line_list)
                _out_list.append(str(_result[i]) + ' \n-# Line Number: ' + str(_number))
            except IndexError:
                appendwriteit('error.txt', path + ' +++++++ ' + pformat(_result))
        return path, _out_list
    else:
        return path, None


# region[Main_Exec]
if __name__ == '__main__':
    if os.path.isfile('test.txt'):
        os.remove('test.txt')

    _fin = map(find_log_calls, read_files())
    print("################################################ finished searching ################################################")

    for _path, result in _fin:
        if result:
            _path = _path.replace('D:/Dropbox/hobby/Modding/Programs/Github/Foreign_Repos/', '')
            appendwriteit('test.txt', f"\n\n\n\n#######################################\n{_path} ----->\n\n")
            for item in result:
                appendwriteit('test.txt', str(item) + '\n\n-------------------\n')


# endregion[Main_Exec]
