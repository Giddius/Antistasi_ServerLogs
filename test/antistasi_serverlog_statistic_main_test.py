from antistasi_serverlog_statistic.antistasi_serverlog_statistic_main import filter_logs
import pytest

TEST_LOG_SNIPPET = """13:07:50 "5568.37: [Antistasi] | ERROR | initVarCommon.sqf | Stuck on compiling missionPath, re-launch the mission. | (R) R logistics 200:2 (Lewis)"
13:07:50 "5568.91: [Antistasi] | DEBUG | fn_assignBossIfNone | Not attempting to assign new boss - player R Fox Command LR77:1 (Tyler) REMOTE is the boss"
13:07:51 "5569.84: [Antistasi] | DEBUG | fn_punishment_FF_addEH.sqf | Punishment Event Handlers Added to: Lewis"
13:07:52 "5571.39: [Antistasi] | INFO | fn_logPerformance |  ServerFPS:15.7947, Players:34, DeadUnits:236, AllUnits:181, UnitsAwareOfEnemies:45, AllVehicles:302, WreckedVehicles:16, Entities:634, GroupsRebels:79, GroupsInvaders:1, GroupsOccupants:56, GroupsCiv:14, GroupsTotal:150, GroupsCombatBehaviour:28, Faction Cash:29765, HR:297"
13:07:53 ["_open arsenal for: clientOwner ",26]"""


def test_filter_logs():
    assert filter_logs(TEST_LOG_SNIPPET) == {
        'INFO': [('13:07:52', 'fn_logPerformance', ' ServerFPS:15.7947, Players:34, DeadUnits:236, AllUnits:181, UnitsAwareOfEnemies:45, AllVehicles:302, WreckedVehicles:16, Entities:634, GroupsRebels:79, GroupsInvaders:1, GroupsOccupants:56, GroupsCiv:14, GroupsTotal:150, GroupsCombatBehaviour:28, Faction Cash:29765, HR:297"', '"5571.39: [Antistasi] | INFO | fn_logPerformance |  ServerFPS:15.7947, Players:34, DeadUnits:236, AllUnits:181, UnitsAwareOfEnemies:45, AllVehicles:302, WreckedVehicles:16, Entities:634, GroupsRebels:79, GroupsInvaders:1, GroupsOccupants:56, GroupsCiv:14, GroupsTotal:150, GroupsCombatBehaviour:28, Faction Cash:29765, HR:297"')],
        'ERROR': [('13:07:50', '"5568.37: [Antistasi] | ERROR | initVarCommon.sqf | Stuck on compiling missionPath, re-launch the mission. | (R) R logistics 200:2 (Lewis)"')],
        'DEBUG': [('13:07:50', '"5568.91: [Antistasi] | DEBUG | fn_assignBossIfNone | Not attempting to assign new boss - player R Fox Command LR77:1 (Tyler) REMOTE is the boss"'), ('13:07:51', '"5569.84: [Antistasi] | DEBUG | fn_punishment_FF_addEH.sqf | Punishment Event Handlers Added to: Lewis"')],
        'else': ['13:07:53 ["_open arsenal for: clientOwner ",26]']
    }
