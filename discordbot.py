import discord
import traceback
from discord.ext import commands
from os import getenv
import openai

# OpenAIのAPIキーを設定
openai.api_key = getenv('OPENAI_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# OpenAI GPT-3を使った応答を追加
@bot.command()
async def ask(ctx, *, question):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 使用するGPTのモデル
            prompt=question,  # ユーザーが送った質問
            max_tokens=100  # 応答のトークン数制限
        )
        answer = response.choices[0].text.strip()  # 応答を整形
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {str(e)}")

# Discordのトークンを取得してBOTを起動
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
