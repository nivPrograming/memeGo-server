class User:
    def __init__(self, ID, username, email, psw_hash, salt, token):
        self.Id = ID
        self.Username = username
        self.Email = email
        self.Psw_hash = psw_hash
        self.Salt = salt
        self.Token = token


class Creature:
    def __init__(self, ID, name, photo, rarity):
        self.Id = ID
        self.name = name
        self.photo = photo
        self.Rarity = rarity


class CreaturesInTheWild:
    def __init__(self, ID, type_id, resilience_points, geohash, lon, lat):
        self.Id = ID
        self.Type = type_id
        self.Resilience_points = resilience_points
        self.Geohash = geohash
        self.Lon = lon
        self.Lat = lat


class CreaturesCaught:
    def __init__(self, ID, type_id, resilience_points, user_id):
        self.Id = ID
        self.Type = type_id
        self.Resilience_points = resilience_points
        self.User_id = user_id
