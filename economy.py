import discord
import random
import time

# 돈 확인
async def handle_money(message, idA, moneyA, levelA):
    ID = str(message.author.id)
    if ID in idA:
        embed = discord.Embed(title=message.author.name, description="자산 : "+format(moneyA[idA.index(ID)], ",d") + "원\n레벨 : "+format(levelA[idA.index(ID)]), color=0x118811)
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(title=message.author.name, description="자산 : 0원\n레벨 : 0", color=0x118811)
        await message.channel.send(embed=embed)

# 시급
async def handle_hourly(message, usernames, idA, moneyA, timeA, levelA, timeB, timeC):
    ID = str(message.author.id)
    TIME = int(time.time())
    random_money = random.randrange(1000000, 10000000)
    if ID in idA:
        if TIME - int(timeA[idA.index(ID)]) < 3600:
            embed = discord.Embed(title=message.author.name, description=f"1시간마다 받을 수 있습니다.\n{int((3600 - (TIME - int(timeA[idA.index(ID)])))/60)}분", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        elif TIME - int(timeA[idA.index(ID)]) >= 3600:
            timeA[idA.index(ID)] = int(time.time())
    if ID in idA:
        give = int(random_money * (1+ levelA[idA.index(ID)]/10))
        moneyA[idA.index(ID)] += give
    else:
        give = random_money
        usernames.append(message.author.name)
        idA.append(ID)
        moneyA.append(give)
        levelA.append(0)
        timeA.append(int(time.time()))
        timeB.append(int(0))
        timeC.append(int(0))
    embed = discord.Embed(title=message.author.name,description=f"**{format(give, ',d')}원** 받았습니다. `[자산: {format(moneyA[idA.index(ID)], ',d')}]`",color=0x00FF00)
    await message.channel.send(embed=embed)

# 분급
async def handle_minutely(message, usernames, idA, moneyA, timeA, levelA, timeB, timeC):
    ID = str(message.author.id)
    TIME = int(time.time())
    random_money = random.randrange(1000000, 10000000)
    if ID in idA:
        if TIME - int(timeC[idA.index(ID)]) < 60:
            embed = discord.Embed(title=message.author.name, description=f"1분마다 받을 수 있습니다.\n{60-(TIME - int(timeC[idA.index(ID)]))}초", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        elif TIME - int(timeC[idA.index(ID)]) >= 60:
            timeC[idA.index(ID)] = int(time.time())
    if ID in idA:
        give = int(random_money * (1+ levelA[idA.index(ID)]/10))
        moneyA[idA.index(ID)] += give
    else:
        give = random_money
        usernames.append(message.author.name)
        idA.append(ID)
        moneyA.append(give)
        levelA.append(0)
        timeA.append(0)
        timeB.append(0)
        timeC.append(int(time.time()))
    embed = discord.Embed(title=message.author.name,description=f"**{format(give, ',d')}원** 받았습니다. `[자산: {format(moneyA[idA.index(ID)], ',d')}]`",color=0x00FF00)
    await message.channel.send(embed=embed)

# 출석
async def handle_attendance(message, usernames, idA, moneyA, timeA, levelA, timeB, timeC):
    ID = str(message.author.id)
    TIME = int(time.time())
    if ID in idA:
        if TIME - int(timeB[idA.index(ID)]) < 86400:
            embed = discord.Embed(title=message.author.name, description=f"하루에 한번 출석할 수 있습니다.\n{int((86400 - (TIME - int(timeB[idA.index(ID)])))/3600)}시간", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        elif TIME - int(timeB[idA.index(ID)]) >= 86400:
            timeB[idA.index(ID)] = int(time.time())
    if ID in idA:
        levelA[idA.index(ID)] += 1
    else:
        usernames.append(message.author.name)
        idA.append(ID)
        moneyA.append(0)
        levelA.append(1)
        timeA.append(0)
        timeB.append(int(time.time()))
        timeC.append(0)
    embed = discord.Embed(title=message.author.name, description="레벨이 올랐습니다.", color=0x00FF00)
    await message.channel.send(embed=embed)

# 순위
async def handle_rank(message, idA, moneyA, levelA):
    # 현재 서버(길드) 멤버 ID만 추출
    member_dict = {str(member.id): member for member in message.guild.members if not member.bot}
    # 서버에 실제로 존재하는 유저만 필터링
    rankA = [
        [idA[i], moneyA[i], levelA[i]]
        for i in range(len(idA))
        if idA[i] in member_dict
    ]
    # 돈 기준 내림차순 정렬
    rankA = sorted(rankA, reverse=True, key=lambda x: x[1])

    embed = discord.Embed(
        title=f"🏆 {message.guild.name} 서버 돈 순위 TOP 10",
        color=0xFFD700
    )
    medal = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    for i in range(min(10, len(rankA))):
        user_id = rankA[i][0]
        member = member_dict.get(user_id)
        # 이름: 닉네임(서버 닉) 있으면 그걸, 없으면 디스코드 이름
        if member:
            name = member.display_name
        else:
            name = f"<@{user_id}>"
        name_underline = f"{name}"
        level = rankA[i][2]
        money = format(rankA[i][1], ",d")
        # 한 줄로: 🥇 1위 __이름__ (Lv.0) 💰 `39,947,100원`
        line = f"{medal[i]} {i+1}위 {name_underline} (Lv.{level}) 💰`{money}원`"
        embed.add_field(
            name=line,
            value="",
            inline=False
        )
    if not rankA:
        embed.description = "서버 내 등록된 유저가 없습니다."
    await message.channel.send(embed=embed)

# 송금
async def handle_transfer(message, idA, moneyA):
    ID = str(message.author.id)
    money = message.content.split(" ")[1]
    person = str(message.content.split(" ")[2])
    person = person.strip("<"">""@")
    if moneyA[idA.index(ID)] < int(money):
        embed = discord.Embed(title=message.author.name, description="잔액이 부족합니다", color=0xFF0000)
        await message.channel.send(embed=embed)
        return
    if person in idA:
        moneyA[idA.index(ID)] -= int(money)
        moneyA[idA.index(person)] += int(money)
        embed = discord.Embed(title=message.author.name, description=f"**{format(int(money),',d')}원**을 송금했습니다ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`", color=0x118811)
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="오류", description="송금을 실패했습니다", color=0xFF0000)
        await message.channel.send(embed=embed) 