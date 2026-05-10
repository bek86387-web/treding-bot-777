import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """Sen professional trading va moliya bozori bo'yicha mutaxassis AI assistantsan.
Siz foydalanuvchilarga quyidagi mavzularda yordam berasiz:
- Forex, Kripto (BTC, ETH), Oltin (XAU) bozorlari
- Kuchli support va resistance zonalari
- Supply va demand zonalari
- Buy va Sell signallari
- Texnik tahlil
- Moliyaviy yangiliklar

Javoblaringiz aniq, qisqa va professional bo'lsin. O'zbekcha yoki rus tilida javob bering, foydalanuvchi qaysi tilda yozsa shu tilda."""


def get_ai_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI xatosi: {str(e)}"