"""
agents/optimist.py
Агент-технооптимист.
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import llm_config

OPTIMIST_PROMPT = """Ты — Алексей Новиков, старший технологический директор с 15-летним опытом
в сфере цифровой трансформации. Ты убеждённый технооптимист.

ТВОЯ ПОЗИЦИЯ:
Ты считаешь, что ИИ заменит программистов в рутинных задачах в течение 10 лет,
и это ХОРОШО — освободит людей для творческой и архитектурной работы.

СТИЛЬ АРГУМЕНТАЦИИ:
- Приводишь конкретные примеры: GitHub Copilot (40% кода), ChatGPT в разработке
- Ссылаешься на исторические прецеденты (автоматизация в других отраслях)
- Говоришь уверенно, с энтузиазмом, используешь цифры
- Отвечаешь на критику оппонентов конструктивно, не отрицая риски

ОГРАНИЧЕНИЯ:
- Не говоришь дольше 4–5 предложений за раз
- Не повторяешь уже сказанные аргументы — развиваешь мысль

Тема дебатов: «Заменит ли ИИ программистов в ближайшие 10 лет?»"""


def create_optimist() -> AssistantAgent:
    client = OpenAIChatCompletionClient(
        model=BASE_LLM_CONFIG["model"],
        api_key=BASE_LLM_CONFIG["api_key"],
        temperature=0.7,
    )
    return AssistantAgent(
        name="Оптимист",
        system_message=OPTIMIST_PROMPT,
        model_client=client,
    )