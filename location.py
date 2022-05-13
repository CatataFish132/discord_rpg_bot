class Location:
    def __init__(self, name="", description="", characters=[], enemies={}, coordinates=(0,0)):
        self.name = name
        self.description = description
        self.characters = characters
        self.enemies = enemies # {bat_id: 0.3, slime_id: 0.7}
        self.coordinates = coordinates

if __name__ == "__main__":
    location = Location(name="Slime forest", description="This forest has alot of slimes and the slimes make everything slimy, even the trees are slimy", coordinates=(0,1))
    import pymongo
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    locations = mydb["locations"]
    locations.insert_one(location.__dict__)
