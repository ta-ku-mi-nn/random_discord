import os
import discord
from discord import app_commands
from discord.ext import commands
import random

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# エージェントリスト
agents = {
    "デュエリスト": [
        "ジェット", "レイズ", "フェニックス", "レイナ", "ヨル", "ネオン", "アイソ", "ウェイレイ"
    ],
    "イニシエーター": [
        "ブリーチ", "ソーヴァ", "スカイ", "KAY／O", "フェイド", "ゲッコー", "テホ"
    ],
    "コントローラー": [
        "オーメン", "ブリムストーン", "ヴァイパー", "アストラ", "ハーバー", "クローヴ"
    ],
    "センチネル": [
        "セージ", "サイファー", "キルジョイ", "チェンバー", "デッドロック", "ヴァイス"
    ]
}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="randomteam_valo", description="Valorantエージェントをカテゴリごとにランダムで選択（重複なし）")
async def randomteam_valo(interaction: discord.Interaction):
    result = {}
    selected_agents = set()  # 重複防止

    # 各カテゴリから1人ずつ選択
    for category, agent_list in agents.items():
        choices = [a for a in agent_list if a not in selected_agents]
        chosen = random.choice(choices)
        result[category] = chosen
        selected_agents.add(chosen)

    # 全カテゴリから1人（重複なし）
    all_agents = [a for a in sum(agents.values(), []) if a not in selected_agents]
    result["全カテゴリ"] = random.choice(all_agents)

    # Embed作成（色はすべてデフォルト）
    embeds = []
    for cat, agent in result.items():
        embed = discord.Embed(
            title=f"🎲 {cat} - ランダム選択",
            description=agent
        )
        embed.set_footer(text="Botによるランダムチーム生成")
        embeds.append(embed)
    
    # Embedを順番に送信
    for embed in embeds:
        await interaction.channel.send(embed=embed)
    
    await interaction.response.send_message("✅ ランダムチーム生成完了！", ephemeral=True)

# Botトークンは環境変数から
bot.run(os.getenv("DISCORD_TOKEN"))
