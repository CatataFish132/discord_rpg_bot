import discord
from discord.ext import commands
from mongodb import RpgDb

description = ""

# intents = discord.Intents.default()
# intents.members = True

bot = commands.Bot(command_prefix='?', description=description)
# , intents=intents)
db = RpgDb()


def needs_character_selected(func):
    async def inner1(*args, **kwargs):
        if db.has_character_selected(args[0].author.id):
            await func(*args, **kwargs)
        else:
            await args[0].send("You don't have a character selected")

    return inner1


# def needs_registered(func):
#     async def inner1(*args, **kwargs):
#         if db.is_registered(args[0].author.id):
#             await func(*args, **kwargs)
#         else:
#             await args[0].send("You need to be registered to use this command pls use the register command.")
#     return inner1


# def needs_character_selected(func):
#     async def decorator(*args, **kwargs):
#         print("test")
#         await func(*args, **kwargs)
#     print("another test")
#     return decorator


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.group(name="create")
async def create(ctx):
    pass

@create.command(usage="test", help="another test", description="test", name="character")
async def character(ctx, name: str = None):
    if not db.is_registered(ctx.author.id):
        await ctx.send("You need to register first")
        return
    if name is not None:
        db.create_character(name, ctx.author.id)
        await ctx.send(f"Created {name}")
    else:
        await ctx.send("Usage: create character {name}")


@bot.group(name="admin")
async def admin(ctx):
    pass

# still need work
@admin.command(name="give")
async def give(ctx, item_id: int, user: discord.Member):
    character_id = db.get_selected_character_id(user.id)
    db.give_item(item_id, character_id)


@bot.group(name="list")
async def _list(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f'holy moly')


# should work with new db
@_list.command(name="character")
async def list_characters(ctx):
    discord_id = ctx.author.id
    chars = db.get_characters(discord_id)
    rtrnstr = ""
    if len(chars) == 0:
        ctx.send("You don't have any characters!")
    for char in chars:
        rtrnstr += f"Name: {char['name']}\n"
    await ctx.send(rtrnstr)


@bot.group()
async def select(ctx):
    pass


# should work with new db
@select.command()
async def character(ctx):
    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    chars = db.get_characters(ctx.author.id)
    rtrnstr = ""
    if len(chars) == 0:
        await ctx.send("You don't have any characters.\nmake one with the create character command")
        return
    for i, char in enumerate(chars):
        rtrnstr += f"{i+1}: {char['name']}\n"
    await ctx.send(rtrnstr)
    try:
        answer = await bot.wait_for('message', check=is_correct, timeout=5)
    except TimeoutError:
        await ctx.send("You took to long try again")
        return
    db.select_character(ctx.author.id, int(answer.content)-1)
    await ctx.send(f"You selected {chars[int(answer.content) - 1]['name']}")


# works with new db
@bot.command()
async def register(ctx):
    if db.is_registered(ctx.author.id):
        await ctx.send("You already have been registered!")
    else:
        db.create_player(ctx.author.id)
        await ctx.send("You have been registered")


# works with new db
@bot.command(name="character")
@needs_character_selected
async def character(ctx, *user: discord.Member):
    character_id = db.get_selected_character(ctx.author.id)
    await ctx.send(str(character_id))


# work with new db
@bot.command(name="inventory")
@needs_character_selected
async def inventory(ctx):
    items = db.get_inventory(ctx.author.id)
    print("ITEEEEEEEEEEEMS")
    print(items)
    if len(items) == 0:
        await ctx.send("You don't have any items yet.")
        return
    rtrnstr = ""
    for item in items:
        item_amount = item["amount"]
        item_name = item["name"]
        rtrnstr += f"{item_amount}: {item_name}\n"
    await ctx.send(rtrnstr)

@bot.command(name="mirror")
async def mirror(ctx):
    char = db.get_selected_character(ctx.author.id)
    string = "You are {name} a traveler from another world!\n You have {hair_colour} hair that is {hair_length} and {hair_type}.\n Ur from the {race} race"
    await ctx.send(format_string(string, char))

def format_string(non_formatted_string, character):
    appearance = character['appearance']
    hair = appearance['hair']
    dictionary = {
        "name": character['name'],
        "hair_colour": hair['colour'],
        "hair_length": hair['length'],
        "hair_type" : hair['type'],
        "race": character['race']
        }
    return non_formatted_string.format(**dictionary)

@bot.command(name="look")
async def look(ctx):
    coordinates = db.get_selected_character_location(ctx.author.id)
    await look_around(ctx, coordinates)

async def look_around(ctx, coordinates):
    location = db.get_location(coordinates)
    x = coordinates[0]
    y = coordinates[1]
    return_string = ""
    return_string += location["description"]
    return_string += "\n\n"

    directions = {
    "north": [x,y+1],
    "east": [x+1,y],
    "south": [x,y-1],
    "west": [x-1,y]
    }

    for object_id in location['characters']:
        character = db.get_npc_from_id(object_id)
        return_string += f"{character['description']}\n\n"

    for direction, coordinates in directions.items():
        result = db.get_location(coordinates)
        if result == None:
            continue
        else:
            return_string += f"You are able to go {direction} towards {result['name']}\n"
    await ctx.send(return_string)

@bot.command(name="north")
async def north(ctx):
    coordinates = db.get_selected_character_location(ctx.author.id)
    coordinates[1] += 1
    db.change_location(ctx.author.id, coordinates)
    await look_around(ctx, coordinates)

@bot.command(name="east")
async def east(ctx):
    coordinates = db.get_selected_character_location(ctx.author.id)
    coordinates[0] += 1
    db.change_location(ctx.author.id, coordinates)
    await look_around(ctx, coordinates)

@bot.command(name="south")
async def south(ctx):
    coordinates = db.get_selected_character_location(ctx.author.id)
    coordinates[1] -= 1
    db.change_location(ctx.author.id, coordinates)
    await look_around(ctx, coordinates)

@bot.command(name="west")
async def west(ctx):
    coordinates = db.get_selected_character_location(ctx.author.id)
    coordinates[0] -= 1
    db.change_location(ctx.author.id, coordinates)
    await look_around(ctx, coordinates)


@bot.command(name="map", description="Displays the map")
async def _map(ctx):
    return


with open("token.txt") as f:
    token = f.read()

bot.run(token)
