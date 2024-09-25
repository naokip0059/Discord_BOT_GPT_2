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

# メッセージ履歴の管理
message_history = []

@bot.event
async def on_message(message):
    # BOT自身がメンションされたか確認
    if bot.user in message.mentions:
        # メンションされたメッセージから質問を抽出
        question = message.content.replace(f'<@!{bot.user.id}>', '').strip()  # メンションを取り除く
        if question:
            # 質問を履歴に追加
            message_history.append({"role": "user", "content": question})
            
            # OpenAIに履歴を渡す
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message_history
            )
            answer = response.choices[0].message['content'].strip()  # 応答を整形
            
            # 履歴にBOTの応答を追加
            message_history.append({"role": "assistant", "content": answer})
            
            await message.channel.send(answer)

    await bot.process_commands(message)  # コマンドの処理を続ける

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# Discordのトークンを取得してBOTを起動
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
