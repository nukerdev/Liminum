import discord, json, os, subprocess

os.system('pip install -r requirements/requirements.txt')

from colorama import Fore
from discord.ext import commands
from utili import init, clearConsole, printToConsole

with open("src/config.json", "r") as data:
    config = json.load(data)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)
token = config["token"]

@bot.event
async def on_ready():
    init()
    clearConsole()
    print(f"""{Fore.MAGENTA} ██▓     ██▓ ███▄ ▄███▓ ██▓ ███▄    █  █    ██  ███▄ ▄███▓
▓██▒    ▓██▒▓██▒▀█▀ ██▒▓██▒ ██ ▀█   █  ██  ▓██▒▓██▒▀█▀ ██▒
▒██░    ▒██▒▓██    ▓██░▒██▒▓██  ▀█ ██▒▓██  ▒██░▓██    ▓██░
▒██░    ░██░▒██    ▒██ ░██░▓██▒  ▐▌██▒▓▓█  ░██░▒██    ▒██ 
░██████▒░██░▒██▒   ░██▒░██░▒██░   ▓██░▒▒█████▓ ▒██▒   ░██▒
░ ▒░▓  ░░▓  ░ ▒░   ░  ░░▓  ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░
░ ░ ▒  ░ ▒ ░░  ░      ░ ▒ ░░ ░░   ░ ▒░░░▒░ ░ ░ ░  ░      ░
  ░ ░    ▒ ░░      ░    ▒ ░   ░   ░ ░  ░░░ ░ ░ ░      ░   
    ░  ░ ░         ░    ░           ░    ░            ░   
                                                          """)
    printToConsole(f"Logged in as {bot.user}", "success")
    printToConsole(f"Guilds: {len(bot.guilds)}", "info")
    printToConsole(f"Token: {config["token"][8]}{"*" * 8}{"..."}", "info")

    if bool(config["auto_grab_on_start"]):
        for guild in bot.guilds:
            await grab(guild=guild)

async def grab(ctx: commands.Context = None, guild: discord.Guild = None):
    delete_message = config.get("delete_message", False)

    if ctx is not None:
        guild = ctx.guild

    if delete_message and ctx is not None:
        await ctx.message.delete()

    webhooks = await guild.webhooks()
    webhook_list = []
    webhook_limit = int(config.get("webhooks", 10))
    more_info = config.get("webhook_info", False)

    for i, webhook in enumerate(webhooks, start=1):
        if i > webhook_limit:
            break

        webhook_data = {"url": webhook.url}
        if more_info:
            webhook_data["details"] = {
                "created_at": str(webhook.created_at),
                "name": webhook.name,
                "channel": webhook.channel.name,
                "avatar": str(webhook.avatar),
            }
        webhook_list.append(webhook_data)

    file_path = f"src/{config['target_file']}.json"
    file_path = file_path.replace("%guild_id%", str(guild.id)).replace("%guild_name%", guild.name)

    try:
        with open(file_path, "w") as f:
            json.dump({"webhooks": webhook_list}, f, indent=4)
    except Exception as e:
        printToConsole(f"Failed to save webhooks to file: {e}", "error")
    else:
        printToConsole("Saved webhooks to file.", "saved")

@bot.command(name=config["command_name"])
async def grab_webhooks(ctx: commands.Context):
    await grab(ctx=ctx)

try:
    bot.run(token)
except KeyboardInterrupt:
    printToConsole("Exit program by user.", "exit")
except discord.errors.LoginFailure:
    printToConsole("Invalid token", "discord_error")