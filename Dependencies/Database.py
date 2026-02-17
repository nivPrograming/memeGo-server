import sqlite3
from hashlib import sha256
import random

from Models.data_base_types import *


class DataBase:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.db_con = sqlite3.connect(kwargs['name'])
        else:
            self.db_con = sqlite3.connect("tralaleo tralala.db")

        self.pepper = None
        #with open('../pepper.txt', 'rb') as f:
        #    self.pepper = f.read()

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
                        type INTEGER NOT NULL,
                        insertion_time TEXT NUT NULL
                    )
                ''')

        self.cursor.execute('''
                           CREATE TABLE IF NOT EXISTS users (
                               id INTEGER AUTO INCREMENT PRIMARY KEY,
                               email TEXT NOT NULL,
                               username TEXT NOT NULL,
                               psw_hash TEXT NOT NULL,
                               salt TEXT NOT NULL,
                               token TEXT NOT NULL
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
        self.cursor.execute("SELECT id, name, photo, rarity "
                            "FROM creature")

        data = self.cursor.fetchall()
        creatures = []
        for creature in data:
            creatures.append(Creature(creature[0], creature[1], creature[2], creature[3]))
        return creatures

    def insert_new_creature(self, creature: CreaturesInTheWild):
        self.cursor.execute("INSERT INTO creature_in_wild (geohash, lat, lon, resilience_points, type, insertion_time) "
                            "VALUES (?, ?, ?, ?, ?, DATETIME('now'))",
                            (creature.Geohash, creature.Lat, creature.Lon,
                             creature.Resilience_points, creature.Type))

        self.db_con.commit()


    def remove_old_creatures(self):
        minutes = 20
        self.cursor.execute(
            "DELETE FROM creature_in_wild WHERE insertion_time < datetime('now', ?)",
            (f"-{minutes} minutes",)
        )
        self.db_con.commit()

    def get_usr(self, email):
        self.cursor.execute(
            "SELECT id, email, username, psw_hash, salt, token FROM users "
            "WHERE email = ?", (email,)
        )

        usr = self.cursor.fetchall()

        if len(usr) == 0 or len(usr) > 1:
            return None

        return User(usr[0][0], usr[0][2], usr[0][1], usr[0][3], usr[0][4], usr[0][5])

    def login_usr_psw(self, email, psw):
        usr = self.get_usr(email)
        if usr is None:
            return -1

        hashed_psw = self._hash_psw(psw, usr.Salt)

        if hashed_psw != usr.Psw_hash:
            return -2

        return usr

    def login_usr_jwt(self, email, token):
        usr = self.get_usr(email)
        if usr is None:
            return -1

        if token != usr.Token:
            return -2

        return usr

    def _hash_psw(self, psw, salt):
        psw = psw.encode()
        psw += self.pepper + salt
        h = sha256()
        h.update(psw)
        return h.hexdigest()

    @staticmethod
    def gen_salt():
        return random.randbytes(10)
