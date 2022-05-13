import pymongo
from player import Player

class RpgDb:

    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.players = self.mydb["players"]
        self.locations = self.mydb["locations"]
        self.characters = self.mydb["characters"]

    def is_registered(self, discord_id):
        query = {"discord_id": discord_id}
        results = self.players.find_one(query)
        if results == None:
            return False
        else:
            return True

    def get_inventory(self, discord_id):
        query = {"discord_id": discord_id}
        results = self.players.find_one(query, {"_id": 0, "selected_character": 1, "characters": 1})
        print(results)
        inventory = results["characters"][int(results["selected_character"])]["inventory"]
        print(inventory)
        return inventory

    def create_character(self, name, discord_id):
        query = {"discord_id": discord_id}
        char = Player(name)
        updatestr = {"$push": {"characters": char.__dict__}}
        self.players.update_one(query, updatestr)

    def create_player(self, discord_id):
        query = {"discord_id": discord_id, "selected_character": None, "characters": []}
        self.players.insert_one(query)

    def get_characters(self, discord_id):
        query = {"discord_id": discord_id}
        results = self.players.find_one(query, {"_id": 0, "characters": 1})
        if results == None:
            return None
        return results["characters"]

    def get_selected_character(self, discord_id):
        query = {"discord_id": discord_id}
        results = self.players.find_one(query, {"_id": 0})
        return results["characters"][int(results["selected_character"])]

    def has_character_selected(self, discord_id):
        query = {"discord_id": discord_id}
        results = self.players.find_one(query, {"_id": 0, "selected_character": 1})
        if results == None:
            return False
        if results["selected_character"] != None:
            return True
        return False

    def select_character(self, discord_id, character_num):
        query = {"discord_id": discord_id}
        self.players.update_one(query, {"$set": {"selected_character": character_num}})

    def get_location(self, coordinates):
        query = {"coordinates": coordinates}
        return self.locations.find_one(query)

    def get_selected_character_location(self, discord_id):
        return self.get_selected_character(discord_id)["coordinates"]

    def get_npc_from_id(self, objectid):
        query = {"_id": objectid}
        return self.characters.find_one(query)

    def change_location(self, discord_id, coordinates):
        char_id = self.get_selected_character_id(discord_id)
        query = {"discord_id": discord_id}
        updatestr = {"$set": {f"characters.{char_id}.coordinates": coordinates}}
        self.players.update_one(query, updatestr)

    def get_selected_character_id(self, discord_id):
        query = {"discord_id": discord_id}
        results = self.players.find_one(query, {"_id": 0, "selected_character": 1})
        return results["selected_character"]



    
if __name__ == "__main__":
    db = RpgDb()
    db.get_selected_character_id(284769523020595200)
    # db.get_inventory(284769523020595200)
    # print(db.get_location((0,0)))
    # print(db.get_characters(21342319847))
    # player = {"discord_id": "21342319847", "selected_character": 0, "characters": [{"name": "harry", "stats": {"strength": 1, "physique": 1}, "currency": 100, "inventory": [{"amount": 1, "name": "big_sword", "type": "weapon", "stats": {}}]}]}
    # db.get_characters(21342319847)
    # db.get_characters(40)
    # db.players.insert_one(player)
    # print("Done")