# agent/state.py

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class AgentState:
    """
    AgentState is a dumb memory container.
    It stores what happened, NOT what should happen.
    """

    # ---- execution tracking ----
    step_count: int = 0
    completed: bool = False
    aborted: bool = False
    abort_reason: Optional[str] = None

    # ---- history ----
    tool_history: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    # ---- public helpers ----
    def record_tool_result(self, step: Dict[str, Any], result: Any) -> None:
        """
        Record the outcome of a tool execution.
        """
        self.tool_history.append({
            "tool_name": step.get("tool_name"),
            "args": step.get("args"),
            "success": result.success,
            "output": result.output,
            "error_type": result.error_type,
            "error_message": result.error_message,
        })

    def record_error(self, error: str) -> None:
        """
        Record planner / system level errors.
        """
        self.errors.append(error)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state into a planner-safe dictionary.
        """
        return {
            "step_count": self.step_count,
            "completed": self.completed,
            "aborted": self.aborted,
            "abort_reason": self.abort_reason,
            "tool_history": self.tool_history,
            "errors": self.errors,
        }




