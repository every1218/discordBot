import discord
import datetime
import threading
from flask import Flask
from dotenv import load_dotenv
import os

from user_data import load_user_data, save_user_data
from commands import handle_simple_commands
from economy import handle_money, handle_hourly, handle_minutely, handle_attendance, handle_rank, handle_transfer
from games import handle_even_odd, handle_jackpot, handle_lotto,handle_blackjack
#from games import handle_bet_prediction, handle_call_my_name, handle_sutda
from champion import handle_champion_command
from chat import llm_chat

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# Flask 웹서버 생성
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

intents = discord.Intents.all()
client = discord.Client(intents=intents)

today = datetime.datetime.now() + datetime.timedelta(hours=9) - datetime.timedelta(days=1)

usernames, idA, moneyA, levelA, timeA, timeB, timeC = load_user_data()

@client.event
async def on_ready():
    print("봇 준비 완료!")
    print(client.user)
    print("==========")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(".도움말"))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # 봇이 멘션되었을 때 LLM 기능 호출
    if client.user in message.mentions:
        query = message.content.replace(f'<@{client.user.id}>', '').strip()
        async with message.channel.typing():
            answer = await llm_chat(query)
            await message.reply(answer, mention_author=False)
        return
        
    ID = str(message.author.id)
    
    # 단순 명령어 처리
    if await handle_simple_commands(message, today):
        return

    if message.content.startswith(".카운터"):
        await handle_champion_command(message)
    
    # 경제 관련 명령어 분기
    if message.content == ".돈":
        await handle_money(message, idA, moneyA, levelA)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    if message.content == ".시급":
        await handle_hourly(message, usernames, idA, moneyA, timeA, levelA, timeB, timeC)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    if message.content == ".분급":
        await handle_minutely(message, usernames, idA, moneyA, timeA, levelA, timeB, timeC)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    if message.content == ".출석":
        await handle_attendance(message, usernames, idA, moneyA, timeA, levelA, timeB, timeC)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    if message.content == ".순위":
        await handle_rank(message, idA, moneyA, levelA)
        return
    if message.content.startswith(".송금"):
        await handle_transfer(message, idA, moneyA)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    
    # 게임 관련 명령어 분기
    if message.content.startswith(".홀짝"):
        await handle_even_odd(message, idA, moneyA)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    if message.content == ".잭팟":
        await handle_jackpot(message, idA, moneyA)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    if message.content.startswith(".복권"):
        await handle_lotto(message, idA, moneyA)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    if message.content.startswith(".블랙잭"):
        await handle_blackjack(client, message, idA, moneyA)
        save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
        return
    # if message.content.startswith(".승부예측"):
    #     await handle_bet_prediction(message, idA, moneyA)
    #     save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
    #     return
    # if message.content.startswith(".콜마이네임"):
    #     await handle_call_my_name(message)
    #     return
    # if message.content == ".섯다":
    #     await handle_sutda(message, idA, moneyA, timeA, levelA, timeB, timeC)
    #     save_user_data(usernames, idA, moneyA, levelA, timeA, timeB, timeC)
    #     return

keep_alive()
client.run(token)
