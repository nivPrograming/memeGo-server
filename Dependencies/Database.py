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
                        geohash TEXT NOT NULL,
                        lat REAL NOT NULL,
                        lon REAL NOT NULL,
                        resilience_points INTEGER NOT NULL,
                        type INTEGER NOT NULL
                    )
                ''')

    def get_creatures_in_geohash(self, gh):
        self.cursor.execute("SELECT geohash, lat, lon, resilience_points, type "
                            "FROM creature_in_wild where geohash=?", (gh,))

        data = self.cursor.fetchall()
        creatures = []
        for creature in data:
            creatures.append(CreaturesInTheWild(creature[4], creature[3], creature[0],
                                                creature[1], creature[2]))
        return creatures

    def get_creature_types(self):
        self.cursor.execute("SELECT id, name, photo, rarity"
                            "FROM creature")

        data = self.cursor.fetchall()
        creatures = []
        for creature in data:
            creatures.append(Creature(creature[0], creature[1], creature[2], creature[3]))
        return creatures

    def insert_new_creature(self, creature: CreaturesInTheWild):
        self.cursor.execute("INSERT INTO creature_in_wild (geohash, lat, lon, resilience_points, type)"
                            "VALUES (?, ?, ?, ?, ?",
                            (creature.Geohash, creature.Lat, creature.Lon,
                             creature.Resilience_points, creature.Type))

        self.db_con.commit()
