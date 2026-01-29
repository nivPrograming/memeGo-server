import pygeohash as pgh
from geopy.distance import great_circle, geodesic

from Dependencies.Database import DataBase
from Models.data_base_types import *
import random
import math


class CreatureManager:
    def __init__(self):
        self.db = DataBase()

    def find_creatures_around(self, lat, lon, r):
        creatures = []
        player_gh = pgh.encode(lat, lon, 7)
        neighbors = self._geohash_neighbors(player_gh)

        creatures += self.db.get_creatures_in_geohash(player_gh)
        creatures += self.db.get_creatures_in_geohash(neighbors['n'])
        creatures += self.db.get_creatures_in_geohash(neighbors['s'])
        creatures += self.db.get_creatures_in_geohash(neighbors['e'])
        creatures += self.db.get_creatures_in_geohash(neighbors['w'])
        creatures += self.db.get_creatures_in_geohash(neighbors['ne'])
        creatures += self.db.get_creatures_in_geohash(neighbors['nw'])
        creatures += self.db.get_creatures_in_geohash(neighbors['se'])
        creatures += self.db.get_creatures_in_geohash(neighbors['sw'])

        creatures_in_distance = []

        for creature in creatures:
            if great_circle((creature.lat, creature.lon), (lat, lon)).meters <= r:
                creatures_in_distance.append(creature)

        return creatures_in_distance

    def gen_new_creatures(self, locations):
        """
        generates new creatures a round players
        :param locations: known locations of active users
        :return: new creatures in data_base
        """
        types = self.db.get_creature_types()

        for usr in locations:
            existing_creatures = self.find_creatures_around(usr[0], usr[1], 600)

            missing_c = max(0, 8 - len(existing_creatures))
            for i in range(missing_c):
                c = self._gen_random_creature(usr[0], usr[1], 600, types)
                self.db.insert_new_creature(c)

    @staticmethod
    def _gen_random_creature(lat, lon, r, types):
        c_type = random.choices(types, weights=[i.Rarity for i in types], k=1)[0]
        resilience_points = random.randrange(0, (10 - c_type.Rarity) * 1000)

        distance = math.sqrt(random.random()) * r
        bearing = random.uniform(0, 360)

        destination = geodesic(meters=distance).destination((lat, lon), bearing)

        gh = pgh.encode(destination.latitude, destination.longitude, precision=7)

        return CreaturesInTheWild(c_type, resilience_points, gh, destination.latitude, destination.longitude)

    @staticmethod
    def _geohash_neighbors(gh):
        north = pgh.get_adjacent(gh, "top")
        south = pgh.get_adjacent(gh, "bottom")
        east = pgh.get_adjacent(gh, "right")
        west = pgh.get_adjacent(gh, "left")

        return {
            "n": north,
            "s": south,
            "e": east,
            "w": west,
            "ne": pgh.get_adjacent(north, "right"),
            "nw": pgh.get_adjacent(north, "left"),
            "se": pgh.get_adjacent(south, "right"),
            "sw": pgh.get_adjacent(south, "left"),
        }

