# main.py

import os

from llm.client import LLMClient
from agent.planner import Planner
from agent.executor import Executor
from agent.loop import AgentLoop
from agent.state import AgentState
from config.settings import MAX_STEPS, MAX_RETRIES

# import tools
from tools.calculator import CalculatorTool
from tools.file_writer import FileWriterTool
from tools.web_search import WebSearchTool


def main():
    # ---- LLM ----
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    llm = LLMClient(api_key=api_key)
    planner = Planner(llm)

    # ---- TOOLS REGISTRATION ----
    tools = {
        "calculator": CalculatorTool(),
        "file_writer": FileWriterTool(),
        "web_search": WebSearchTool(),
    }

    executor = Executor(tools=tools)

    # ---- AGENT LOOP ----
    agent = AgentLoop(
    planner=planner,
    executor=executor,
    max_steps=MAX_STEPS,
    max_retries=MAX_RETRIES,
)

    # ---- STATE ----
    state = AgentState()

    # ---- RUN ----
    task = input("Enter task: ")
    final_state = agent.run(task, state)

    # ---- OUTPUT ----
    print("\n=== AGENT FINISHED ===")
    print("Completed:", final_state.completed)
    print("Aborted:", final_state.aborted)
    print("Abort reason:", final_state.abort_reason)
    print("Steps executed:", final_state.step_count)
    print("Tool history:")
    for entry in final_state.tool_history:
        print(entry)


if __name__ == "__main__":
    main()