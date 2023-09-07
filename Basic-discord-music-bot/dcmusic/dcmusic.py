import discord
from discord.ext import commands
import nacl
import asyncio
import youtube_dl

intents = discord.Intents().all()
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='', intents=intents)
key = "TOKEN"

@bot.event
async def on_ready():
    print("im ok")

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}



@bot.event
async def on_message(ctx):
    if ctx.content.startswith("!play"):
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
            await asyncio.sleep(1)
        except:
            print('error')
        try:
            url = ctx.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")
            await asyncio.sleep(3)

            voice_clients[ctx.guild.id].play(player)
            await asyncio.sleep(1)

        except Exception as err:
            print(err)
    elif ctx.content.startswith("!pause"):
        try:
            await asyncio.sleep(1)
            voice_clients[ctx.guild.id].pause()
        except Exception as err:
            print(err)

    elif ctx.content.startswith("!stop"):
        try:
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            await asyncio.sleep(1)
        except Exception as err:
            print(err)

    elif ctx.content.startswith("!resume"):
        try:
            voice_clients[ctx.guild.id].resume()
            await asyncio.sleep(1)
        except Exception as err:
            print(err)


bot.run("TOKEN")