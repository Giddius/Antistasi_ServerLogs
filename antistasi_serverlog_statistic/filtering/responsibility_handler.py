import os
import re
from gidtools.gidfiles import pathmaker, loadjson, writejson, writeit, readit, linereadit, appendwriteit, QuickFile, pickleit, get_pickled, readbin
from antistasi_serverlog_statistic.regex.regex_storage import RegexMachine
from datetime import datetime
from collections import namedtuple


Linetuple = namedtuple('Linetuple', ['datetime', 'rest'])


class BaseResponsibilityHandler:
    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    def handle(self, line_match_result):
        if self._next_handler:
            return self._next_handler.handle(line_match_result)

        return None


class FunctionHandler(BaseResponsibilityHandler):
    def __init__(self, function_identifier):
        self.function_identifier = function_identifier
        self.clean_func_name = self.function_identifier.replace('.', '').replace('_', '').replace(' ', '').title()
        self.lines = {}
        self.linetuple = namedtuple(self.clean_func_name.title() + 'LineTuple', ['datetime', 'rest'])

    def handle(self, line_match_result: namedtuple):
        if line_match_result.function == self.function_identifier:
            _level = line_match_result.level
            if _level not in self.lines:
                self.lines[_level] = []
            self.lines[_level].append(self.linetuple(line_match_result.date + '_' + line_match_result.time, line_match_result.rest))
        else:
            return super().handle(line_match_result)
