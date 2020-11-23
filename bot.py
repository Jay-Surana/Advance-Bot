'''
Made by - Jay Surana
Discord - ! Real#4810
Join My support bot server - https://discord.gg/qAs3Zr2cnU
Please Follow me on Github - https://github.com/Jay-Surana
'''

import discord
from discord.ext import commands
import traceback
import sys
import asyncio
from typing import Union
from discord import utils
from discord.errors import Forbidden

intents = discord.Intents.default() #IMPORTANT:Enable all Privileged Gateway Intents in https://discord.com/developers/applications/ 
intents.members = True

TOKEN="token here" #example - "bjqfebjlnqklnifbnaewnhnfoiqefioqip"
PREFIX="?" #put your prefix here

bot = commands.Bot(command_prefix =PREFIX,
                   intents=intents,
                   help_command=None,
                   case_insensitive=True)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Made by - ! Real#4810')) 
    print("Bot is ready...")

@bot.event
async def on_member_join(member):
    guild: discord.Guild = member.guild
    channels = guild.channels
    
    wel_channel = bot.guild.get_channel('id here') #example - bot.guild.get_channel(733224387263856681) 
    #for none type wel_channel=None
    wlcm_msg = f'Hi {member.mention}' #this is just a example you can change it. 
                                             #if u want to print something on new like use \n 
                                             #if u want to mention a channel use <#channel id>
                                             #if u want to use animated server emojis use the emoji id like this <a:pin:750619312989011990>  
    
    #sending message
    await wel_channel.send(wlcm_msg)
    

@bot.event
async def on_member_remove(member):
    guild = member.guild
    channels = guild.channels
    
    leave_channel = bot.guild.get_channel('channel id here') #example - bot.guild.get_channel(733224387263856681) 
    #for none type leave_channel=None
    leave_msg = f"{member} left ....."

    #sending message
    await leave_channel.send(leave_msg)

#mute role creation
async def create_mute_role(guild):
    perms = discord.Permissions(send_messages=False)
    mute_role = await guild.create_role(name="Muted", color=discord.Color.dark_grey(), permissions=perms)

    for channel in guild.channels:
        await channel.set_permissions(mute_role, send_messages=False)

    return mute_role

#commands
@bot.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author  

    embed = discord.Embed(
    title = f"Hello {author.name}" "\n" "Here are all Command",
    description =  "**Member Commands**" "\n" "`help`, `hello`" "\n" "`ping`, `support`, `userinfo`," "\n" "`serverinfo`" "\n"
    "**Mod Command**" "\n" "`kick`, `ban`," "\n" "`unban`, `addrole`," "\n" "`removerole`, `mute`," "\n" "`unmute`, `clear`," "\n"
    "`warn`, `warncount`" "\n"
    "**Management Command**" "\n" "`lockchannel`, `unlockchannel`," "\n" "`say`, `nuke`,"  "\n" "`announce`, `poll`," "\n" 
    "`lock`, `unlock`",
    colour = discord.Colour.red()
    )
    await ctx.send(f"**Hello {ctx.author.mention} Check Your DM**", delete_after = 5)
    await author.send(embed=embed)

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Hi {ctx.author.mention}")

@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    await ctx.send(f'🏓Pong `{ping}ms`')

@bot.command(name="clear")
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx, count: int = None):
    if count is None:
        await ctx.send("Insufficient arguments.")
    else:
        await ctx.channel.purge(limit=count+1)
        rtmsg = await ctx.send(f"Cleared the last {count} message(s)!")
        await asyncio.sleep(3)
        await rtmsg.delete()

@bot.command(name="nuke")
@commands.has_guild_permissions(manage_channels=True)
async def nuke(ctx):
    temp_channel: discord.TextChannel = await ctx.channel.clone()
    await temp_channel.edit(position=ctx.channel.position)
    await ctx.channel.delete(reason="Nuke")
    embed = discord.Embed(color=discord.Colour.red(), description=f"{ctx.author.mention} Nuked This Channel!")
    embed.set_image(url="https://media.tenor.com/images/04dc5750f44e6d94c0a9f8eb8abf5421/tenor.gif")
    await temp_channel.send(embed=embed)

@bot.command(name="support")
async def support(ctx):
    await ctx.send('https://github.com/Jay-Surana\nContact = ! Real#4810')

warn_count = {}

@bot.command(name="warn")
@commands.has_guild_permissions(kick_members=True)
async def warn(ctx, user: discord.Member = None, *, reason=None):
    if user is None or reason is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot warn this user because their role is higher than or equal to yours.")
    else:
        print(f"Warning user {user.name} for {reason}...")

        if str(user) not in warn_count:
            warn_count[str(user)] = 1
        else:
            warn_count[str(user)] += 1

        embed = discord.Embed(
            title=f"{user.name} has been warned", color=discord.Colour.red())
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="This user has been warned",
                        value=f"{warn_count[str(user)]} time(s)")

        await ctx.send(content=None, embed=embed)

@bot.command(name="warncount")
async def warncount(ctx, user: discord.Member):
    if str(user) not in warn_count:
        warn_count[str(user)] = 0

        count = warn_count[str(user)]
        await ctx.send(f"{user.mention} has been warned {count} time(s)")

@bot.command(name="mute")
@commands.has_guild_permissions(kick_members=True)
async def mute(ctx, user: discord.Member = None, time: str = None):
    if user is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot mute this user because their role is higher than or equal to yours.")
    else:
        guild = ctx.guild
        mute_role = None

        for role in guild.roles:
            if role.name.lower() == "muted":
                mute_role = role
                break

        if mute_role in user.roles:
            await ctx.send("This user is already muted.")
        else:
            if not mute_role:
                await ctx.send("This server does not have a `Muted` Role. Creating one right now.")
                await ctx.send("This may take some time.")
                mute_role = await create_mute_role(guild)

            if time is None:
                await user.add_roles(mute_role)
                await ctx.send(f"User {user.mention} has been muted! They cannot speak.")
            else:
                time_unit = None
                parsed_time = None

                if "s" in time:
                    time_unit = "seconds"
                    parsed_time = time[0:(len(time) - 1)]
                elif "m" in time:
                    time_unit = "minutes"
                    parsed_time = time[0:(len(time) - 1)]
                elif "h" in time:
                    time_unit = "hours"
                    parsed_time = time[0:(len(time) - 1)]
                else:
                    time_unit = "minutes"  # default to minutes if user doesn't provide a time unit
                    parsed_time = time[0:len(time)]

                await user.add_roles(mute_role)
                await ctx.send(f"User {user.mention} has been muted for {parsed_time} {time_unit}! They cannot speak.")

                if time_unit == "seconds":
                    await asyncio.sleep(int(parsed_time))
                elif time_unit == "minutes":
                    await asyncio.sleep(int(parsed_time) * 60)
                elif time_unit == "hours":
                    await asyncio.sleep(int(parsed_time) * 3600)

                await user.remove_roles(mute_role)
                await ctx.send(f"User {user.mention} has been unmuted after {parsed_time} {time_unit}! They can speak now.")

@bot.command(name="unmute")
@commands.has_guild_permissions(kick_members=True)
async def unmute(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot unmute this user because their role is higher than or equal to yours.")
    else:
        guild = ctx.guild
        mute_role = None

        for role in guild.roles:
            if role.name.lower() == "muted":
                mute_role = role
                break

        if mute_role in user.roles:
            if not mute_role:
                mute_role = await create_mute_role(guild)

            await user.remove_roles(mute_role)
            await ctx.send(f"User {user.mention} has been unmuted! They can now speak.")

        else:
            await ctx.send("This user was never muted.")

@bot.command(name="ban")
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx, user: Union[discord.Member, int], *, reason=None):
    if not isinstance(user, int):
        if ctx.author.top_role.position <= user.top_role.position \
                and ctx.guild.owner_id != ctx.author.id:
            await ctx.send(
                "You cannot ban this user because their role "
                "is higher than or equal to yours."
            )
            return
    if isinstance(user, int):
        user_str = f"<@{user}>"
        user = discord.Object(id=user)
    else:
        user_str = user
    try:
        await user.send(
            f"You have been **banned** from **{ctx.guild}** server "
            f"due to the following reason:\n**{reason}**"
        )
    except Exception:
        pass
    await ctx.guild.ban(user, reason=reason)
    if reason:
        await ctx.send(
            f"User **{user_str}** has been banned for reason: "
            f"**{reason}**."
        )
    else:
        await ctx.send(f"User **{user_str}** has been banned.")

@bot.command(name="unban")
@commands.has_guild_permissions(ban_members=True)
@commands.guild_only()
async def unban(
    ctx, user: Union[discord.User, int, str],
    *, reason=None
):
    if isinstance(user, int):
        user_str = f"<@{user}>"
        user = discord.Object(id=user)
    else:
        user_str = user
        
    if isinstance(user, str):
        guild_bans = await ctx.guild.bans()
        try:
            name, tag = user.split('#')
        except:
            await ctx.send(
                "Please format the username like this: "
                "Username#0000"
            )
            return
        banned_user = utils.get(
            guild_bans, user__name=name,
            user__discriminator=tag
        )
        if banned_user is None:
            await ctx.send("I could not find that user in the bans.")
            return
        await ctx.guild.unban(banned_user.user)
        try:
            await banned_user.send(
                f"You have been unbanned with reason: {reason}"
            )
        except Exception:
            pass

    else:
        await ctx.guild.unban(user)
        try:
            await user.send(
                f"You have been unbanned with reason: {reason}"
            )
        except Exception:
            pass

    await ctx.send(f"Unbanned **{user_str}**")

@bot.command(name="kick")
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if user is None:
        await ctx.send("Insufficient arguments.")
    elif ctx.author.top_role.position <= user.top_role.position and ctx.guild.owner.id != ctx.author.id:
        await ctx.send("You cannot kick this user because their role is higher than or equal to yours.")
    else:
        await ctx.guild.kick(user, reason=reason)
        if reason:
            await ctx.send(f"User **{user}** has been kicked for reason: **{reason}**.")
        else:
            await ctx.send(f"User **{user}** has been kicked.")
        await user.send(f"You have been **kicked** from **{ctx.guild}** server due to the following reason:\n**{reason}**")

@bot.command(name="lockchannel", aliases=['lock'])
@commands.has_guild_permissions(manage_guild=True)
async def lockchannel(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    for role in ctx.guild.roles:
        if role.permissions.administrator:
            await channel.set_permissions(role, send_messages=True, read_messages=True)
        elif role.name == "@everyone":
            await channel.set_permissions(role, send_messages=False)

    await ctx.send(f"🔒The channel {channel.mention} has been locked")

@bot.command(name="unlockchannel", aliases=['unlock'])
@commands.has_guild_permissions(manage_guild=True)
async def unlockchannel(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    await channel.set_permissions(ctx.guild.roles[0], send_messages=True)

    await ctx.send(f"🔓The channel {channel.mention} has been unlocked")

@bot.command(name="slowmode", aliases=['sm'])
@commands.has_guild_permissions(manage_guild=True)
async def setdelay(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode in this channel to **{seconds}** seconds!")

@bot.command(name="serverinfo", aliases=['si'])
async def serverinfo(ctx):
    name = ctx.guild.name
    description = ctx.guild.description
    owner = ctx.guild.owner
    guild_id = ctx.guild.id
    region = ctx.guild.region
    member_count = ctx.guild.member_count
    icon = ctx.guild.icon_url

    embed = discord.Embed(
        title=f"{name} Server Information",
        description=description,
        color=discord.Colour.red()
        )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)

    await ctx.send(embed=embed)

@bot.command(name="userinfo", aliases=['ui', 'whois'])
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        color=discord.Colour.red(),
        timestamp=ctx.message.created_at,
        description=member.mention
    )

    embed.set_author(name=f"{member} Info")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(
        name="Registered At:",
        value=member.created_at.strftime("%a, %d %b %Y %I:%M %p"),
        inline=False
    )
    embed.add_field(
        name="Joined Server At:",
        value=member.joined_at.strftime("%a, %d %b %Y %I:%M %p"),
        inline=False
    )

    roles = " ".join([role.mention for role in member.roles if role != ctx.guild.default_role])

    if len(roles.strip()) == 0:
        roles = "This user does not have any roles"

    embed.add_field(
        name=f"{len(member.roles)-1} Roles",
        value=roles,
        inline=False
    )
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)

@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def poll(ctx,*,msg):
    channel = ctx.channel
    try:
        op1, op2 = msg.split("or")
        txt = f"React with 👍🏼 {op1} or 👎🏼 {op2}"
    except:
        await channel.send("Correct Syntex: [Choice1] or [Choice2]")
        return
  
    embed = discord.Embed(title= "poll", description=txt, color= discord.Colour.red())
    message_ = await channel.send(embed=embed)
    await message_.add_reaction("👍🏼")
    await message_.add_reaction("👎🏼")
    await ctx.message.delete()

@bot.command(pass_context = True)
@commands.has_permissions(manage_channels = True)
async def announce(ctx, channel: discord.TextChannel,*,msg):
    await ctx.send(f'Message sended to {channel}')
    embed = discord.Embed(
    description = msg,
    colour= discord.Colour.red())
    await channel.send(embed=embed)

@bot.command(name="addrole",aliases=['ad'])
@commands.has_permissions(manage_roles = True)
async def addrole(ctx,role: discord.Role ,user: discord.Member):
    await user.add_roles(role)
    await ctx.send(f"Successfully Added {role.mention} to {user.mention}")

@bot.command(name= "removerole",aliases=['rd'])
@commands.has_permissions(manage_roles = True)
async def removerole(ctx,role: discord.Role ,user: discord.Member):
    await user.remove_roles(role)
    await ctx.send(f"Successfully Removed {role.mention} to {user.mention}")

@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx , *, msg):
    await ctx.message.delete() 
    await ctx.send("{}".format(msg))

@bot.command(name="avatar", aliases=['av'])
async def avatar(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    aembed = discord.Embed(
        color=discord.Colour.red(),
        title=f"{user}"
    )

    aembed.set_image(url=f"{user.avatar_url}")
    await ctx.send(embed=aembed)

#Error handler
@bot.event
async def on_command_error(ctx, error):
    try:
        error = error.original
    except Exception:
        pass
    if type(error) is discord.ext.commands.errors.CommandNotFound:
        return
    elif type(error) is discord.ext.commands.errors.BadArgument:
        pass
    elif type(error) is discord.ext.commands.errors.MissingRequiredArgument:
        pass
    elif type(error) is discord.ext.commands.errors.NoPrivateMessage:
        pass
    elif type(error) is discord.ext.commands.errors.MissingPermissions:
        pass
    elif type(error) is discord.ext.commands.errors.NotOwner:
        pass
    elif type(error) is discord.ext.commands.errors.CommandOnCooldown:
        pass
    elif type(error) is discord.ext.commands.errors.ChannelNotFound:
        pass
    elif type(error) is discord.ext.commands.errors.BadUnionArgument:
        pass
    elif type(error) is discord.ext.commands.errors.BotMissingPermissions:
        pass
    elif type(error) is discord.errors.Forbidden:
        error = "I don't have permission to do that!"
    else:
        print(f"Error {type(error)}: {error}")
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

        embed = discord.Embed(
            title='Error!',
            description='An unexpected error ocurred.\
                Please report this to the dev.',
        )
        embed.add_field(
            name='Error Message:',
            value=f"{type(error)}:\n{error}",
            inline=False
        )
    await ctx.send(f"{error}")

bot.run(TOKEN)
