import discord
from discord import app_commands
from discord.ext import commands
import random

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# カテゴリごとのワードリスト
categories = {
    "果物": ["りんご", "みかん", "バナナ", "ぶどう", "メロン", "スイカ", "いちご", "キウイ", "マンゴー"],
    "動物": ["ねこ", "いぬ", "うさぎ", "とり", "さる", "ぞう", "ライオン", "ペンギン", "カンガルー"],
    "色": ["赤", "青", "緑", "黄色", "紫", "オレンジ", "ピンク", "白", "黒"]
}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

# スラッシュコマンド定義
@bot.tree.command(name="randomwords", description="カテゴリと数を選んでランダムワードを生成します")
@app_commands.choices(
    category=[
        app_commands.Choice(name="果物", value="果物"),
        app_commands.Choice(name="動物", value="動物"),
        app_commands.Choice(name="色", value="色"),
    ],
    count=[
        app_commands.Choice(name="1個", value=1),
        app_commands.Choice(name="2個", value=2),
        app_commands.Choice(name="3個", value=3),
        app_commands.Choice(name="4個", value=4),
        app_commands.Choice(name="5個", value=5),
    ]
)
async def randomwords(
    interaction: discord.Interaction,
    category: app_commands.Choice[str],
    count: app_commands.Choice[int]
):
    chosen = random.sample(categories[category.value], count.value)

    embed = discord.Embed(
        title=f"🎲 ランダムワード生成（{category.value} - {count.value}個）",
        description="\n".join(f"• {word}" for word in chosen),
        color=discord.Color.green() if category.value == "果物" else (
            discord.Color.orange() if category.value == "動物" else discord.Color.blue()
        )
    )
    embed.set_footer(text="Botによるランダムワード生成")
    
    await interaction.response.send_message(embed=embed)

bot.run("YOUR_BOT_TOKEN")
