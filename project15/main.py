"""
main.py — Мультиагентные дебаты (autogen-agentchat 0.4+, Python 3.12+)

Запуск:
    python main.py
    python main.py --topic "Стоит ли компании перейти на ИИ-контент?"
    python main.py --rounds 5 --no-moderator
"""
import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path


from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console

from agents import optimist, skeptic, analyst, moderator

DEFAULT_TOPIC = "Заменит ли ИИ программистов в ближайшие 10 лет?"

ROLE_EMOJI = {
    "Модератор": "🎙️",
    "Оптимист":  "🚀",
    "Скептик":   "🔍",
    "Аналитик":  "📊",
}


# ─────────────────────────────────────────────────────────────
# Сохранение лога
# ─────────────────────────────────────────────────────────────
def save_log(messages: list, topic: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Дебаты: «{topic}»",
        f"",
        f"**Дата:** {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        f"",
        f"---",
        f"",
    ]
    for i, msg in enumerate(messages, 1):
        name    = getattr(msg, "source", "Система")
        content = getattr(msg, "content", "").strip()
        if not content:
            continue
        emoji = ROLE_EMOJI.get(name, "💬")
        lines += [f"## {emoji} {name} (реплика {i})", "", content, "", "---", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n💾 Лог сохранён: {path}")


# ─────────────────────────────────────────────────────────────
# Статистика
# ─────────────────────────────────────────────────────────────
def show_stats(messages: list) -> None:
    counts: dict[str, int] = {}
    lengths: dict[str, list] = {}
    for msg in messages:
        name    = getattr(msg, "source", "")
        content = getattr(msg, "content", "")
        if not name or not content:
            continue
        counts[name] = counts.get(name, 0) + 1
        lengths.setdefault(name, []).append(len(content.split()))

    print("\n📊 СТАТИСТИКА ДЕБАТОВ")
    print("─" * 42)
    for name, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        avg = sum(lengths[name]) // len(lengths[name])
        print(f"  {name:<12}  реплик: {cnt}  │  средняя длина: {avg} слов")
    print("─" * 42)


# ─────────────────────────────────────────────────────────────
# Основная логика
# ─────────────────────────────────────────────────────────────
async def run_debate(topic: str, max_rounds: int, use_moderator: bool) -> None:
    print(f"\n{'═'*55}")
    print(f"  МУЛЬТИАГЕНТНЫЕ ДЕБАТЫ")
    print(f"  Тема: {topic}")
    print(f"  Раундов: {max_rounds} | Модератор: {'да' if use_moderator else 'нет'}")
    print(f"{'═'*55}\n")

    # Создаём агентов
    participants = []
    if use_moderator:
        participants.append(moderator.create_moderator())
    participants += [optimist.create_optimist(), skeptic.create_skeptic(), analyst.create_analyst()]

    # Условие завершения: достигнут лимит сообщений ИЛИ модератор написал "ФИНАЛ"
    termination = (
        MaxMessageTermination(max_messages=max_rounds)
        | TextMentionTermination("ФИНАЛ")
    )

    # Команда — RoundRobin: агенты говорят по очереди
    team = RoundRobinGroupChat(
        participants=participants,
        termination_condition=termination,
    )

    # Стартовое сообщение
    opening = (
        f"Начинаем дебаты на тему: «{topic}»\n\n"
        f"Участники:\n"
        f"- Оптимист (Алексей Новиков) — технооптимист\n"
        f"- Скептик (Марина Соколова) — исследователь рисков ИИ\n"
        f"- Аналитик (Дмитрий Волков) — финансовый аналитик\n\n"
        f"Каждый участник должен выступить минимум три раза. "
        + ("Модератор, пожалуйста, открой дискуссию." if use_moderator else "")
    )

    # Запускаем — Console выводит сообщения в реальном времени
    result = await Console(team.run_stream(task=opening))

    # Сохраняем лог
    messages = result.messages
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_log(messages, topic, Path(f"output/debate_log_{ts}.md"))
    save_log(messages, topic, Path("output/debate_log.md"))

    show_stats(messages)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Мультиагентные дебаты с AutoGen")
    parser.add_argument("--topic",        type=str, default=DEFAULT_TOPIC)
    parser.add_argument("--rounds",       type=int, default=16)
    parser.add_argument("--no-moderator", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run_debate(
            topic=args.topic,
            max_rounds=args.rounds,
            use_moderator=not args.no_moderator,
        ))
    except KeyboardInterrupt:
        print("\n⚠️  Дебаты прерваны.")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}", file=sys.stderr)
        raise