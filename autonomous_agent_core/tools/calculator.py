import ast
from tools.base import BaseTool, ToolResult


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluates basic arithmetic expressions safely"

    def run(self, **kwargs) -> ToolResult:
        expression = kwargs.get("expression")

        if not expression:
            return ToolResult(
                success=False,
                error_type="permanent",
                error_message="No expression provided"
            )

        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            return ToolResult(
                success=False,
                error_type="permanent",
                error_message="Invalid expression syntax"
            )

        for node in ast.walk(tree):
            if not isinstance(
                node,
                (
                    ast.Expression,
                    ast.BinOp,
                    ast.UnaryOp,
                    ast.Num,
                    ast.Constant,
                    ast.Add,
                    ast.Sub,
                    ast.Mult,
                    ast.Div,
                    ast.USub,
                ),
            ):
                return ToolResult(
                    success=False,
                    error_type="permanent",
                    error_message="Unsupported operation in expression"
                )

        try:
            result = eval(compile(tree, filename="", mode="eval"))
        except Exception as e:
            return ToolResult(
                success=False,
                error_type="transient",
                error_message=str(e)
            )

        return ToolResult(
            success=True,
            output=result
        )