import discord
import os
from dotenv import load_dotenv
from typer import Typer

load_dotenv()
app = Typer()

intents = discord.Intents.default()
intents.members=True
intents.message_content = True
client = discord.Client(intents=intents)
channel_id = 1233733493683650600  

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('alo'):
        await message.channel.send('que?!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(channel_id)
    if channel:  
        embed = discord.Embed(title=f"Boas {member.name}", description=f"Thanks for joining bro, have fun!")
        embed.set_thumbnail(url=member.avatar)
        await channel.send(embed=embed)
    else:
        print("Channel not found!")



client.run(os.getenv('DISCORD_TOKEN',None))
