"""Raw-HTTP drop-in replacement for tau_bench's LLM user simulator.

tau_bench.envs.user.LLMUserSimulationEnv (site-packages) talks to the user
model through litellm's `completion()`. RawHttpxUserSim instead POSTs
directly to a vLLM-served OpenAI-compatible `/chat/completions` endpoint
via an `httpx2.Client`, so the harness can attach its own event hooks
(e.g. for capturing traces) to that client. It copies
LLMUserSimulationEnv's exact system prompt, its reset()/step()/
get_total_cost() interface, and the "###STOP###" stop convention, so it
can be swapped in for `env.user` (tau_bench.envs.base.Env.__init__,
`self.user = load_user(...)`) without changing Env.reset()/Env.step().
"""

from typing import Any, Dict, List, Optional

import httpx2
from tau_bench.envs.user import BaseUserSimulationEnv

DEFAULT_BASE_URL = "http://localhost:18001/v1"
DEFAULT_MODEL = "qwen32b"


class RawHttpxUserSim(BaseUserSimulationEnv):
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        client: Optional[Any] = None,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.model = model
        self.client = client if client is not None else httpx2.Client()
        self.messages: List[Dict[str, Any]] = []
        self.total_cost = 0.0

    def build_system_prompt(self, instruction: Optional[str]) -> str:
        instruction_display = (
            ("\n\nInstruction: " + instruction + "\n")
            if instruction is not None
            else ""
        )
        return f"""You are a user interacting with an agent.{instruction_display}
Rules:
- Just generate one line at a time to simulate the user's message.
- Do not give away all the instruction at once. Only provide the information that is necessary for the current step.
- Do not hallucinate information that is not provided in the instruction. For example, if the agent asks for the order id but it is not mentioned in the instruction, do not make up an order id, just say you do not remember or have it.
- If the instruction goal is satisified, generate '###STOP###' as a standalone message without anything else to end the conversation.
- Do not repeat the exact instruction in the conversation. Instead, use your own words to convey the same information.
- Try to make the conversation as natural as possible, and stick to the personalities in the instruction."""

    def generate_next_message(self, messages: List[Dict[str, Any]]) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "max_tokens": 512,
            "chat_template_kwargs": {"enable_thinking": False},
        }
        response = self.client.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers={"X-Agent": "user_sim"},
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": content})
        return content

    def reset(self, instruction: Optional[str] = None) -> str:
        self.messages = [
            {
                "role": "system",
                "content": self.build_system_prompt(instruction=instruction),
            },
            {"role": "user", "content": "Hi! How can I help you today?"},
        ]
        return self.generate_next_message(self.messages)

    def step(self, content: str) -> str:
        self.messages.append({"role": "user", "content": content})
        return self.generate_next_message(self.messages)

    def get_total_cost(self) -> float:
        return 0.0


def install_user_sim(
    env: Any,
    client: Optional[Any] = None,
    base_url: str = DEFAULT_BASE_URL,
    model: str = DEFAULT_MODEL,
) -> RawHttpxUserSim:
    """Replace env.user with a RawHttpxUserSim (see tau_bench.envs.base.Env,
    which stores the user sim as `self.user` and drives it via
    `self.user.reset(instruction=...)` / `self.user.step(content)` /
    `self.user.get_total_cost()`)."""
    user_sim = RawHttpxUserSim(base_url=base_url, model=model, client=client)
    env.user = user_sim
    return user_sim
