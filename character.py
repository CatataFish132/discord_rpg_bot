from bson.objectid import ObjectId
class Character:

    def __init__(self, name, gender, race, strength, constitution, intelligence, dexterity, wisdom, charisma, description):
        self.name = name
        self.gender = gender
        self.inventory = []
        self.race = race

        # self.appearance = {
        #     "hair": {
        #         "colour": hair_colour,
        #         "type": hair_type,
        #         "length": hair_length
        #     },
        #     "body": {
        #         "size": body_size
        #     },
        # }

        self.stats = {
            "Strength": strength,
            "Constitution": constitution,
            "Dexterity": dexterity,
            "Intelligence": intelligence,
            "Wisdom": wisdom,
            "Charisma": charisma
        }

        self.dialogue = {
            "talk": {
                "text": "hello there",
                "actions": ["give sword"],
                "next": {
                    "how are you doing?": {
                        "text": "Im doing great ty for asking!",
                        "next": {
                            "bye": {
                                "text": "cya"
                            }
                        }
                    }
                }}}

        self.description = description

if __name__ == "__main__":
    import json
    # name = input("name: ")
    # gender = input("gender(male, female, nonbinary): ")
    # race = input("race: ")
    # hair_colour = input("hair_colour: ")
    # hair_length = input("hair_length(short, long): ")
    # hair_type = input("hair_type: ")
    # body_size = input("body_size(slim, big, chunky): ")
    
    # strength = input("strength: ")
    # constitution = input("constitution: ")
    # intelligence = input("intelligence: ")
    # dexterity = input("dexterity: ")    
    # wisdom = input("wisdom: ")
    # charisma = input("charisma: ")

    # description = input("description")

    # dialogue = {}
    # while True:
    #     option = input("do you want to add a dialogue option: ")
    #     if option == "yes" or option == "y":
    #         label = input("label: ")
    #         text = input("text: ")
    #         actions = []
    #         while True:
    #             if input("do you want to add an action?(type yes): ") == "yes":
    #                 actions.append(input("action: "))
    #             else:
    #                 break
    #         print("do you want to add\n\n")
    #         print(str({"text": text, "actions": actions}))
    #         while True:
    #             continue_adding = input("yes or no?: ")
    #             if continue_adding == "yes" or continue_adding == "y":
    #                 dialogue[label] = {"text": text, "actions": actions}
    #             elif continue_adding == "no" or continue_adding == "n":
    #                 break
    #             else:
    #                 print("invalid input try again")
    #     if option == "no" or option == "n":
    #         break
    #     print("please type yes/y or no/n")
    
    # character = Character(name, gender, race, hair_colour, hair_type, hair_length, body_size, location_id, strength, constitution, intelligence, dexterity, wisdom, charisma, description)
    # # json_string = json.dumps(character.__dict__)
    # # print("\n\n" + json_string + "\n\n")

    # add_this_character = input("add this character?: ")
    # if add_this_character == "yes":
    #     import pymongo
    #     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    #     mydb = myclient["mydatabase"]
    #     characters = mydb["characters"]
    #     characters.insert_one(character.__dict__)



    name = "Mysterious man"
    gender = "Male"
    race = "human"
    
    strength = 1000
    constitution = 1000
    intelligence = 1000
    dexterity = 1000
    wisdom = 1000
    charisma = 1000

    description = "There is a mysterious man at the river in the cave. He has medium long black hair. One of his eyes is covered by his hair and the other eye is glowing green. You feel him creepely gazing upon you."
    
    character = Character(name=name, gender=gender, race=race, strength=strength, constitution=constitution, intelligence=intelligence, dexterity=dexterity, wisdom=wisdom, charisma=charisma, description=description)

    import pymongo
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    characters = mydb["characters"]
    characters.insert_one(character.__dict__)