from bson.objectid import ObjectId
class Player:

    def __init__(self, name="Harry", gender="male", race="human", hair_colour="black", hair_type="straight", hair_length="short", body_size="slim", coordinates=(0,0), strength=1, constitution=1, intelligence=1, dexterity=1, wisdom=1, charisma=1, hp=100, mana=100):
        self.name = name
        self.gender = gender
        self.inventory = []
        self.race = race
        self.appearance = {
            "hair": {
                "colour": hair_colour,
                "type": hair_type,
                "length": hair_length
            },
            "body": {
                "size": body_size
            },
        }
        self.coordinates = coordinates
        self.stats = {
            "Strength": strength,
            "Constitution": constitution,
            "Dexterity": dexterity,
            "Intelligence": intelligence,
            "Wisdom": wisdom,
            "Charisma": charisma
        }
        self.hp = hp
        self.mana = mana