import json
from os import path
from statsnba import config


class MockLoader(object):
    def get_boxscore(self):
        return 0

    def get_playbyplay(self):
        return 0


class MongoLoader(object):

    def __init__(self):
        from pymongo import MongoClient
        self._db = MongoClient(config['mongodb']['uri'])[config['mongodb']['database']]

    def get_boxscore(self, game_id):
        return self._db.boxscoretraditionalv2.find_one({'parameters.GameID': game_id})

    def get_playbyplay(self, game_id):
        return self._db.playbyplay.find_one({'parameters.GameID': game_id})


class FsLoader(object):

    def __init__(self):
        pass

    def get_boxscore(self, game_id):
        file_path = path.join(path.abspath(__file__), '../../', config['data']['development'], 'boxscores/boxscore_%s.json' % game_id)
        return json.load(open(file_path, 'r'))

    def get_playbyplay(self, game_id):
        file_path = path.join(path.abspath(__file__), '../../', config['data']['development'], 'playbyplays/playbyplay_%s.json' % game_id)
        return json.load(open(file_path, 'r'))


class WebLoader(object):
    def __init__(self):
        pass

    def get_boxscore(self, game_id):
        from statsnba.resources import StatsNBABoxscore
        return StatsNBABoxscore.fetch_resource({'GameID': game_id})

    def get_playbyplay(self, game_id):
        from statsnba.resources import StatsNBAPlayByPlay
        return StatsNBAPlayByPlay.fetch_resource({'GameID': game_id})
