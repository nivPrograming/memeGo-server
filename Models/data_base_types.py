import json
import base64


class User:
    def __init__(self, ID, username, email, psw_hash, salt):
        self.Id = ID
        self.Username = username
        self.Email = email
        self.Psw_hash = psw_hash
        self.Salt = salt

    def to_bytes(self):
        """Convert User to JSON bytes for network transmission"""
        data = {
            'id': self.Id,
            'username': self.Username,
            'email': self.Email,
            'psw_hash': base64.b64encode(self.Psw_hash).decode('utf-8'),
            'salt': base64.b64encode(self.Salt).decode('utf-8'),
        }
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def from_bytes(data):
        """Reconstruct User from JSON bytes"""
        obj = json.loads(data.decode('utf-8'))
        return User(
            obj['id'],
            obj['username'],
            obj['email'],
            base64.b64decode(obj['psw_hash']),
            base64.b64decode(obj['salt']),
        )


class Creature:
    def __init__(self, ID, name, photo, rarity):
        self.Id = ID
        self.Name = name
        self.Photo = photo
        self.Rarity = rarity

    def to_bytes(self):
        """Convert Creature to JSON bytes for network transmission"""
        data = {
            'id': self.Id,
            'name': self.Name,
            'photo': self.Photo,
            'rarity': self.Rarity
        }
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def from_bytes(data):
        """Reconstruct Creature from JSON bytes"""
        obj = json.loads(data.decode('utf-8'))
        return Creature(
            obj['id'],
            obj['name'],
            obj['photo'],
            obj['rarity']
        )


class CreaturesInTheWild:
    def __init__(self, type_id, resilience_points, geohash, lat, lon):
        self.Type = type_id
        self.Resilience_points = resilience_points
        self.Geohash = geohash
        self.Lat = lat
        self.Lon = lon

    def to_bytes(self):
        """Convert CreaturesInTheWild to JSON bytes for network transmission"""
        data = {
            'type': self.Type,
            'resilience_points': self.Resilience_points,
            'geohash': self.Geohash,
            'lat': self.Lat,
            'lon': self.Lon
        }
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def from_bytes(data):
        """Reconstruct CreaturesInTheWild from JSON bytes"""
        obj = json.loads(data.decode('utf-8'))
        return CreaturesInTheWild(
            obj['type'],
            obj['resilience_points'],
            obj['geohash'],
            obj['lat'],
            obj['lon']
        )


class CreaturesCaught:
    def __init__(self, ID, type_id, resilience_points, user_id):
        self.Id = ID
        self.Type = type_id
        self.Resilience_points = resilience_points
        self.User_id = user_id

    def to_bytes(self):
        """Convert CreaturesCaught to JSON bytes for network transmission"""
        data = {
            'id': self.Id,
            'type': self.Type,
            'resilience_points': self.Resilience_points,
            'user_id': self.User_id
        }
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def from_bytes(data):
        """Reconstruct CreaturesCaught from JSON bytes"""
        obj = json.loads(data.decode('utf-8'))
        return CreaturesCaught(
            obj['id'],
            obj['type'],
            obj['resilience_points'],
            obj['user_id']
        )


# Example usage:
if __name__ == "__main__":
    # Test User
    user = User(1, "alice", "alice@example.com", b'0' * 32, b'1' * 16, b'2' * 32)
    user_bytes = user.to_bytes()
    print(f"User JSON: {user_bytes[:100]}...")  # Show first 100 chars
    user_restored = User.from_bytes(user_bytes)
    print(f"Restored: {user_restored.Username}, {user_restored.Email}")

    # Test Creature
    creature = Creature(101, "Dragon", "dragon.png", 5)
    creature_bytes = creature.to_bytes()
    print(f"\nCreature JSON: {creature_bytes}")
    creature_restored = Creature.from_bytes(creature_bytes)
    print(f"Restored: {creature_restored.Name}, Rarity: {creature_restored.Rarity}")

    # Test CreaturesInTheWild
    wild = CreaturesInTheWild(101, 100, "gcpvj0du6e", 40.7128, -74.0060)
    wild_bytes = wild.to_bytes()
    print(f"\nWild JSON: {wild_bytes}")
    wild_restored = CreaturesInTheWild.from_bytes(wild_bytes)
    print(f"Restored: Type {wild_restored.Type}, Lat: {wild_restored.Lat}")

    # Test CreaturesCaught
    caught = CreaturesCaught(1, 101, 80, 1)
    caught_bytes = caught.to_bytes()
    print(f"\nCaught JSON: {caught_bytes}")
    caught_restored = CreaturesCaught.from_bytes(caught_bytes)
    print(f"Restored: ID {caught_restored.Id}, Type {caught_restored.Type}")