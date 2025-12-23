import datetime
import random
import discord

#단순 명령어 처리
async def handle_simple_commands(message, today):
    if message.content == ".준엽 전역":
        LJY_discharge = datetime.datetime(2023, 11, 30)
        await message.channel.send(f"준엽 전역 **{(LJY_discharge-today).days}일** 남았습니다", reference=message, mention_author=False)
        return True
    if message.content == ".정혁 전역":
        LJH_join_army = datetime.datetime(2024, 3, 25)
        await message.channel.send(f"정혁 전역 **{(LJH_join_army-today).days}일** 남았습니다", reference=message, mention_author=False)
        return True
    if message.content == ".도현 입대":
        KDH_join_army = datetime.datetime(2022, 12, 26)
        await message.channel.send(f"도현 입대 **{(KDH_join_army-today).days}일** 남았습니다", reference=message, mention_author=False)
        return True
    if message.content == ".상훈 입대":
        PSH_join_army = datetime.datetime(2023, 1, 9)
        await message.channel.send(f"상훈 입대 **{(PSH_join_army-today).days}일** 남았습니다", reference=message, mention_author=False)
        return True
    if message.content == ".수능":
        CSAT = datetime.datetime(2022, 11, 17)
        await message.channel.send(f"수능 **{(CSAT-today).days}일** 남았습니다", reference=message, mention_author=False)
        return True
    if message.content == ".4수":
        CSAT2 = datetime.datetime(2023, 11, 16)
        await message.channel.send(f"4수 **{(CSAT2-today).days}일** 남았습니다", reference=message, mention_author=False)
        return True
    if message.content == ".점메추":
        food = ["짜장면","짬뽕","김치찌개","순두부찌개","부대찌개","생선구이","볶음밥","초밥","덮밥","도시락","돈까스","우동","냉면","햄버거","스파게티","떡볶이","피자","치킨","카레","칼국수","떡볶이","밥버거","토스트","샌드위치","라면","보쌈","족발","비빔밥","닭갈비","수제비","된장찌개","갈비탕","삼계탕","깐풍기","파스타","김밥","메밀소바","삼겹살","곱창","닭볶음탕","국밥","제육볶음","낙지볶음","찜닭","김밥","잔치국수","비빔국수","집밥"]
        await message.channel.send(f"**{food[random.randrange(0,len(food))]}** 어떠세요?", reference=message, mention_author=False)
        return True
    if message.content == ".라인":
        line = ("탑", "정글", "미드", "원딜", "서폿")
        pick = random.choice(line)
        color_dict = {
            "탑": 0x3498db,      # 파랑
            "정글": 0x27ae60,    # 초록
            "미드": 0x9b59b6,    # 보라
            "원딜": 0xe67e22,    # 주황
            "서폿": 0xf1c40f     # 노랑
        }
        emoji_dict = {
            "탑": "🗻",
            "정글": "🌲",
            "미드": "🏙️",
            "원딜": "🏹",
            "서폿": "🛡️"
        }
        embed = discord.Embed(
            title=f"{emoji_dict[pick]} 오늘의 추천 라인!",
            description=f"**{pick}** 라인은 어떠세요?",
            color=color_dict[pick]
        )
        embed.set_footer(text="펭귄봇 라인추천", icon_url=message.author.avatar.url if hasattr(message.author, 'avatar') else None)
        await message.channel.send(embed=embed, reference=message, mention_author=False)
        return True
        
    return False 