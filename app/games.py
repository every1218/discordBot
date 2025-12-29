import discord
import random
import asyncio
import time

def get_dice_emoji(num):
    return ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣'][num-1]

# 홀짝 게임
async def handle_even_odd(message, idA, moneyA):
    ID = str(message.author.id)
    try:
        expectation = message.content.split(" ")[1]
        betting = int(message.content.split(" ")[2])
    except:
        embed = discord.Embed(title="🎲 홀짝 게임", 
                            description="**명령어 형식:** `.홀짝 (홀/짝) (금액)`\n\n**예시:** `.홀짝 홀 1000`", 
                            color=0x3498db)
        embed.set_footer(text="홀수: 1,3,5 | 짝수: 2,4,6")
        await message.channel.send(embed=embed)
        return
    
    # 입력 검증
    if not (expectation == "홀" or expectation == "짝"):
        embed = discord.Embed(title="❌ 입력 오류", 
                            description="**홀** 또는 **짝**만 입력해주세요!", 
                            color=0xFF0000)
        embed.add_field(name="올바른 형식", value="`.홀짝 홀 1000`\n`.홀짝 짝 5000`")
        await message.channel.send(embed=embed)
        return
    
    # 돈 부족 체크
    if not ID in idA or moneyA[idA.index(ID)] - betting < 0:
        embed = discord.Embed(title="💰 잔액 부족", 
                            description=f"**현재 자산:** {format(moneyA[idA.index(ID)] if ID in idA else 0, ',d')}원\n**필요 금액:** {format(betting, ',d')}원", 
                            color=0xFF0000)
        await message.channel.send(embed=embed)
        return
    
    # 게임 시작
    start_embed = discord.Embed(title="🎲 홀짝 게임 시작!", 
                              description=f"**{message.author.display_name}**님이 **{expectation}**에 **{format(betting, ',d')}원** 베팅!\nㅤ", 
                              color=0x3498db)
    start_embed.add_field(name="🎯 예측", value=expectation, inline=True)
    start_embed.add_field(name="💰 베팅 금액", value=f"{format(betting, ',d')}원", inline=True)
    start_embed.add_field(name="💵 현재 자산", value=f"{format(moneyA[idA.index(ID)], ',d')}원", inline=True)
    await message.channel.send(embed=start_embed)
    
    # 주사위 굴리는 애니메이션
    dice_emojis = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    animation_msg = await message.channel.send("🎲 주사위를 굴리는 중...")
    
    for i in range(5):  # 5번 애니메이션
        random_dice = random.choice(dice_emojis)
        await animation_msg.edit(content=f"🎲 주사위를 굴리는 중... {random_dice}")
        await asyncio.sleep(0.5)
    
    # 최종 결과
    temp = random.randrange(1, 7)
    final_dice = get_dice_emoji(temp)
    result = "홀" if temp % 2 == 1 else "짝"
    
    # 승패 판정
    if expectation == result:
        # 승리
        moneyA[idA.index(ID)] += betting
        win_embed = discord.Embed(title="🎉 홀짝 성공!", 
                                description=f"**축하합니다!** {expectation}을 맞추셨습니다!\nㅤ", 
                                color=0x00FF00)
        win_embed.add_field(name="💰 획득", value=f"+{format(betting, ',d')}원", inline=True)
        win_embed.add_field(name="💵 자산", value=f"{format(moneyA[idA.index(ID)], ',d')}원", inline=True)
        await animation_msg.edit(content=f"🎲 최종 결과: {final_dice}")
        await message.channel.send(embed=win_embed, reference=message)
    else:
        # 패배
        moneyA[idA.index(ID)] -= betting
        lose_embed = discord.Embed(title="💔 홀짝 실패", 
                                 description=f"**아쉽네요...**  {expectation}이 아닌 {result}이 나왔습니다.\nㅤ", 
                                 color=0xFF0000)
        lose_embed.add_field(name="💰 손실", value=f"-{format(betting, ',d')}원", inline=True)
        lose_embed.add_field(name="💵 자산", value=f"{format(moneyA[idA.index(ID)], ',d')}원", inline=True)
        await animation_msg.edit(content=f"🎲 최종 결과: {final_dice}")
        await message.channel.send(embed=lose_embed, reference=message)

# 잭팟 게임
async def handle_jackpot(message, idA, moneyA):
    ID = str(message.author.id)
    betting = 10000
    jackpot= ['🦑','🐳','🦑','🦑','🐧','🦑','🐳','🦑','🦑','🐳']
    animal = ['','','']
    
    # 돈 부족 체크
    if not ID in idA or moneyA[idA.index(ID)] - betting < 0:
        embed = discord.Embed(title="💰 잔액 부족", 
                            description=f"**현재 자산:** {format(moneyA[idA.index(ID)] if ID in idA else 0, ',d')}원\n**필요 금액:** {format(betting, ',d')}원", 
                            color=0xFF0000)
        embed.set_footer(text="잭팟 게임은 1만원이 필요합니다")
        await message.channel.send(embed=embed)
        return
    
    # 베팅 차감
    moneyA[idA.index(ID)] -= betting
    
    # 슬롯머신 애니메이션 (기존 텍스트 방식)
    msg = await message.channel.send("❓          ❓          ❓", reference=message)
    await asyncio.sleep(1)

    animal[0] = random.choice(jackpot)
    await msg.edit(content=f"{animal[0]}          ❓          ❓")
    await asyncio.sleep(1)
    
    animal[1] = random.choice(jackpot)
    await msg.edit(content=f"{animal[0]}          {animal[1]}          ❓")
    await asyncio.sleep(1)
    
    animal[2] = random.choice(jackpot)
    await msg.edit(content=f"{animal[0]}          {animal[1]}          {animal[2]}")
    await asyncio.sleep(1)
    
    # 결과 판정
    if animal[0] == animal[1] == animal[2] == '🦑':
        # 🦑 잭팟 (3배)
        earned = 30000
        moneyA[idA.index(ID)] += earned
        win_embed = discord.Embed(title="🎉 🦑 잭팟 당첨!", 
                                description=f"**축하합니다!** 🦑 잭팟을 맞추셨습니다!\nㅤ", 
                                color=0x00FF00)
        win_embed.add_field(name="💰 획득", value=f"+{format(earned, ',d')}원", inline=True)
        win_embed.add_field(name="💵 자산", value=f"{format(moneyA[idA.index(ID)], ',d')}원", inline=True)
        
    elif animal[0] == animal[1] == animal[2] == '🐳':
        # 🐳 잭팟 (20배)
        earned = 200000
        moneyA[idA.index(ID)] += earned
        win_embed = discord.Embed(title="🎉 🐳 잭팟 당첨!", 
                                description=f"**대박!** 🐳 잭팟을 맞추셨습니다!\nㅤ", 
                                color=0x00FF00)
        win_embed.add_field(name="💰 획득", value=f"+{format(earned, ',d')}원", inline=True)
        win_embed.add_field(name="💵 자산", value=f"{format(moneyA[idA.index(ID)], ',d')}원", inline=True)
        
    elif animal[0] == animal[1] == animal[2] == '🐧':
        # 🐧 잭팟 (300배)
        earned = 3000000
        moneyA[idA.index(ID)] += earned
        win_embed = discord.Embed(title="🎉 🐧 잭팟 당첨!", 
                                description=f"**전설!** 🐧 잭팟을 맞추셨습니다!\nㅤ", 
                                color=0xFFD700)
        win_embed.add_field(name="💰 획득", value=f"+{format(earned, ',d')}원", inline=True)
        win_embed.add_field(name="💵 자산", value=f"{format(moneyA[idA.index(ID)], ',d')}원", inline=True)
        
    else:
        # 꽝
        lose_embed = discord.Embed(title="💔 꽝!", 
                                 description=f"아쉽지만 3개가 일치하지 않았습니다.\nㅤ", 
                                 color=0xFF0000)
        lose_embed.add_field(name="💰 손실", value=f"-{format(betting, ',d')}원", inline=True)
        lose_embed.add_field(name="💵 자산", value=f"{format(moneyA[idA.index(ID)], ',d')}원", inline=True)
        await message.channel.send(embed=lose_embed)
        return
    
    # 당첨 시 결과 표시
    await message.channel.send(embed=win_embed)

# 복권 게임
async def handle_lotto(message, idA, moneyA):
    ID = str(message.author.id)
    betting = 5000
    lotto = []
    input_num = []
    result = 0
    money = 0
    if not ID in idA or moneyA[idA.index(ID)] - betting < 0:
        embed = discord.Embed(title=message.author.display_name, description="돈이 부족합니다!", color=0xFF0000)
        await message.channel.send(embed=embed)
        return
    try:
        for i in range(0,6):
            n = int(message.content.split(" ")[i+1])
            if 1 <= n <= 20:
                input_num.append(n)
            else:
                embed = discord.Embed(title=message.author.display_name, description="1~20 사이 번호를 입력하세요", color=0xFF0000)
                await message.channel.send(embed=embed)
                return
    except:
        await message.channel.send(".복권 [숫자1] [숫자2] [숫자3] [숫자4] [숫자5] [숫자6] 형식으로 입력해주세요\n1~20사이 숫자 입력")
        return
    while True:
        num = random.randint(1,20)
        if num not in lotto:
            lotto.append(num)
        if len(lotto) == 6:
            break
    for i in range(0,6):
        if input_num[i] in lotto:
            result+=1
    moneyA[idA.index(ID)] -= betting
    if result == 3:
        money = 15000
        moneyA[idA.index(ID)] += money
    elif result == 4:
        money = 60000
        moneyA[idA.index(ID)] += money
    elif result == 5:
        money = 1000000
        moneyA[idA.index(ID)] += money
    elif result == 6:
        money = 250000000
        moneyA[idA.index(ID)] += money
    input_num.sort()
    lotto.sort()
    if result <3:
        embed = discord.Embed(title=message.author.display_name,description=f"**{result}개 꽝!**ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`\n\n📥입력 : {input_num}\n📤복권 : {lotto}",color=0xFF0000)
    else:
        embed = discord.Embed(title=message.author.display_name,description=f"**{result}개 당첨됐습니다!**ㅤ`[+{format(money,',d')}]`ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`\n\n📥입력 : {input_num}\n📤복권 : {lotto}",color=0x00FF00)
    await message.channel.send(embed=embed)

# 블랙잭 게임
async def handle_blackjack(client, message, idA, moneyA):
    ID = str(message.author.id)
    try:
        betting = int(message.content.split(" ")[1])
    except (IndexError, ValueError):
        await message.channel.send("명령어 형식: .블랙잭 (베팅금액)")
        return
    dealer, part = [], []
    dealer_emoji, part_emoji = [],[]
    card = [1,2,3,4,5,6,7,8,9,10,'J','Q','K']
    card_emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','🇯','🇶' ,'🇰']
    if not ID in idA or moneyA[idA.index(ID)] - betting < 0:
        embed = discord.Embed(title=message.author.display_name, description="돈이 부족합니다!", color=0xFF0000)
        await message.channel.send(embed=embed)
        return
    for i in range(0,10):
        a = random.choice(card); b=random.choice(card)
        dealer.append(a)
        dealer_emoji.append(card_emoji[card.index(a)])
        part.append(b)
        part_emoji.append(card_emoji[card.index(b)])
    dealer_value = f"{dealer_emoji[0]} {dealer_emoji[1]}"
    part_value = f"{part_emoji[0]} {part_emoji[1]}"
    temp = card_emoji[card.index(dealer[1])]
    total = 0
    count = 1
    dealer_total = 0
    dealer_count = 1
    for i in range(0, count+1):
        if part[i] == 'J' or part[i] == 'Q' or part[i] == 'K':
            total += 10
        else :
            total += part[i]
        if dealer[i] == 'J' or dealer[i] == 'Q' or dealer[i] == 'K':
            dealer_total +=10
        else :
            dealer_total += dealer[i]
    embed=discord.Embed(title="ㅤ               블랙잭", description=f"베팅ㅤ:ㅤ**{format(betting, ',d')}원**\n입력ㅤ:ㅤ**.힛ㅤ/ㅤ.스탠드**\nㅤ", color=0xD8AA2D)
    embed.add_field(name=f"딜러[?]", value=f"❔ {temp}")
    embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
    embed.add_field(name=f"{message.author.display_name}[{total}]", value=part_value)
    await message.channel.send(embed=embed)
    def check(m):
        return m.author == message.author and m.channel == message.channel and m.content in [".힛", ".스탠드"]
    while True:
        msg = await client.wait_for('message', check=check)
        if msg.content == ".힛":
            count+=1
            part_value += f" {part_emoji[count]}"
            if part[count] == 'J' or part[count] == 'Q' or part[count] == 'K':
                total += 10
            else:
                total += part[count]
            if(total>21):
                embed=discord.Embed(title="ㅤ               블랙잭", description=f"베팅ㅤ:ㅤ**{format(betting, ',d')}원**\nㅤ", color=0xD8AA2D)
                embed.add_field(name=f"딜러[{dealer_total}]", value=dealer_value)
                embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
                embed.add_field(name=f"{message.author.display_name}[{total}]", value=part_value)
                await message.channel.send(embed=embed)
                moneyA[idA.index(ID)] -= betting
                embed=discord.Embed(title="【버스트】ㅤ딜러 승리", description=f"`[-{format(betting, ',d')}]`ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`", color=0xFF0000)
                await message.channel.send(embed=embed)
                return
            else:
                embed=discord.Embed(title="ㅤ               블랙잭", description=f"베팅ㅤ:ㅤ**{format(betting, ',d')}원**\n입력ㅤ:ㅤ**.힛ㅤ/ㅤ.스탠드**\nㅤ", color=0xD8AA2D)
                embed.add_field(name=f"딜러[?]", value=f"? {temp}")
                embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
                embed.add_field(name=f"{message.author.display_name}[{total}]", value=part_value)
                await message.channel.send(embed=embed)
        if msg.content == ".스탠드":
            embed=discord.Embed(title="ㅤ               블랙잭", description=f"베팅ㅤ:ㅤ**{format(betting, ',d')}원**\nㅤ", color=0xD8AA2D)
            embed.add_field(name=f"딜러[{dealer_total}]", value=dealer_value)
            embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
            embed.add_field(name=f"{message.author.display_name}[{total}]", value=part_value)
            await message.channel.send(embed=embed)
            await asyncio.sleep(1)
            while(dealer_total<17):
                dealer_count+=1
                dealer_value +=f" {dealer_emoji[dealer_count]}"
                if dealer[dealer_count] == 'J' or dealer[dealer_count] == 'Q' or dealer[dealer_count] == 'K':
                    dealer_total +=10
                else :
                    dealer_total += dealer[dealer_count]
                if (dealer_total >21):
                    embed=discord.Embed(title="ㅤ               블랙잭", description=f"베팅ㅤ:ㅤ**{format(betting, ',d')}원**\nㅤ", color=0xD8AA2D)
                    embed.add_field(name=f"딜러[{dealer_total}]", value=dealer_value)
                    embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
                    embed.add_field(name=f"{message.author.display_name}[{total}]", value=part_value)
                    await message.channel.send(embed=embed)
                    moneyA[idA.index(ID)] += betting
                    embed=discord.Embed(title=f"【버스트】ㅤ{message.author.display_name} 승리", description=f"`[+{format(betting, ',d')}]`ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`", color=0x00FF00)
                    await message.channel.send(embed=embed)
                    return
                else:
                    embed=discord.Embed(title="ㅤ               블랙잭", description=f"베팅ㅤ:ㅤ**{format(betting, ',d')}원**\nㅤ", color=0xD8AA2D)
                    embed.add_field(name=f"딜러[{dealer_total}]", value=dealer_value)
                    embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
                    embed.add_field(name=f"{message.author.display_name}[{total}]", value=part_value)
                    await message.channel.send(embed=embed)
                await asyncio.sleep(1)
            if(total >dealer_total) :
                moneyA[idA.index(ID)] += betting
                embed=discord.Embed(title=f"{message.author.display_name} 승리", description=f"`[+{format(betting, ',d')}]`ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`", color=0x00FF00)
                await message.channel.send(embed=embed)
                return
            elif(total <dealer_total) :
                moneyA[idA.index(ID)] -= betting
                embed=discord.Embed(title="딜러 승리", description=f"`[-{format(betting, ',d')}]`ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`", color=0xFF0000)
                await message.channel.send(embed=embed)
                return
            else :
                embed=discord.Embed(title="푸시", description=f"`[+0]`ㅤ`[자산 : {format(moneyA[idA.index(ID)], ',d')}원]`", color=0xd070fb)
                await message.channel.send(embed=embed)
                return

# 승부예측 게임
"""
async def handle_bet_prediction(message, idA, moneyA):
    team1 = message.content.split(" ")[1]
    team2 = message.content.split(" ")[2]
    betting = int(message.content.split(" ")[3])
    team1_list, team2_list = [], []
    people = []
    deadline = 0
    total_money = 0
    value1, value2 = "", ""
    embed = discord.Embed(title=f"승부 예측ㅤ[{team1} VS {team2}]", description=f"ㅤ\n참가비ㅤ:ㅤ`{format(betting, ',d')}원`\n입력ㅤ:ㅤ`.예측 {team1}` / `.예측 {team2}`\n마감ㅤ:ㅤ`.예측 마감`", color=0x00aaaa)
    await message.channel.send(embed=embed)
    while True:
        msg = await message.client.wait_for('message')
        if (str(msg.content).find('.예측')==0) and not msg.author.name in people and deadline == 0:
            if str(msg.content)[4:] == team1:
                if not str(msg.author.id) in idA or moneyA[idA.index(str(msg.author.id))] - betting < 0:
                    embed = discord.Embed(title=msg.author.name, description="돈이 부족합니다!", color=0xFF0000)
                    await message.channel.send(embed=embed)
                else:
                    moneyA[idA.index(str(msg.author.id))] -= betting
                    people.append(msg.author.name)
                    team1_list.append([msg.author.name, str(msg.author.id)])
                    embed = discord.Embed(title="", description=f"{msg.author.name}님이 {team1} 예측했습니다.", color=0x00FF00)
                    await message.channel.send(embed=embed)
            elif str(msg.content)[4:] == team2:
                if not str(msg.author.id) in idA or moneyA[idA.index(str(msg.author.id))] - betting < 0:
                    embed = discord.Embed(title=msg.author.name, description="돈이 부족합니다!", color=0xFF0000)
                    await message.channel.send(embed=embed)
                else:
                    moneyA[idA.index(str(msg.author.id))] -= betting
                    people.append(msg.author.name)
                    team2_list.append([msg.author.name, str(msg.author.id)])
                    embed = discord.Embed(title="", description=f"{msg.author.name}님이 {team2} 예측했습니다.", color=0x00FF00)
                    await message.channel.send(embed=embed)
        if (msg.content == ".예측 마감"):
            deadline = 1
            total_money = betting * len(people)
            if (len(people)<2 or len(team1_list)==0 or len(team2_list)==0):
                embed = discord.Embed(title=msg.author.name, description="인원수 부족으로 게임을 종료합니다", color=0xFF0000)
                await message.channel.send(embed=embed)
                for i in range(0,len(team1_list)):
                    moneyA[idA.index(team1_list[i][1])] += betting
                for i in range(0,len(team2_list)):
                    moneyA[idA.index(team2_list[i][1])] += betting
                return
            else:
                for i in range(0,len(team1_list)):
                    value1 += team1_list[i][0]+'\n'
                for i in range(0,len(team2_list)):
                    value2 += team2_list[i][0]+'\n'
                embed=discord.Embed(title="ㅤ         승부예측", description=f"`[상금 : {format(total_money, ',d')}원]`\nㅤ", color=0xD8AA2D)
                embed.add_field(name=f"{team1}", value=value1)
                embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
                embed.add_field(name=f"{team2}", value=value2)
                embed.set_footer(text=f"ㅤ\n끝 :ㅤ.승리 {team1}/.승리 {team2}")
                await message.channel.send(embed=embed)
        if (str(msg.content).find('.승리')==0 and msg.author == message.author and deadline == 1):
            if str(msg.content)[4:] == team1:
                individual_money = int(total_money / len(team1_list))
                for i in range(0,len(team1_list)):
                    moneyA[idA.index(team1_list[i][1])] += individual_money
                embed = discord.Embed(title=f"{team1} 승리!", description=f"`[개인 상금 : {format(individual_money, ',d')}원]`", color=0x00FF00)
                embed.add_field(name=f"ㅤ\n승리팀 명단", value=value1)
                await message.channel.send(embed=embed)
            elif str(msg.content)[4:] == team2:
                individual_money = int(total_money / len(team2_list))
                for i in range(0,len(team2_list)):
                    moneyA[idA.index(team2_list[i][1])] += individual_money
                embed = discord.Embed(title=f"{team2} 승리!", description=f"`[개인 상금 : {format(individual_money, ',d')}원]`", color=0x00FF00)
                embed.add_field(name=f"ㅤ\n승리팀 명단", value=value2)
                await message.channel.send(embed=embed)
                """

# 콜마이네임 게임
"""
async def handle_call_my_name(message):
    list_names = [ ... ]  # 기존 인물 리스트 복사
    person = []
    name, obj = [], []
    people = 0
    deadline = 0
    embed = discord.Embed(title = "콜 마이 네임 (양세찬 게임)",description=f"서로 질문을 주고 받으며, 먼저 자신의 인물을 맞추면 승리입니다!\nㅤ\n참가ㅤ:ㅤ`.참가`\n시작ㅤ:ㅤ`.시작`ㅤㅤㅤㅤ `(2명 이상)`\n정답ㅤ:ㅤ`.정답 (이름)`ㅤ`(ex 정답. 유재석)` \n관전ㅤ:ㅤ`.관전`ㅤㅤㅤㅤ `(참여자는 사용 불가)`", color=discord.Color.blue())
    await message.channel.send(embed=embed)
    while True:
        msg = await message.client.wait_for('message')
        if (msg.content == ".참가" and message.channel == msg.channel and not msg.author in name and deadline == 0):
            name.append(msg.author)
            obj.append(random.choice(list_names))
            people +=1
            embed = discord.Embed(description=f"**{msg.author.name}**님이 참가하셨습니다 `[참가자 : {people}명]`" , color=0xd070fb)
            await message.channel.send(embed=embed)
        if msg.content == ".시작" and message.channel == msg.channel and deadline == 0:
            deadline = 1
            if people <2 :
                embed = discord.Embed(title=msg.author.name, description="인원수 부족으로 게임을 종료합니다", color=0xFF0000)
                await message.channel.send(embed=embed)
                return
            embed = discord.Embed(title = "게임 시작",description=f"각자 dm을 확인하시고 **자신의 인물**을 맞추세요. ㅤ`.정답 (이름)`" , color=0xD8AA2D)
            embed.set_footer(text="dm 내용을 메모장에 써두고 보면서 하는 걸 추천드립니다.\n(+모든 인물은 붙여쓰기합니다.)")
            await message.channel.send(embed=embed)
            for i in range(0, len(name)):
                person.append([name[i], obj[i]])
            for i in range(0, len(name)):
                note = ""
                if name[i].dm_channel:
                    for j in range(0, len(name)):
                        if (i ==j):
                            note += f"**{person[j][0].name}**의 인물 : **???**\n"
                        else :
                            note += f"**{person[j][0].name}**의 인물 : **{person[j][1]}**\n"
                    embed = discord.Embed(title = "콜 마이 네임",description=note, color=discord.Color.blue())
                    await name[i].send(embed=embed)
                elif name[i].dm_channel is None:
                    channel = await name[i].create_dm()
                    for j in range(0, len(name)):
                        if (i ==j):
                            note += f"**{person[j][0].name}**의 인물 : **???**\n"
                        else :
                            note += f"**{person[j][0].name}**의 인물 : **{person[j][1]}**\n"
                    embed = discord.Embed(title = "콜 마이 네임",description=note, color=discord.Color.blue())
                    await channel.send(embed=embed)
        if msg.content == ".관전" and message.channel == msg.channel and not message.author in name and deadline == 1:
            note = ""
            if message.author.dm_channel:
                for j in range(0, len(name)):
                    note += f"**{person[j][0].name}**의 인물 : **{person[j][1]}**\n"
                embed = discord.Embed(title = "콜 마이 네임 - 관전",description=note, color=discord.Color.blue())
                await message.author.send(embed=embed)
            elif message.author.dm_channel is None:
                channel = await message.author.create_dm()
                for j in range(0, len(name)):
                    note += f"**{person[j][0].name}**의 인물 : **{person[j][1]}**\n"
                embed = discord.Embed(title = "콜 마이 네임 - 관전",description=note, color=discord.Color.blue())
                await channel.send(embed=embed)
        if str(msg.content).find('.정답')==0 and msg.author in name and deadline == 1:
            note = ""
            for i in range(0, len(name)):
                if str(msg.content)[4:] == person[i][1] and msg.author ==person[i][0]:
                    for j in range(0, len(name)):
                        note += f"**{person[j][0].name}**의 인물 : **{person[j][1]}**\n"
                    embed = discord.Embed(title=f"🎉{person[i][0].name}님 승리입니다!🎉",description=note, color=0x00FF00)
                    await message.channel.send(embed=embed)
                    return """

# 섯다 게임
"""
async def handle_sutda(message, idA, moneyA, timeA, levelA, timeB, timeC):
    name, name_id, hand1, hand2, score, id, hand1_emoji, hand2_emoji = [], [], [], [], [], [], [], []
    people = 0
    turn = 3; start = 0
    betting = 0; betting_raise = 0
    embed=discord.Embed(title="ㅤ             섯다", description=f"참가ㅤ:ㅤ**.참가**\n시작ㅤ:ㅤ**.시작 (2명)**ㅤ", color=discord.Color.blue())
    await message.channel.send(embed=embed)
    while True:
        msg = await message.client.wait_for('message')
        if (msg.content == ".참가" and not str(msg.author.id) in id):
            if str(msg.author.id) in idA:
                people+=1
                name.append(msg.author.name)
                name_id.append(msg.author)
                id.append(str(msg.author.id))
                embed=discord.Embed(title="ㅤ                    섯다", description=f"**__{msg.author.name}__** 님이 참가했습니다ㅤ`[참가자 {people}명]`", color=0x00FF00)
                await message.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="ㅤ                    섯다", description=f"등록되지 않은 아이디입니다", color=0x00FF00)
                await message.channel.send(embed=embed)
        if (msg.content == ".시작"):
            if(people != 2):
                embed=discord.Embed(title="ㅤ               섯다", description=f"인원수 2명을 맞춰주세요", color=0xFF0000)
                await message.channel.send(embed=embed)
                return
            embed=discord.Embed(title=f"ㅤ                     섯다〔1〕", description=f"<@{id[0]}> 입력ㅤ:ㅤ**.베팅 (돈)/.다이**\nㅤ", color=0xD8AA2D)
            embed.add_field(name=f"{name[0]}[?]", value=f"❔ ❔\n\n`[{format(moneyA[idA.index(id[0])], ',d')}]`")
            embed.add_field(name="ㅤ   VS   ㅤ", value="ㅤ")
            embed.add_field(name=f"{name[1]}[?]", value=f"❔ ❔\n\n`[{format(moneyA[idA.index(id[1])], ',d')}]`")
            await message.channel.send(embed=embed)
            num = [1,2,3,4,5,6,7,8,9]
            num_emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
            for i in range(0, 2):
                a = random.choice(num); b = random.choice(num)
                hand1.append(a)
                hand1_emoji.append(num_emoji[a-1])
                hand2.append(b)
                hand2_emoji.append(num_emoji[b-1])
                if hand1[i] == hand2[i]:
                    score.append(hand1[i] +hand2[i] + 20)
                else:
                    score.append(hand1[i] +hand2[i])
                if name_id[i].dm_channel:
                    embed=discord.Embed(title="ㅤ               섯다", description=f"**__{name[i]}__** 님의 패ㅤ:ㅤ**{hand1_emoji[i]} {hand2_emoji[i]}**ㅤㅤ`점수 : {score[i]}`", color=0xD8AA2D)
                    await name_id[i].dm_channel.send(embed=embed)
                elif name_id[i].dm_channel is None:
                    dm_channel = await name_id[i].create_dm()
                    embed=discord.Embed(title="ㅤ               섯다", description=f"**__{name[i]}__** 님의 패ㅤ:ㅤ**{hand1_emoji[i]} {hand2_emoji[i]}**ㅤㅤ`점수 : {score[i]}`", color=0xD8AA2D)
                    await dm_channel.send(embed=embed)
        # 이하 모든 베팅, 콜, 레이즈, 다이, 승패 처리 로직을 main.py에서 그대로 함수로 옮겨서 구현
        # (코드가 길어질 수 있으니 필요시 분할 작성)
        # ... (생략) ... 
"""