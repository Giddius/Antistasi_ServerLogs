# region [Imports]

# * Standard Library Imports -->
import os

# * Third Party Imports -->

# * PyQt5 Imports -->
# * Gid Imports -->
# import gidlogger as glog
from antistasi_serverlog_statistic.utilities.misc import (pickleit, pathmaker, get_pickled)


# endregion[Imports]

__updated__ = '2020-11-01 16:27:15'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

# log = glog.aux_logger(__name__)
# log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class LatestDateKeeper:
    def __init__(self, save_folder=None):
        self.dates = {}
        self.save_folder = os.getcwd() if save_folder is None else save_folder

    @staticmethod
    def _make_pickle_name(identifier):
        return identifier + '_latest_date.pkl'

    def pickle_date(self, identifier, date):
        _name = self._make_pickle_name(identifier)
        pickleit(date, pathmaker(self.save_folder, _name))
        self.dates[identifier] = date

    def retrieve_pickled_date(self, identifier):
        _name = self._make_pickle_name(identifier)
        _path = pathmaker(self.save_folder, _name)
        if os.path.isfile(_path) is True:
            _out = get_pickled(pathmaker(self.save_folder, _name))
        else:
            _out = None
        return _out

    def check_is_newer_date(self, identifier, new_date):
        _old_date = self.dates.get(identifier, self.retrieve_pickled_date(identifier))
        return _old_date is None or new_date > _old_date


if __name__ == '__main__':
    pass
