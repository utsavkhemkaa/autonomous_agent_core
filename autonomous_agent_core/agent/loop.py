from typing import Optional

from utils.logger import get_logger
from agent.planner import Planner
from agent.executor import Executor
from agent.state import AgentState
from agent.executor import ToolResult


class AgentLoop:
    """
    The AgentLoop is the system authority.

    Responsibilities:
    - Call planner
    - Validate plans
    - Execute tools (one at a time)
    - Handle retries vs replans
    - Enforce safety limits
    - Mutate state
    """

    def __init__(
        self,
        planner: Planner,
        executor: Executor,
        max_steps: int = 20,
        max_retries: int = 2,
    ):
        self.planner = planner
        self.executor = executor
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.logger = get_logger(self.__class__.__name__)

    def run(self, task: str, state: AgentState) -> AgentState:
        """
        Run the agent loop until completion, refusal, or safety stop.
        """

        current_step: Optional[dict] = None
        retries: int = 0

        while state.step_count < self.max_steps:
            self.logger.info(f"Step {state.step_count}")

            # ---------- PLANNING PHASE ----------
            if current_step is None:
                plan = self.planner.plan(task, state.to_dict())

                if not plan.is_valid():
                    self.logger.warning("Invalid plan generated")
                    state.record_error("invalid_plan")
                    state.step_count += 1
                    continue  # replan

                if plan.stop:
                    self.logger.info("Planner indicated completion")
                    state.completed = True
                    return state

                if plan.refusal_reason:
                    self.logger.warning(f"Planner refusal: {plan.refusal_reason}")
                    state.aborted = True
                    state.abort_reason = plan.refusal_reason
                    return state

                # Take exactly ONE step
                current_step = plan.steps[0]
                retries = 0

            # ---------- EXECUTION PHASE ----------
            self.logger.info(
                f"Executing tool: {current_step['tool_name']} (retry {retries})"
            )

            result: ToolResult = self.executor.execute(
                tool_name=current_step["tool_name"],
                args=current_step["args"],
            )

            # ---------- SUCCESS ----------
            if result.success:
                state.record_tool_result(current_step, result)
                state.step_count += 1
                current_step = None
                retries = 0
                continue

            # ---------- TRANSIENT FAILURE (RETRY) ----------
            if result.error_type == "transient" and retries < self.max_retries:
                retries += 1
                self.logger.warning(
                    f"Transient error, retrying ({retries}/{self.max_retries})"
                )
                continue  # retry SAME step

            # ---------- PERMANENT FAILURE / RETRIES EXHAUSTED ----------
            self.logger.error("Non-transient failure or retries exhausted")
            state.record_tool_result(current_step, result)
            state.step_count += 1
            current_step = None
            retries = 0
            continue  # replan

        # ---------- SAFETY STOP ----------
        self.logger.error("Max steps exceeded")
        state.aborted = True
        state.abort_reason = "max_steps_exceeded"
        return state




