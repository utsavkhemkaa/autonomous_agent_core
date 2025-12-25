# tools/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ToolResult:
    """
    Standardized result returned by every tool.
    Must align with AgentLoop and AgentState.
    """
    success: bool
    output: Optional[Any] = None
    error_type: Optional[str] = None     # "transient" | "permanent"
    error_message: Optional[str] = None


class BaseTool(ABC):
    """
    Abstract base class for all tools.
    """

    name: str
    description: str

    def __init__(self):
        if not getattr(self, "name", None):
            raise ValueError("Tool must define a name.")
        if not getattr(self, "description", None):
            raise ValueError("Tool must define a description.")

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        """
        Execute the tool logic.
        Must be implemented by subclasses.
        """
        pass

    def __call__(self, **kwargs) -> ToolResult:
        """
        Execute the tool safely and always return ToolResult.
        """
        try:
            result = self.run(**kwargs)

            # Safety: tools MUST return ToolResult
            if not isinstance(result, ToolResult):
                return ToolResult(
                    success=False,
                    error_type="permanent",
                    error_message="Tool returned invalid result type"
                )

            return result

        except Exception as e:
            # Unexpected crash → transient failure
            return ToolResult(
                success=False,
                error_type="transient",
                error_message=str(e)
            )


