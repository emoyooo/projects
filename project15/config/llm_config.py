
import os
from dotenv import load_dotenv

load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise EnvironmentError("OPENAI_API_KEY не найден. Проверьте файл .env")

BASE_LLM_CONFIG = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": _api_key,
        }
    ],
    "temperature": 0.7,
    "cache_seed": None, 
}


MODERATOR_LLM_CONFIG = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": _api_key,
        }
    ],
    "temperature": 0.2,
    "cache_seed": None,
}
