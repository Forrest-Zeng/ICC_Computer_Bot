import discord, os
bot = discord.Client()

@bot.event
async def on_ready():
    ... # do stuff
    

bot.run(os.environ["DISCORD_TOKEN"])