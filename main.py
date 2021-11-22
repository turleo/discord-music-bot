import logging

from discord import Embed, FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord.voice_client import VoiceClient
import asyncio
import os

import info_controller

bot: commands.Bot = commands.Bot(".")
ffmpeg = os.environ.get("ffmpeg_executable", "ffmpeg")

queue = {}


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


def check_queue_generator(ctx):
    global queue

    async def check_queue():
        global queue

        if queue.get(ctx.channel.id, None) is not None and queue.get(ctx.channel.id)["queue"]:
            await play_music(queue[ctx.channel.id]["queue"].pop(0), ctx)
        else:
            await ctx.send('Queue ended')
            queue[ctx.channel.id]["playing"] = False

    return check_queue


async def after_callback_generator(ctx):
    def callback(error: Exception):
        bot.loop.create_task(check_queue_generator(ctx)())

    return callback


async def play_music(track: info_controller.Music, ctx):
    global queue

    if not bot.voice_clients:
        await hi(ctx)

    await ctx.send(f'Playing {track}')
    voice: VoiceClient = bot.voice_clients[0]

    voice.play(FFmpegPCMAudio(track.load(), executable=ffmpeg),
               after=await after_callback_generator(ctx))


@bot.command()
async def play(ctx, arg: str):
    global queue

    queue[ctx.channel.id] = queue.get(ctx.channel.id, {"playing": True, "queue": []})
    queue[ctx.channel.id]["playing"] = True
    if ctx.author == bot.user:
        return

    track = info_controller.get_song(arg)
    if track is None:
        ctx.send("Sorry, this platform is not supported yet")
    try:
        await play_music(track, ctx)
    except CommandInvokeError:
        await ctx.send("Already playing")


@bot.command()
async def add(ctx, arg):
    global queue

    queue[ctx.channel.id] = queue.get(ctx.channel.id, {"playing": False, "queue": []})
    track = info_controller.get_song(arg)
    if track is None:
        ctx.send("Sorry, this platform is not supported yet")

    await ctx.send(f'Added {track}')
    if not queue[ctx.channel.id]["playing"]:
        await play(ctx, arg)
    else:
        queue[ctx.channel.id]["queue"].append(track)


@bot.command()
async def stop(ctx):
    global queue

    queue[ctx.channel.id] = {"playing": False, "queue": []}
    ctx.bot.voice_clients[0].stop()
    await ctx.send("Stopped")


@bot.command()
async def next(ctx):
    await ctx.send("Playing next")
    ctx.bot.voice_clients[0].stop()


@bot.command()
async def hi(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"Joined to {channel.name}")


@bot.command()
async def bye(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Bye 👋")


bot.run(os.environ.get("discord_token"))
