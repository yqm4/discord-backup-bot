
import discord
from discord.ext import commands

TOKEN = "BOT_TOKEN"
A_SERVER_ID = A_SERVER_ID
B_SERVER_ID = B_SERVER_ID 

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"ログインしました: {bot.user}（スラッシュコマンド同期: {len(synced)}件）")

@bot.tree.command(name="transfer_logs_webhook", description="Aサーバーの過去ログをWebhook経由でBサーバーにコピー（全チャンネル）")
async def transfer_logs_webhook(interaction: discord.Interaction, limit: int = 50):
    await interaction.response.send_message(f"Webhookを使って過去ログを複製中...（各チャンネル最大 {limit} 件）", ephemeral=True)

    a_guild = bot.get_guild(A_SERVER_ID)
    b_guild = bot.get_guild(B_SERVER_ID)

    if not a_guild or not b_guild:
        await interaction.followup.send("サーバーが見つかりません。")
        return

    b_channels = {c.name: c for c in b_guild.text_channels}

    for a_channel in a_guild.text_channels:
        if a_channel.name not in b_channels:
            print(f"スキップ: {a_channel.name}（Bに対応チャンネルなし）")
            continue

        b_channel = b_channels[a_channel.name]
        await interaction.followup.send(f"チャンネル {a_channel.name} のログをコピー中...", ephemeral=True)

        webhooks = await b_channel.webhooks()
        webhook = webhooks[0] if webhooks else await b_channel.create_webhook(name="Log Cloner")

        async for message in a_channel.history(limit=limit, oldest_first=True):
            files = [await attachment.to_file() for attachment in message.attachments]

            if not message.content and not files and not message.embeds:
                continue

            content = message.content or ""
            if len(content) > 2000:
                content = content[:1997] + "..."

            await webhook.send(
                content=content or None,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                files=files,
                embeds=message.embeds
            )

    await interaction.followup.send("Webhookによる過去ログ複製が完了しました！", ephemeral=True)

@bot.tree.command(name="transfer_logs_webhook_one", description="指定したチャンネルの過去ログをWebhookでコピー")
async def transfer_logs_webhook_one(interaction: discord.Interaction, channel_name: str, limit: int = 50):
    await interaction.response.send_message(f"{channel_name} の過去ログを複製中...（最大 {limit} 件）", ephemeral=True)

    a_guild = bot.get_guild(A_SERVER_ID)
    b_guild = bot.get_guild(B_SERVER_ID)

    if not a_guild or not b_guild:
        await interaction.followup.send("サーバーが見つかりません。")
        return

    a_channel = discord.utils.get(a_guild.text_channels, name=channel_name)
    b_channel = discord.utils.get(b_guild.text_channels, name=channel_name)

    if not a_channel:
        await interaction.followup.send(f"Aサーバーにチャンネル {channel_name} が見つかりません。")
        return
    if not b_channel:
        await interaction.followup.send(f"Bサーバーにチャンネル {channel_name} が見つかりません。")
        return

    webhooks = await b_channel.webhooks()
    webhook = webhooks[0] if webhooks else await b_channel.create_webhook(name="Log Cloner")

    async for message in a_channel.history(limit=limit, oldest_first=True):
        files = [await attachment.to_file() for attachment in message.attachments]

        if not message.content and not files and not message.embeds:
            continue

        content = message.content or ""
        if len(content) > 2000:
            content = content[:1997] + "..."

        await webhook.send(
            content=content or None,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
            files=files,
            embeds=message.embeds
        )

    await interaction.followup.send(f"{channel_name} の過去ログ複製が完了しました！", ephemeral=True)

bot.run(TOKEN)
