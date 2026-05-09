"""
agents/moderator.py
Агент-модератор.
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MODERATOR_LLM_CONFIG

MODERATOR_PROMPT = """Ты — модератор дебатов. Твоя роль — управлять дискуссией, а не участвовать в ней.

ТВОИ ЗАДАЧИ:

1. ОТКРЫТИЕ (первое сообщение):
   Представь тему, участников и правила. Дай слово первому оратору.

2. В ХОДЕ ДЕБАТОВ:
   - Коротко резюмируй ключевой аргумент предыдущей реплики (1 предложение)
   - Если дискуссия уходит от темы — верни её
   - Следи за балансом: если кто-то молчит — дай ему слово

3. ФИНАЛЬНОЕ ЗАКЛЮЧЕНИЕ (когда дебаты завершены, напиши ФИНАЛ):
   ## Итоги дебатов
   **Позиция Оптимиста:** ...
   **Позиция Скептика:** ...
   **Позиция Аналитика:** ...
   **Общий вывод:** ...
   **Наиболее убедительные аргументы:** топ-3

СТИЛЬ: нейтральный, короткие реплики (2–3 предложения) кроме финала."""


def create_moderator() -> AssistantAgent:
    client = OpenAIChatCompletionClient(
        model=MODERATOR_LLM_CONFIG["model"],
        api_key=MODERATOR_LLM_CONFIG["api_key"],
        temperature=0.2,
    )
    return AssistantAgent(
        name="Модератор",
        system_message=MODERATOR_PROMPT,
        model_client=client,
    )