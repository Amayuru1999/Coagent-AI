# Coagent
[![CI](https://github.com/OpenCSGs/coagent/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenCSGs/coagent/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)

An open-source framework for building monolithic or distributed agentic systems, ranging from simple LLM calls to compositional workflows and autonomous agents.


<p align="center">
<img src="assets/coagent-overview.png" height="600">
</p>


## Features

- [x] Event-driven
- [x] Monolithic or Distributed
- [x] Single-agent
    - [x] Function-calling
    - [ ] ReAct
- [x] Multi-agent orchestration
    - [x] Agent Discovery
    - [x] Static orchestration
        - [x] Sequential
    - [x] Dynamic orchestration
        - [x] Dynamic Triage
        - [x] Handoffs (based on async Swarm)
        - [ ] Group Chat
- [x] Runtime
    - [x] Local Runtime (In-process Runtime)
    - [x] HTTP Runtime (HTTP-based Distributed Runtime)
    - [x] NATS Runtime (NATS-based Distributed Runtime)
        - [ ] Using NATS [JetStream][1]
- [x] [CoS](coagent/cos) (Multi-language support)
    - [x] [Python](examples/cos/cos.py)
    - [x] [Node.js](examples/cos/cos.js)
    - [x] [Go](examples/cos/goagent)
    - [ ] Rust


## Three-tier Architecture

<p align="center">
<img src="assets/coagent-three-tier-architecture.png" height="500">
</p>


## Installation

```bash
pip install git+https://github.com/OpenCSGs/coagent.git
```


## Quick Start

```python
# translator.py

import asyncio
import os

from coagent.agents import ChatAgent, ChatHistory, ChatMessage, ModelClient
from coagent.core import AgentSpec, new, set_stderr_logger
from coagent.runtimes import LocalRuntime

client = ModelClient(
    model=os.getenv("MODEL_NAME"),
    api_base=os.getenv("MODEL_API_BASE"),
    api_version=os.getenv("MODEL_API_VERSION"),
    api_key=os.getenv("MODEL_API_KEY"),
)

translator = AgentSpec(
    "translator",
    new(
        ChatAgent,
        system="You are a professional translator that can translate Chinese to English.",
        client=client,
    ),
)


async def main():
    async with LocalRuntime() as runtime:
        await runtime.register_spec(translator)

        result = translator.run_stream(
            ChatHistory(
                messages=[ChatMessage(role="user", content="你好，世界")]
            ).encode()
        )
        async for chunk in result:
            msg = ChatMessage.decode(chunk)
            print(msg.content, end="", flush=True)


if __name__ == "__main__":
    set_stderr_logger()
    asyncio.run(main())
```

Run the agent:

```bash
export MODEL_NAME=<YOUR_MODEL_NAME>
export MODEL_API_BASE=<YOUR_MODEL_API_BASE>
export MODEL_API_VERSION=<YOUR_MODEL_API_VERSION>
export MODEL_API_KEY=<YOUR_MODEL_API_KEY>
python translator.py
```


## Patterns

TODO


## Examples

- [ping-pong](examples/ping-pong)
- [stream-ping-pong](examples/stream-ping-pong)
- [discovery](examples/discovery)
- [translator](examples/translator)
- [opencsg](examples/opencsg)
- [app-builder](examples/app-builder)
- [autogen](examples/autogen)
- [cos](examples/cos)


[1]: https://docs.nats.io/nats-concepts/jetstream
