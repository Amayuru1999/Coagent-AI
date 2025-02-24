# translator.py

# import asyncio
# import os
#
# from coagent.agents import ChatAgent, ModelClient
# from coagent.core import AgentSpec, idle_loop, new, set_stderr_logger
# from coagent.runtimes import NATSRuntime
#
# translator = AgentSpec(
#     "translator",
#     new(
#         ChatAgent,
#         system="You are a professional translator that can translate Chinese to English.",
#         client=ModelClient(model="openai/gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
#     ),
# )
#
#
# async def main():
#     async with NATSRuntime.from_servers("nats://localhost:4222") as runtime:
#         await runtime.register(translator)
#         await idle_loop()
#
#
# if __name__ == "__main__":
#     set_stderr_logger()
#     asyncio.run(main())

# Distributed Approach
# translator.py

import asyncio
import os

from coagent.agents import ChatAgent, ModelClient
from coagent.core import AgentSpec, idle_loop, new, set_stderr_logger
from coagent.runtimes import NATSRuntime

translator = AgentSpec(
    "translator",
    new(
        ChatAgent,
        system="You are a professional translator that can translate Chinese to English.",
        client=ModelClient(model="openai/gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    ),
)


async def main():
    async with NATSRuntime.from_servers("nats://localhost:4222") as runtime:
        await runtime.register(translator)
        await idle_loop()


if __name__ == "__main__":
    set_stderr_logger()
    asyncio.run(main())