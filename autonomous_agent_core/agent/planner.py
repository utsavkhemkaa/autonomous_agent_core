from dataclasses import dataclass
from typing import Optional, Dict, List, Any
from utils.logger import get_logger


@dataclass
class Plan:
    stop: bool
    confidence: float
    steps: Optional[List[Dict[str, Any]]] = None
    reason: Optional[str] = None

    def is_valid(self) -> bool:
        # confidence must always exist and be valid
        if not isinstance(self.confidence, float):
            return False
        if not (0.0 <= self.confidence <= 1.0):
            return False

        if self.stop:
            return True

        if isinstance(self.steps, list) and len(self.steps) > 0:
            for step in self.steps:
                if (
                    not isinstance(step, dict)
                    or "tool_name" not in step
                    or "args" not in step
                    or not isinstance(step["args"], dict)
                ):
                    return False
            return True

        return False


class Planner:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.logger = get_logger(self.__class__.__name__)

    def plan(self, task: str, state: Dict[str, Any]) -> Plan:
        prompt = self._build_prompt(task, state)

        try:
            response = self.llm.generate(prompt)
        except Exception as e:
            self.logger.error(f"Failed to generate response from LLM: {e}")
            return Plan(
                stop=False,
                confidence=0.0,
                reason="planner_llm_failure"
            )

        return self._parse_response(response)

    def _build_prompt(self, task: str, state: Dict[str, Any]) -> str:
        return f"""
You are an AI planner.

Task:
{task}

Current state:
{state}

Rules:
- If you believe no further useful actions remain, respond with:
  {{
    "stop": true,
    "confidence": <float between 0 and 1>
  }}

- Otherwise, respond with:
  {{
    "stop": false,
    "confidence": <float between 0 and 1>,
    "steps": [
      {{ "tool_name": "<tool>", "args": {{ ... }} }}
    ]
  }}

Confidence represents how strongly you believe the task is complete.
Do not explain.
Do not add extra text.
"""

    def _parse_response(self, response: str) -> Plan:
        response = response.strip()

        try:
            data = self._safe_json_parse(response)
            return Plan(
                stop=data.get("stop"),
                confidence=data.get("confidence"),
                steps=data.get("steps"),
                reason="planner_output"
            )
        except Exception as e:
            self.logger.error(f"Failed to parse response from LLM: {e}")
            return Plan(
                stop=False,
                confidence=0.0,
                reason="plan_parse_error"
            )

    def _safe_json_parse(self, text: str) -> Dict[str, Any]:
        import json
        return json.loads(text)



