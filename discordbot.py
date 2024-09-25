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
async def on_message(message):
    # BOT自身がメンションされたか確認
    if bot.user in message.mentions:
        # メンションされたメッセージから質問を抽出
        question = message.content.replace(f'<@!{bot.user.id}>', '').strip()  # メンションを取り除く
        if question:
            await ask_weather(message.channel, question)  # 質問に基づく処理を実行

    await bot.process_commands(message)  # コマンドの処理を続ける

async def ask_weather(channel, question):
    # ここに天気APIを呼び出すコードを追加
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    answer = response.choices[0].message['content'].strip()  # 応答を整形
    await channel.send(answer)

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
        # ChatCompletionを使用して質問に対する応答を取得
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 使用するモデルを指定
            messages=[
                {"role": "user", "content": question}  # ユーザーのメッセージを設定
            ]
        )
        answer = response.choices[0].message['content'].strip()  # 応答を整形
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {str(e)}")

# Discordのトークンを取得してBOTを起動
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
