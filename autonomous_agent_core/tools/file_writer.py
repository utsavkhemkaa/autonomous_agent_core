import os
from tools.base import BaseTool, ToolResult
from config.settings import DATA_DIR

class FileWriterTool(BaseTool):
    name = "file_writer"
    description = "Writes content to a file inside the data directory"

    BASE_DIR = DATA_DIR

    def run(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        content = kwargs.get("content")

        if not path or content is None:
            return ToolResult(
                success=False,
                error_type="permanent",
                error_message="Both 'path' and 'content' are required"
            )

        try:
            full_path = os.path.join(self.BASE_DIR, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            return ToolResult(
                success=True,
                output={"path": full_path}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error_type="transient",
                error_message=str(e)
            )