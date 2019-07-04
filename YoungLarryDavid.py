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
client.remove_command('help')
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

@client.command(pass_context=True)
async def help(ctx):
    author=ctx.message.author
    
    embed=discord.Embed(
        color=discord.Color.orange()
    )
    embed.set_author(name='Help')
    
    embed.add_field(name='+kanye', value='Displays random lyrics from the greatest artist of our generation.', inline=False)
    embed.add_field(name='+gucci', value='Displays lyrics by Guwop AKA El Gato the Human Glacier.', inline=False)
    embed.add_field(name='+nas', value='Displays random lyrics from the greatest album of all time, Illmatic.', inline=False)
    embed.add_field(name='+e40', value='Displays random lyrics by E40 AKA Charlie Hustle.', inline=False)
    embed.add_field(name='+snoop', value='Displays random lyrics by the Dogg Father.', inline=False)
    embed.add_field(name='+triple6', value='Displays random lyrics by Three 6 Mafia.', inline=False)
    embed.add_field(name='+pat', value='Displays random lyrics by Project Pat.', inline=False)
    embed.add_field(name='+wutang', value='Wu-Tang is for the the children.', inline=False)
    embed.add_field(name='+bigge', value='Displays random lyrics by the black Frank White.', inline=False)
    embed.add_field(name='+droctagon', value='Displays random lyrics by Dr.Octagon AKA the Dr.Octagonecologyst.', inline=False)
    embed.add_field(name='+eminem', value='Displays random lyrics by Eminem.', inline=False)
    embed.add_field(name='+gibbs', value='Displays random lyrics by Gangsta Gibbs.', inline=False)
    embed.add_field(name='+bigl', value='Displays random lyrics by Big L.', inline=False)
    embed.add_field(name='+outkast', value='Displays random lyrics by Outkast.', inline=False)
    embed.add_field(name='+top10', value='Young LD displays his top 10 list of the best Hip-Hop artist of all time.', inline=False)
    embed.add_field(name='+producers', value='Young LD displays his top 10 list of the best Hip-Hop producers of all time.', inline=False)
    embed.add_field(name='+random', value='Displays random lyrics from a bunch of different artist.', inline=False)
    embed.add_field(name='+spit', value='Uses a Markov chain to combine lyrics and comes up with some funky shit.', inline=False)
    embed.add_field(name='+help', value='Young LD Displays the list of command that can be used.', inline=False)
    
    await client.send_message(author, embed=embed)

async def list_server():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_server())
client.run(os.getenv('TOKEN'))
