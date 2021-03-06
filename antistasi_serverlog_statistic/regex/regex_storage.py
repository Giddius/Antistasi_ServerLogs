import re
import textwrap


class RegexMachine:
    LineDateRegex = 'line_date_regex'
    LineTimeRegex = 'line_time_regex'
    LineLevelRegex = 'line_level_regex'
    LineFunctionRegex = 'line_function_regex'
    LineRestRegex = 'line_rest_regex'
    FilenameDateTimeRegex = 'filename_datetime_regex'
    LineCombinedRegex = 'line_combined_regex'

    def __init__(self):

        self.raw_regexes = {
            "raw_line_date_regex": r"(?P<year>\d\d\d\d).(?P<month>\d\d).(?P<day>\d\d).*?",
            "raw_line_time_regex": r"(?P<hour>[012\s]?\d).(?P<minute>[0123456]\d).(?P<second>[0123456]\d)",
            "raw_line_level_regex": r"(?P<level>(?<=\|\s)[A-Z0-9][A-Z0-9]+(?=\\|))",
            "raw_line_function_regex": r"(?P<function>(?<=\s\|\s)\w+(\.\w+)?(?=\s\|\s))",
            "raw_line_rest_regex": r".*?(?P<message>(?<=\|\s).*)",
            "raw_filename_datetime_regex": textwrap.dedent(r'''
                                                    (?P<year>\d\d\d\d)
                                                    .*?
                                                    (?P<month>[01]\d)
                                                    .*?
                                                    (?P<day>[0123]\d)
                                                    .*?
                                                    (?P<hour>[012]\d)
                                                    .*?
                                                    (?P<minute>[0-6]\d)
                                                    .*?
                                                    (?P<second>[0-6]\d)
                                                    '''),
        }
        self.compiled_regexes = {}
        self.combined_line_regex = None
        self.combined_date_time_regex = None
        self._compile_all()

    def _compile_all(self):
        self.compiled_regexes = {}
        for key, value in self.raw_regexes.items():
            key = key.replace('raw_', '')
            self.compiled_regexes[key] = re.compile(value, re.VERBOSE)
        self.make_combine_line_regex()
        self.make_combine_date_time_regex()

    def __setitem__(self, key, value):
        key = 'raw_' + key
        self.raw_regexes[key] = value
        self._compile_all()

    def __getitem__(self, key):
        return self.compiled_regexes[key]

    def make_combine_line_regex(self):
        _comb = []
        for key, value in self.raw_regexes.items():
            if '_line_' in key:
                _comb.append(value)
        self.combined_line_regex = re.compile('.*?'.join(_comb), re.VERBOSE)

    def make_combine_date_time_regex(self):
        self.combined_date_time_regex = re.compile(r"^" + self.raw_regexes["raw_line_date_regex"] + self.raw_regexes["raw_line_time_regex"])
