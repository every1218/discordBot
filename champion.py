import json
import discord

def load_champion_data():
    """JSONL 파일에서 챔피언 데이터를 로드합니다."""
    try:
        with open('champ.jsonl', 'r', encoding='utf-8') as f:
            # 각 줄을 읽어 JSON 객체로 변환하고 리스트에 추가
            return [json.loads(line) for line in f]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"오류: 'champ.jsonl' 파일을 읽을 수 없습니다. ({e})")
        return []

def find_champion(champion_data, query):
    """챔피언 데이터에서 쿼리와 일치하는 챔피언을 찾습니다."""
    query = query.lower()
    for champ in champion_data:
        # 챔피언 이름 또는 별명이 쿼리와 일치하는지 확인
        if query == champ['champion'].lower() or query in [alias.lower() for alias in champ.get('aliases', [])]:
            return champ
    return None

def create_champion_embed(champion_info):
    """챔피언 정보를 바탕으로 Discord 임베드를 생성합니다."""
    embed = discord.Embed(
        title=f"{champion_info['champion']} 카운터 정보",
        color=discord.Color.blue()
    )

    # 하드 카운터 정보 추가
    hard_counters = champion_info.get('hard_counters', [])
    if hard_counters:
        for counter in hard_counters:
            reason = counter.get('reason', '이유 없음')
            if len(reason) > 1024:
                reason = reason[:1021] + '...'
            embed.add_field(name=f"💀 {counter['name']}", value=reason, inline=False)
    else:
        embed.add_field(name="💀 하드 카운터", value="정보 없음", inline=False)

    # 일반 카운터 정보 추가
    general_counters = champion_info.get('general_counters', [])
    if general_counters:
        value = ", ".join(general_counters)
        embed.add_field(name="🔥 일반 카운터", value=value, inline=False)
    else:
        embed.add_field(name="🔥 일반 카운터", value="정보 없음", inline=False)
    return embed

async def handle_champion_command(message):
    """'.챔피언' 명령어를 처리합니다."""
    if not message.content.startswith('.카운터 '):
        return

    query = message.content[5:].strip()
    if not query:
        await message.channel.send("카운터 이름을 입력해주세요. (예: .카운터 가렌)", reference=message)
        return

    champion_data = load_champion_data()
    if not champion_data:
        await message.channel.send("카운터 데이터를 불러오는 데 실패했습니다.", reference=message)
        return
        
    found_champion = find_champion(champion_data, query)

    if found_champion:
        embed = create_champion_embed(found_champion)
        await message.channel.send(embed=embed, reference=message)
    else:
        await message.channel.send(f"'{query}' 카운터 정보를 찾을 수 없습니다.", reference=message)
