import asyncio
import random
import time
import discord
import os
import string
import lyrics
from discord.ext.commands import Bot
from discord.ext import commands
from collections import defaultdict

BOT_PREFIX = ("+")

client = Bot(command_prefix=BOT_PREFIX)
markov = defaultdict(lambda: defaultdict(int))

def remove_punction(text):
    """
    Removes the punctuation from a given string
    """
    return text.translate(str.maketrans("", "", string.punctuation))

def get_trigrams(data):
    """
    Generates the trigrams of an array of elements. For example, if `data = [a, b, c, d]` then the
    output will be `[[a,b,c], [b,c,d]]`.
    """
    for i in range(len(data) - 2):
        yield data[i:i + 3]

def get_ngrams(degree, data):
    """
    Generates the n-grams of an array of elements. For example, if `data = [a, b, c, d]` and
    `degree = 2` then the output will be `[[a,b], [b,c], [c,d]]`. This is just a generic
    version of the `get_trigrams` function, here for reference.
    """
    for i in range(len(data) - degree + 1):
        yield data[i:i + degree]

def weighted_choice(states):
    """
    Given a dictionary of keys and weights, choose a random key based on its weight.
    """
    n = random.uniform(0, sum(states.values()))
    for key, val in states.items():
        if n < val:
            return key
        n -= val

    # Something went wrong, don't make a choice.
    return None

def init_markov():
    # just join the array into a single string
    data = ' '.join([
        *lyrics.kanye_lyrics,
        *lyrics.gucci_lyrics,
        *lyrics.random_lyrics,
        *lyrics.nas_lyrics,
        *lyrics.E40_lyrics,
        *lyrics.snoop_dogg_lyrics,
        *lyrics.three_six_lyrics,
        *lyrics.project_pat_lyrics,
        *lyrics.wu_tang_lyrics,
        *lyrics.biggie_lyrics,
        *lyrics.doc_oct_lyrics,
        *lyrics.eminem_lyrics,
        *lyrics.freddie_gibbs_lyrics,
        *lyrics.big_L_lyrics,
        *lyrics.outkast_lyrics
    ])

    print('data: ' + data)
    data = remove_punction(data).replace('\n', ' ')
    parsed_data = data.split(' ')

    # Now split the input data into trigrams for parsing.
    for (w1, w2, w3) in get_trigrams(parsed_data):
        # Use lowercase to normalize the data.
        w1 = w1.lower()
        w2 = w2.lower()
        w3 = w3.lower()

        # Update the tally for this combination.
        markov[(w1, w2)][w3] += 1
    print('ok its initialized')

def spit_game():
     # Use random to pick a random initial state (or set it yourself).
    start_state = random.choice(list(markov.keys()))
    # You can preview it by writing ```print("Initial State: %s" % repr(start_state))```

    # Now start 'walking' along the Markov Chain to generate stuff. Unfortunately, the hard part
    # is knowing when to stop. Here I say I want sentences no longer than 15 words, and if there's
    # a dead-end, stop immediately. Naturally, there's much better ways to do this.
    s1, s2 = start_state
    max_length = 15
    result = [s1, s2]
    for _ in range(max_length):
        next_state = weighted_choice(markov[(s1, s2)])
        if next_state is None:
            break
        result.append(next_state)
        s1 = s2
        s2 = next_state

    # the result is an array so just make it a string
    return ' '.join(result) + '.'

@client.event
async def on_ready():
    print("It's Gucci Time!")
    init_markov()
    await client.change_presence(game=discord.Game(name='+help for command list!'))

# Sends a message to a new member that joins the discord server.
@client.event
async def on_member_join(member):
    await client.send_message(member, "Sup!? It's ya boy Young LD, and my sole purpose in this world is to provide you and your crew with some dank, absurd, hard hittin' rap lyrics.\n" 
    "For a list of all available commands, use the +help command.\n"
    "ps - Wu-Tang is 4 da children and don't forget to Protect Ya Kneck.")
     
@client.command()
async def kanye(ctx):
    await ctx.send(random.choice(lyrics.kanye_lyrics))

@client.command()
async def gucci(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.gucci_lyrics))

@client.command()
async def random(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.random_lyrics))

@client.command()
async def nas(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.nas_lyrics))

@client.command()
async def e40(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.E40_lyrics))

@client.command()
async def snoop(ctx):
    await ctx.send_message(ctx.channel, random.choices(lyrics.snoop_dogg_lyrics))

@client.command()
async def triple6(ctx):
    await ctx.send_message(ctx.channel, random.choices(lyrics.three_six_lyrics))

@client.command()
async def pat(ctx):
    await ctx.send_message(ctx.channel, random.choices(lyrics.project_pat_lyrics))

@client.command()
async def wutang(ctx):
    await ctx.send_message(ctx.channel, random.choices(lyrics.wu_tang_lyrics))

@client.command()
async def biggie(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.biggie_lyrics))

@client.command()
async def droctagon(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.doc_oct_lyrics))

@client.command()
async def eminem(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.eminem_lyrics))

@client.command()
async def gibbs(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.freddie_gibbs_lyrics))

@client.command()
async def bigl(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.big_L_lyrics))

@client.command()
async def outkast(ctx):
    await ctx.send(ctx.channel, random.choices(lyrics.outkast_lyrics))

async def list_server():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_server())
client.run(os.getenv('TOKEN'))