import discord
from discord.ext import commands
from rpgdb import RpgDb

description = ""

# intents = discord.Intents.default()
# intents.members = True

bot = commands.Bot(command_prefix='?', description=description)
# , intents=intents)
db = RpgDb()


def needs_character_selected(func):
    async def inner1(*args, **kwargs):
        if db.get_selected_character_id(args[0].author.id) is not None:
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
async def character(ctx, name: str = None, class_id: int = None):
    if not db.is_registered(ctx.author.id):
        await ctx.send("You need to register first")
        return
    print(name, class_id)
    if name is not None and class_id is not None:
        db.create_character(name, class_id, ctx.author.id)
        await ctx.send(f"Created {name} as {class_id}")
    else:
        await ctx.send("Usage: create character {name} {class_id}")


@bot.group(name="admin")
async def admin(ctx):
    pass


@admin.command(name="give")
async def give(ctx, item_id: int, user: discord.Member):
    character_id = db.get_selected_character_id(user.id)
    db.give_item(item_id, character_id)


@bot.group(name="list")
async def _list(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f'holy moly')


@_list.command(name="character")
@needs_character_selected
async def list_characters(ctx):
    discord_id = ctx.author.id
    chars = db.get_characters(discord_id)
    rtrnstr = ""
    if len(chars) == 0:
        ctx.send("You don't have any characters!")
    for char in chars:
        rtrnstr += f"Class: {char[0]}\nName: {char[1]}\nGold: {char[2]}\n ID: {char[3]}\n"
    await ctx.send(rtrnstr)


@bot.group()
async def select(ctx):
    pass


@select.command()
async def character(ctx):
    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    chars = db.get_all_character(ctx.author.id)
    rtrnstr = ""
    i = 1
    if len(chars) == 0:
        await ctx.send("You don't have any characters.\nmake one with the create character command")
        return
    for char in chars:
        rtrnstr += f"{i}: {char['name']}\nclass: {char['class_name']}\n\n"
    await ctx.send(rtrnstr)
    try:
        answer = await bot.wait_for('message', check=is_correct, timeout=5)
    except TimeoutError:
        await ctx.send("You took to long try again")
        return
    character_id = chars[int(answer.content) - 1]["character_id"]
    db.select_character(character_id, ctx.author.id)
    await ctx.send(f"You selected {chars[int(answer.content) - 1]['name']}")


@bot.command()
async def register(ctx):
    if db.is_registered(ctx.author.id):
        await ctx.send("You already have been registered!")
    else:
        db.create_player(ctx.author.id)
        await ctx.send("You have been registered")


@bot.command(name="character")
@needs_character_selected
async def character(ctx, *user: discord.Member):
    character_id = db.get_selected_character(ctx.author.id)
    await ctx.send(str(character_id))


@bot.command(name="inventory")
@needs_character_selected
async def inventory(ctx):
    items = db.get_inventory(ctx.author.id)
    print(items)
    if len(items) == 0:
        await ctx.send("You don't have any items yet.")
        return
    rtrnstr = ""
    for item_key, item_amount in items.items():
        item_id, item_name = item_key
        rtrnstr += f"{item_amount}: {item_name}\n"
    await ctx.send(rtrnstr)


@bot.command(name="map", description="Displays the map")
async def _map(ctx):
    return


with open("token.txt") as f:
    token = f.read()

bot.run(token)
