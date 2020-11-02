import os
import re
import json
import matplotlib.pyplot as plt
from antistasi_serverlog_statistic.regex.regex_storage import DATE_FORMAT, META_REGEX
from datetime import datetime
INPUT_FOLDER = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistasi_ServerLog_Statistic\antistasi_serverlog_statistic\input\Antistasi_Community_Logs\Mainserver_1\Server"
LOG_PERF_REGEX = re.compile(r"(?P<ServerFPS>(?<=ServerFPS:)\d+(\.\d+)).*?(?P<Players>(?<=Players:)\d+).*?(?P<DeadUnits>(?<=DeadUnits:)\d+).*?(?P<AllUnits>(?<=AllUnits:)\d+).*?(?P<UnitsAwareOfEnemies>(?<=UnitsAwareOfEnemies:)\d+).*?(?P<AllVehicles>(?<=AllVehicles:)\d+).*?(?P<WreckedVehicles>(?<=WreckedVehicles:)\d+).*?(?P<Entities>(?<=Entities:)\d+).*?(?P<GroupsRebels>(?<=GroupsRebels:)\d+).*?(?P<GroupsInvaders>(?<=GroupsInvaders:)\d+).*?(?P<GroupsOccupants>(?<=GroupsOccupants:)\d+).*?(?P<GroupsCiv>(?<=GroupsCiv:)\d+).*?(?P<GroupsTotal>(?<=GroupsTotal:)\d+).*?(?P<GroupsCombatBehaviour>(?<=GroupsCombatBehaviour:)\d+).*?(?P<FactionCash>(?<=Faction Cash:)\d+).*?(?P<HR>(?<=HR:)\d+).*?")

TEST_FILE = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistasi_ServerLog_Statistic\antistasi_serverlog_statistic\input\Antistasi_Community_Logs\Mainserver_1\Server\arma3server_x64_2020-10-11_14-53-29.txt"


def player_to_attack_dict():
    _attack_list = []
    _player_list = []
    _out_rest = []
    _index = 0
    _out_dict = {'players': {}, 'attacks': {}}
    for _file in os.scandir(INPUT_FOLDER):
        with open(_file.path, 'r', errors='replace') as t_file:
            _lines = t_file.read().splitlines()

        for index, line in enumerate(_lines):
            _match = META_REGEX.search(line)
            if _match:
                g = _match.groupdict()
                _datetime_string = g['date'].strip() + '_' + g['time'].strip()
                _datetime = datetime.strptime(_datetime_string, DATE_FORMAT)
                _level = g['level']
                _function = g['function']
                _rest = g['rest']
                try:
                    if _function == 'rebelAttack' and _level == 'INFO' and 'Starting large attack' in line and 'aborting' not in _lines[index + 1] and 'suitable' not in _lines[index + 1] and 'could not find available' not in _lines[index + 1] and 'could not find available' not in _lines[index + 2]:
                        _attack_list.append(_datetime)
                        _out_dict['attacks'][_datetime.isoformat()] = _rest

                        _out_rest.append(line)
                        _index += 1
                    elif _function == 'fn_logPerformance':
                        _match_perf = LOG_PERF_REGEX.search(_rest)
                        if _match_perf:
                            _player_list.append((_datetime, _match_perf.groupdict()['Players']))
                            _out_dict['players'][_datetime.isoformat()] = int(_match_perf.groupdict()['Players'])
                except ValueError:
                    print('last')
    with open('players_vs_attack_data.json', 'w') as jf:
        json.dump(_out_dict, jf, indent='\t', sort_keys=False)
    with open('test.txt', 'w') as outresf:
        outresf.write('\n'.join(_out_rest))

    return (_player_list, _attack_list)


def graph_it():
    _player_list, _attack_list = player_to_attack_dict()
    x_a = []
    y_a = []
    for index, _date in enumerate(_attack_list):
        try:
            _minutes_one = _date
            _minutes_two = _attack_list[index + 1]
            _delta = (_minutes_two - _minutes_one)
            _delta = _delta.total_seconds() // 60
            if _delta < 250:
                x_a.append(_date)
                y_a.append(_delta)
        except IndexError:
            print('last one')

    print(len(x_a))
    print(len(y_a))
    x = []
    y = []
    for _date, value in _player_list:
        x.append(_date)
        y.append(int(value))
    # plt.style.use('ggplot')
    fig, ax = plt.subplots()

    ax.bar(x, y, width=0.001, color='green', alpha=0.25)
    ax.scatter(x_a, y_a, color='red', linewidths=0.1, marker='v')
    plt.show()


if __name__ == '__main__':
    graph_it()
