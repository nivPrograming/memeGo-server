import pygeohash as pgh
from geopy.distance import great_circle
import sqlite3
from Models.data_base_types import *



class DataBase:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.db_con = sqlite3.connect(kwargs['name'])
        else:
            self.db_con = sqlite3.connect("tralaleo tralala.db")

        self.pepper = None
        with open('pepper.txt', 'rb') as f:
            self.pepper = f.read()

        self.cursor = self.db_con.cursor()

        self._gen_tables()

    def _gen_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS creature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rarity INTEGER NOT NULL,
                photo BLOB NOT NULL
            )
        ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS creature_in_wild (
                        id INTEGER PRIMARY KEY,
                        geohash TEXT NOT NULL,
                        lon REAL NOT NULL,
                        lat REAL NOT NULL,
                        resilience_points INTEGER NOT NULL,
                        type INTEGER NOT NULL
                    )
                ''')

    def get_creatures_in_geohash(self, gh):
        self.cursor.execute("SELECT id, geohash, lon, lat, resilience_points, type "
                            "FROM creature_in_wild where geohash=?", (gh,))

        data = self.cursor.fetchall()
        creatures = []
        for creature in data:
            creatures.append(CreaturesInTheWild(creature[0], creature[5], creature[4],
                                                creature[1], creature[2], creature[3]))
        return creatures

    def find_creatures_around(self, lat, lon, r):
        creatures = []
        player_gh = pgh.encode(lat, lon, 7)
        neighbors = self._geohash_neighbors(player_gh)

        creatures += self.get_creatures_in_geohash(player_gh)
        creatures += self.get_creatures_in_geohash(neighbors['n'])
        creatures += self.get_creatures_in_geohash(neighbors['s'])
        creatures += self.get_creatures_in_geohash(neighbors['e'])
        creatures += self.get_creatures_in_geohash(neighbors['w'])
        creatures += self.get_creatures_in_geohash(neighbors['ne'])
        creatures += self.get_creatures_in_geohash(neighbors['nw'])
        creatures += self.get_creatures_in_geohash(neighbors['se'])
        creatures += self.get_creatures_in_geohash(neighbors['sw'])

        creatures_in_distance = []

        for creature in creatures:
            if great_circle((creature.lat, creature.lon), (lat, lon)).meters <= r:
                creatures_in_distance.append(creature)

        return creatures_in_distance

    @staticmethod
    def _geohash_neighbors(gh):
        north = pgh.get_adjacent(gh, "n")
        south = pgh.get_adjacent(gh, "s")
        east = pgh.get_adjacent(gh, "e")
        west = pgh.get_adjacent(gh, "w")

        return {
            "n": north,
            "s": south,
            "e": east,
            "w": west,
            "ne": pgh.get_adjacent(north, "e"),
            "nw": pgh.get_adjacent(north, "w"),
            "se": pgh.get_adjacent(south, "e"),
            "sw": pgh.get_adjacent(south, "w"),
        }



