# agent/executor.py

from typing import Dict
from tools.base import BaseTool, ToolResult


class Executor:
    """
    Executor executes validated tool calls deterministically.

    Responsibilities:
    - Lookup tool
    - Call tool.run()
    - Normalize all failures into ToolResult
    """

    def __init__(self, tools: Dict[str, BaseTool]):
        self.tools = tools

    def has_tool(self, tool_name: str) -> bool:
        return tool_name in self.tools

    def execute(self, tool_name: str, args: dict) -> ToolResult:
        tool = self.tools.get(tool_name)

        if not tool:
            return ToolResult(
                success=False,
                error_type="permanent",
                error_message=f"Tool '{tool_name}' not found",
            )

        try:
            result = tool.run(**args)

            # Safety check: tools MUST return ToolResult
            if not isinstance(result, ToolResult):
                return ToolResult(
                    success=False,
                    error_type="permanent",
                    error_message="Tool returned invalid result type",
                )

            return result

        except Exception as e:
            # Unexpected crash → transient failure
            return ToolResult(
                success=False,
                error_type="transient",
                error_message=str(e),
            )