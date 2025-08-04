
import discord
from discord.ext import commands

TOKEN = "TOKEN"
A_SERVER_ID = A_SERVER_ID
B_SERVER_ID = B_SERVER_ID 

intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"ログインしました: {bot.user}（スラッシュコマンド同期: {len(synced)}件）")

@bot.tree.command(name="clone_all", description="Bサーバーを初期化して、Aサーバーの構造を複製します")
async def clone_all(interaction: discord.Interaction):
    await interaction.response.send_message("Bサーバーを初期化して複製を開始します...", ephemeral=True)

    a_guild = bot.get_guild(A_SERVER_ID)
    b_guild = bot.get_guild(B_SERVER_ID)

    if not a_guild or not b_guild:
        await interaction.followup.send("サーバーが見つかりません。")
        return

   
    for channel in b_guild.channels:
        await channel.delete()
    print("Bサーバーのチャンネルを削除しました")

    for role in sorted(b_guild.roles, key=lambda r: r.position, reverse=True):
        if not role.is_default():  
            try:
                await role.delete()
            except discord.Forbidden:
                print(f"ロール削除失敗: {role.name}")
    print("Bサーバーのロールを削除しました")

 
    role_map = {}
    for role in sorted(a_guild.roles, key=lambda r: r.position):
        if role.is_default():
            role_map[role.id] = b_guild.default_role
            continue
        new_role = await b_guild.create_role(
            name=role.name,
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable
        )
        role_map[role.id] = new_role

   
    category_map = {}
    for category in a_guild.categories:
        overwrites = {role_map[role.id]: overwrite for role, overwrite in category.overwrites.items() if isinstance(role, discord.Role)}
        new_category = await b_guild.create_category(name=category.name, overwrites=overwrites)
        category_map[category.id] = new_category

    
    for channel in a_guild.text_channels:
        overwrites = {role_map[role.id]: overwrite for role, overwrite in channel.overwrites.items() if isinstance(role, discord.Role)}
        await b_guild.create_text_channel(
            name=channel.name,
            category=category_map.get(channel.category_id),
            overwrites=overwrites,
            topic=channel.topic
        )

   
    for channel in a_guild.voice_channels:
        overwrites = {role_map[role.id]: overwrite for role, overwrite in channel.overwrites.items() if isinstance(role, discord.Role)}
        await b_guild.create_voice_channel(
            name=channel.name,
            category=category_map.get(channel.category_id),
            overwrites=overwrites,
            bitrate=channel.bitrate,
            user_limit=channel.user_limit
        )

    await interaction.followup.send("Bサーバーを初期化し、Aサーバーの複製が完了しました！")

bot.run("TOKEN")
