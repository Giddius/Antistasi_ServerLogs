import re
import os
import json
import sys

INPUT_FOLDER = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistasi_ServerLog_Statistic\antistasi_serverlog_statistic\input\Antistasi_Community_Logs\Mainserver_1\Server"
REGEX = re.compile(r"(?P<date>\d\d\d\d.\d\d.\d\d).*?(?P<time>[012\s]?\d.[0123456]\d.[0123456]\d).*?(?P<level>(?<=\s\|\s)\w+(?=\s\|\s)).*?(?P<function>(?<=\s\|\s)\w+(?=\s\|\s)).*?(?P<ServerFPS>(?<=ServerFPS:)\d+(\.\d+)).*?(?P<Players>(?<=Players:)\d+).*?(?P<DeadUnits>(?<=DeadUnits:)\d+).*?(?P<AllUnits>(?<=AllUnits:)\d+).*?(?P<UnitsAwareOfEnemies>(?<=UnitsAwareOfEnemies:)\d+).*?(?P<AllVehicles>(?<=AllVehicles:)\d+).*?(?P<WreckedVehicles>(?<=WreckedVehicles:)\d+).*?(?P<Entities>(?<=Entities:)\d+).*?(?P<GroupsRebels>(?<=GroupsRebels:)\d+).*?(?P<GroupsInvaders>(?<=GroupsInvaders:)\d+).*?(?P<GroupsOccupants>(?<=GroupsOccupants:)\d+).*?(?P<GroupsCiv>(?<=GroupsCiv:)\d+).*?(?P<GroupsTotal>(?<=GroupsTotal:)\d+).*?(?P<GroupsCombatBehaviour>(?<=GroupsCombatBehaviour:)\d+).*?(?P<FactionCash>(?<=Faction Cash:)\d+).*?(?P<HR>(?<=HR:)\d+).*?")


def loadjson(in_file):
    with open(in_file, 'r') as jsonfile:
        _out = json.load(jsonfile)
    return _out


def writejson(in_object, in_file, sort_keys=True, indent=0):
    with open(in_file, 'w') as jsonoutfile:
        json.dump(in_object, jsonoutfile, sort_keys=sort_keys, indent=indent)


def find_files():
    for dirname, folderlist, filelist in os.walk():
        for _file in filelist:
            if os.path.isfile(_file.path) and _file.name.startswith('arma3server'):
                yield os.path.basename(os.path.dirname(dirname)), os.path.join(dirname, _file)


def get_lines():
    for _server, _file in find_files():
        with open(_file, 'r', errors='replace', encoding='utf-8') as in_file:
            _content = in_file.read().splitlines()
            for line in _content:
                yield _server, line


def get_data():
    if os.path.isfile('fn_logperformance.json') is False:
        writejson({}, 'fn_logperformance.json')
    _json_dict = loadjson('fn_logperformance.json')
    for _server, line in get_lines():
        if _server not in _json_dict:
            _json_dict[_server] = []
        _result = REGEX.search(line)
        if _result:
            _json_dict[_server].append(_result.groupdict())
    writejson(_json_dict, 'fn_logperformance.json')


if __name__ == '__main__':
    with open('fn_logperformance.json', 'w') as json_file:
        json.dump(get_data(), json_file, indent=2, sort_keys=False)
