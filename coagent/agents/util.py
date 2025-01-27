import asyncio
import functools
from typing import AsyncIterator

from coagent.core import logger

from .messages import ChatMessage
from .model_client import default_model_client, ModelClient


async def chat(
    messages: list[ChatMessage], client: ModelClient = default_model_client
) -> ChatMessage:
    response = await client.acompletion(
        messages=[m.model_dump() for m in messages],
    )
    msg = response.choices[0].message
    return ChatMessage(
        role=msg.role,
        content=msg.content,
    )


async def chat_stream(
    messages: list[ChatMessage], client: ModelClient = default_model_client
) -> AsyncIterator[ChatMessage]:
    response = await client.acompletion(
        messages=[m.model_dump() for m in messages],
        stream=True,
    )
    async for chunk in response:
        msg = chunk.choices[0].delta
        if msg.content:
            yield ChatMessage(role="assistant", content=msg.content)


def run_in_thread(func):
    @functools.wraps(func)
    async def run(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return run


async def is_user_confirmed(
    content: str, client: ModelClient = default_model_client
) -> bool:
    """Check whether the user has confirmed or not based on the content."""
    # Quick path
    if content.lower() in ("yes", "ok", "1"):
        return True
    elif content.lower() in ("no", "do not", "0"):
        return False

    logger.debug(f"Using {client.model} to analyze the user's sentiment")

    reply = await chat(
        [
            ChatMessage(
                role="user",
                content=f"""\
Based on the input, determine whether it's positive or not. Return "true" if it's
positive or "false" if not. You should only return "true" or "false.

Input: {content}
Output:\
""",
            )
        ],
        client,
    )
    answer = reply.content
    return answer.strip().lower() == "true"
