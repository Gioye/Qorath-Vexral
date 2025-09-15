import discord
from discord.ext import commands
import time
import re

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # needed for kick/ban

bot = commands.Bot(command_prefix="qv!", intents=intents)

bot.remove_command("help") # to make custom help command


# Utility function to check if user is "admin" (has both kick and ban perms)
def is_admin(member: discord.Member):
    perms = member.guild_permissions
    return perms.kick_members and perms.ban_members

# Ping command with latency
@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    msg = await ctx.send("Pinging...")
    end = time.perf_counter()
    latency = (end - start) * 1000  # in ms
    await msg.edit(content=f"Pong! 🏓 `{int(latency)}ms`")

# Ghostsay command (say then delete user message)
@bot.command()
async def ghostsay(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message + f"\n-# sent by {ctx.author.mention}")

# Webhook command
@bot.command()
async def webhook(ctx, url: str, *, text: str):
    try:
        parsed_text = text.replace("/n", "\n").strip("\"")
        webhook = discord.Webhook.from_url(url, client=bot)
        await webhook.send(parsed_text, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url if ctx.author.avatar else None)
        await ctx.send("✅ Sent webhook message.")
    except Exception as e:
        await ctx.send(f"❌ Error sending webhook: {e}")

# Nuke command
@bot.command()
async def nuke(ctx):
    gif_url = "https://media.tenor.com/kQevh4gr6LwAAAAi/cat-brick.gif"
    await ctx.send(gif_url)
    await ctx.send("I don't know how to nuke this server so I will nuke you cat instead 🧱🐱")

# Raid command
@bot.command()
async def raid(ctx):
    await ctx.send("I'm too lazy to raid, sorry 😴")

# Ban command (admin only)
@bot.command()
async def ban(ctx, target: str):
    if not is_admin(ctx.author):
        await ctx.send("❌ You don't have permission to use this.")
        return

    user = None
    if target.isdigit():
        user = await ctx.guild.fetch_member(int(target))
    elif ctx.message.mentions:
        user = ctx.message.mentions[0]

    if user:
        try:
            await ctx.guild.ban(user)
            await ctx.send(f"✅ Banned {user.name}")
        except Exception as e:
            await ctx.send(f"❌ Couldn't ban: {e}")
    else:
        await ctx.send("❌ Invalid target.")

# Kick command (admin only)
@bot.command()
async def kick(ctx, target: str):
    if not is_admin(ctx.author):
        await ctx.send("❌ You don't have permission to use this.")
        return

    user = None
    if target.isdigit():
        user = await ctx.guild.fetch_member(int(target))
    elif ctx.message.mentions:
        user = ctx.message.mentions[0]

    if user:
        try:
            await ctx.guild.kick(user)
            await ctx.send(f"✅ Kicked {user.name}")
        except Exception as e:
            await ctx.send(f"❌ Couldn't kick: {e}")
    else:
        await ctx.send("❌ Invalid target.")

# NSFW RP commands
@bot.command()
async def nsfw_rp_bathroom(ctx, target: discord.Member):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ This command can only be used in NSFW channels.")
        return
    await ctx.send(f"{ctx.author.mention} and {target.mention} are locked up in a bathroom. They were lost and drunk and forgot they put the key under a carpet. Will they find the key or end up having... 😏")

@bot.command()
async def nsfw_rp_lgbt_bathroom(ctx, target: discord.Member):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ This command can only be used in NSFW channels.")
        return
    await ctx.send(f"{ctx.author.mention} and {target.mention} are locked up in a bathroom. they're gay and they want to fuck so hard. will they open the bathroom or will they... 😏")

# Global dictionary to store tags
tags = {}

@bot.group()
async def tag(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("❌ Invalid subcommand. Use `add`, `delete`, or `show`.")

# Add tag command
@tag.command()
async def add(ctx, tagname: str, *, text: str):
    if tagname in tags:
        await ctx.send("❌ A tag with that name already exists.")
        return
    tags[tagname] = {
        "content": text,
        "author": ctx.author.id  # Store author for future use if needed
    }
    await ctx.send(f"✅ Tag `{tagname}` added.")

# Delete tag command
@tag.command()
async def delete(ctx, tagname: str):
    if tagname not in tags:
        await ctx.send("❌ No such tag exists.")
        return
    tag_data = tags[tagname]
    if tag_data["author"] != ctx.author.id and not is_admin(ctx.author):
        await ctx.send("❌ You can only delete your own tags (or be an admin).")
        return
    del tags[tagname]
    await ctx.send(f"✅ Tag `{tagname}` deleted.")

# Show tag command
@tag.command()
async def show(ctx, tagname: str):
    if tagname not in tags:
        await ctx.send("❌ No such tag exists.")
        return
    tag_data = tags[tagname]
    author_mention = f"<@{tag_data['author']}>"
    await ctx.send(f"{tag_data['content']}\n\n⚠️ WARNING! This tag was made and sent by {author_mention}")


# Custom help command
@bot.command(name="help")
async def help_command(ctx):
    base_cmds = (
        "`qv!ping` - Ping the bot and see latency\n"
        "`qv!ghostsay <message>` - Bot repeats your message and deletes yours\n"
        "`qv!webhook <url> \"message\"` - Send a message to a webhook. Use /n for newlines\n"
        "`qv!tag add <tagname> \"text\"` - Adds a tag, it gets deleted when bot goes offline\n"
        "`qv!tag delete <tagname>` - Deletes your tag\n"
	"`qv!tag show <tagname>` - shows your tag\n"
	"`qv!nuke` - Cat brick gif\n"
        "`qv!raid` - Does absolutely nothing\n"
        "`qv!ban <id or @user>` - Ban someone (admin only)\n"
        "`qv!kick <id or @user>` - Kick someone (admin only)\n"
    )

    if ctx.channel.is_nsfw():
        nsfw_cmds = (
            "`qv!nsfw_rp_bathroom @user` - NSFW RP scenario\n"
            "`qv!nsfw_rp_lgbt_bathroom @user` - NSFW LGBT RP scenario\n"
        )
        help_msg = "**📖 Available Commands:**\n" + base_cmds + nsfw_cmds
    else:
        help_msg = (
            "**📖 Available Commands:**\n" + base_cmds +
            "\nThere are also **NSFW commands**. Switch to an NSFW channel to see them."
        )

    await ctx.send(help_msg)


# On ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

bot.run(TOKEN)
