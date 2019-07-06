import asyncio
import random
import time
import discord
import os
import string
import lyrics
from spit import init_markov
from spit import spit_game
from discord.ext.commands import Bot
from discord.ext import commands
from collections import defaultdict

BOT_PREFIX = ("+")

client = Bot(command_prefix=BOT_PREFIX)
#client.remove_command('help') will fix this later

@client.event
async def on_ready():
    print("Young LD is online")
    init_markov()
    await client.change_presence(game=discord.Game(name='+help for command list!'))

# Sends a message to a new member that joins the discord server.
@client.event
async def on_member_join(member):
    await client.send_message(member, "Sup!? It's ya boy Young LD, and my sole purpose in this world is to provide you and your crew with some dank, absurd, hard hittin' rap lyrics.\n" 
    "For a list of all available commands, use the +help command.\n"
    "ps - Wu-Tang is 4 da children and don't forget to Protect Ya Kneck.")
    
@client.event
async def on_message(message):
    # Don't need the bot to reply to itself.
    if message.author == client.user:
        return

    # Randomly picks a lyric from the list of kanye_lyrics
    if message.content.upper().startswith('+KANYE'):
        await client.send_message(message.channel, random.choice(lyrics.kanye_lyrics))

    # Randomly picks a lyric from the list of gucci_lyrics
    if message.content.upper().startswith('+GUCCI'):
        await client.send_message(message.channel, random.choice(lyrics.gucci_lyrics))

    # Randomly picks a lyrics from the list of random_lyrics
    if message.content.upper().startswith('+RANDOM'):
        await client.send_message(message.channel, random.choice(lyrics.random_lyrics))

    # Randomly picks lyrics from the list of nas_lyrics
    # primarily lyrics from illmatic aka the best hip hop album of all time
    if message.content.upper().startswith('+NAS'):
        await client.send_message(message.channel, random.choice(lyrics.nas_lyrics))

    # Randomly picks lyrics from the list of E40_lyrics
    if message.content.upper().startswith('+E40'):
        await client.send_message(message.channel, random.choice(lyrics.E40_lyrics))

    # Randomly picks lyrics from the list of snoop_dogg_lyrics
    if message.content.upper().startswith('+SNOOP'):
        await client.send_message(message.channel, random.choice(lyrics.snoop_dogg_lyrics))

    # Randomly picks lyrics from the list of three_six_lyrics
    if message.content.upper().startswith('+TRIPLE6'):
        await client.send_message(message.channel, random.choice(lyrics.three_six_lyrics))

    # Randomly picks lyrics from the list of project_pat_lyrics
    if message.content.upper().startswith('+PAT'):
        await client.send_message(message.channel, random.choice(lyrics.project_pat_lyrics))

    # Randomly picks lyrics from the list of wu_tang_lyrics
    if message.content.upper().startswith('+WUTANG'):
        await client.send_message(message.channel, random.choice(lyrics.wu_tang_lyrics))

    # Randomly picks lyrics from the list of biggie_lyrics
    if message.content.upper().startswith('+BIGGIE'):
        await client.send_message(message.channel, random.choice(lyrics.biggie_lyrics))

    # Rancomly picks lyrics from the list of doc_oct_lyrics
    if message.content.upper().startswith('+DROCTAGON'):
        await client.send_message(message.channel, random.choice(lyrics.doc_oct_lyrics))

    # Randomly picks lyrics from the list of eminem_lyrics
    if message.content.upper().startswith('+EMINEM'):
        await client.send_message(message.channel, random.choice(lyrics.eminem_lyrics))

    # Randomly picks lyrics from the list of gangsta gibbs lyrics
    if message.content.upper().startswith('+GIBBS'):
        await client.send_message(message.channel, random.choice(lyrics.freddie_gibbs_lyrics))

    # Randomly picks lyrics from the list of Big L lyrics
    if message.content.upper().startswith('+BIGL'):
        await client.send_message(message.channel, random.choice(lyrics.big_L_lyrics))

    # Randomly picks lyrics from the list of Outkast lyrics
    if message.content.upper().startswith('+OUTKAST'):
        await client.send_message(message.channel, random.choice(lyrics.outkast_lyrics))

    # Displays the bots personal opinion on who are the top 10 best hip-hop artist of all time
    if message.content.upper().startswith('+TOP10'):
        await client.send_message(message.channel, "This is my top ten list of the best hip-hop artist of all time.\n"
                                  "1. Nas\n"
                                  "2. Ghostface Killah\n"
                                  "3. Andre 3000\n"
                                  "4. The Notorious B.I.G.\n"
                                  "5. Big L\n"
                                  "6. Raekwon da Chef\n"
                                  "7. Tupac\n"
                                  "8. Kendrick Lamar\n"
                                  "9. Eminem\n"
                                  "10. Jay-Z")

    # Displays the bots personal opinion on who are the top 10 best hip-hop producers of all time
    if message.content.upper().startswith('+PRODUCERS'):
        await client.send_message(message.channel, "This is my top ten list of best hip-hop producers of all time.\n"
                                  "1. J Dilla\n"
                                  "2. Madlib\n"
                                  "3. RZA\n"
                                  "4. Dr. Dre\n"
                                  "5. Organized Noize\n"
                                  "6. No I.D.\n"
                                  "7. Pete Rock\n"
                                  "8. Sounwave\n"
                                  "9. Q-Tip\n"
                                  "10. Kanye West")
    
    # Uses markov chain to generate random lyrics
    if message.content.upper().startswith('+SPIT'):
        await client.send_message(message.channel, spit_game())
    
    # Displays commands for the user
    if message.content.upper().startswith('+HELP'):
        commands={}
        commands['+help']='Young LD Displays the list of command that can be used.'
        commands['+kanye']='Displays random lyrics from the greatest artist of our generation.'
        commands['+gucci']='Displays lyrics by Guwop AKA El Gato the Human Glacier.'
        commands['+nas']='Displays random lyrics from the greatest album of all time, Illmatic.'
        commands['+e40']='Displays random lyrics by E40 AKA Charlie Hustle.'
        commands['+snoop']='Displays random lyrics by the Dogg Father.'
        commands['+triple6']='Displays random lyrics by Three 6 Mafia.'
        commands['+pat']='Displays random lyrics by Project Pat.'
        commands['+wutang']='Wu-Tang is for the the children.'
        commands['+biggie']='Displays random lyrics by the black Frank White.'
        commands['+droctagon']='Displays random lyrics by Dr.Octagon AKA the Dr.Octagonecologyst.'
        commands['+eminem']='Displays random lyrics by Eminem.'
        commands['+gibbs']='Displays random lyrics by Gangsta Gibbs.'
        commands['+bigl']='Displays random lyrics by Big L.'
        commands['+outkast']='Displays random lyrics by Outkast.'
        commands['+top10']='Young LD displays his top 10 list of the best Hip-Hop artist of all time.'
        commands['+producers']='Young LD displays his top 10 list of the best Hip-Hop producers of all time.'
        commands['+random']='Displays random lyrics from a bunch of different artist.'
        commands['+spit']='Uses a Markov chain to combine lyrics and comes up with some funky shit.'

        msg=discord.Embed(title='Young Larry David', description='Written by SnoopFrogg', color=0x0000ff)
        for command, description in commands.items():
            msg.add_field(name=command, value=description, inline=False)
        #msg.add_field(name='Join our Discord/For Questions/Chilling', value='', inline=False)
        await client.send_message(message.channel, embed=msg)

async def list_server():
    await client.wait_until_ready()
    while not client.is_closed:
        servers = list(client.servers)
        print("Its Gucci Time! Young LD is connected to " + str(len(client.servers)) + " servers:")
        for x in range(len(servers)):
            print(' ' + servers[x-1].name)

        await asyncio.sleep(600)
        
client.loop.create_task(list_server())
client.run(os.getenv('TOKEN'))