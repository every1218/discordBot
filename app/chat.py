from openai import AsyncOpenAI  # OpenAI 비동기 클라이언트 임포트
from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / 'configs' / '.env'
load_dotenv(dotenv_path=dotenv_path, verbose=True)

# 환경 변수 로드 및 검증
api_key = os.environ.get("OPENROUTER_API_KEY")
base_url = os.environ.get("OPENROUTER_BASE_URL")

# 비동기 클라이언트 초기화
client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

async def llm_chat(query: str) -> str:
    """
    OpenRouter LLM에게 질문을 보내고 답변을 받아옵니다.
    """
    if not query:
        return "왜 불렀어?"

    try:
        # 비동기 호출 (await 필수)
        response = await client.chat.completions.create(
            model="google/gemma-3-4b-it:free",  # 모델 이름은 여기서 지정
            messages=[
                {"role": "user", "content": f"너는 사용자에게 반말로 친근하게 대답하는 '펭귄봇'이야. 답변은 3~5문장 이내로 짧고 명확하게 대답해야 해.\n\n{query}"}
            ],
            temperature=0,  # 창의성 설정
            extra_headers={
                "HTTP-Referer": "https://discord.com",
                "X-Title": "Penguin Bot",
            }
        )

        # 답변 추출
        answer = response.choices[0].message.content

        # 디스코드 글자 수 제한(2000자) 처리
        if len(answer) > 2000:
            answer = answer[:1990] + "... (너무 길어서 잘렸어)"

        return answer

    except Exception as e:
        print(f"LLM API 오류 발생: {e}")
        return "오류 발생. 다시 시도해줘."