import os
import discord
from discord.ext import commands
import random

# ===== Bot設定 =====
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== Valorantエージェント =====
valo_agents = {
    "デュエリスト": ["ジェット","レイズ","フェニックス","レイナ","ヨル","ネオン","アイソ","ウェイレイ"],
    "イニシエーター": ["ブリーチ","ソーヴァ","スカイ","KAY／O","フェイド","ゲッコー","テホ"],
    "コントローラー": ["オーメン","ブリムストーン","ヴァイパー","アストラ","ハーバー","クローヴ"],
    "センチネル": ["セージ","サイファー","キルジョイ","チェンバー","デッドロック","ヴァイス"]
}

# ===== APEXエージェント（ロール関係なしで3人ランダム） =====
apex_agents = [
    "バンガロール","レヴナント","ヒューズ","マッドマギー","バリスティック",
    "パスファインダー","レイス","オクタン","ホライゾン","アッシュ","オルター",
    "ブラッドハウンド","クリプト","ヴァルキリー","シア","ヴァンテージ","スパロー",
    "ジブラルタル","ライフライン","ミラージュ","ローバ","ニューキャッスル","コンジット",
    "コースティック","ワットソン","ランパート","カタリスト"
]

# ===== Bot起動時 =====
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot logged in as {bot.user}")

# ===== Valorantコマンド =====
@bot.tree.command(name="randomteam_valo", description="Valorantエージェントをカテゴリごとにランダムで選択（重複なし）")
async def randomteam_valo(interaction: discord.Interaction):
    result = {}
    selected_agents = set()  # 重複防止

    # 各カテゴリから1人ずつ選択
    for category, agent_list in valo_agents.items():
        choices = [a for a in agent_list if a not in selected_agents]
        chosen = random.choice(choices)
        result[category] = chosen
        selected_agents.add(chosen)

    # 全カテゴリから1人（重複なし）
    all_agents = [a for a in sum(valo_agents.values(), []) if a not in selected_agents]
    result["全カテゴリ"] = random.choice(all_agents)

    # Embed作成
    embed = discord.Embed(title="🎲 Valorant ランダムチーム生成", color=discord.Color.blurple())
    for cat, agent in result.items():
        embed.add_field(name=cat, value=agent, inline=False)
    embed.set_footer(text="Botによるランダムチーム生成")

    await interaction.response.send_message(embed=embed)

# ===== APEXコマンド =====
@bot.tree.command(name="random_apex3", description="APEXエージェントを3人ランダム選択")
async def random_apex3(interaction: discord.Interaction):
    chosen = random.sample(apex_agents, 3)
    embed = discord.Embed(
        title="🎲 APEX ランダム3人選択",
        description="\n".join(f"• {a}" for a in chosen),
        color=discord.Color.orange()
    )
    embed.set_footer(text="Botによるランダム選択")
    await interaction.response.send_message(embed=embed)

# ===== Bot起動 =====
bot.run(os.getenv("DISCORD_TOKEN"))
