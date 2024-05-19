from agent_service.agent.agent_step import AgentFinalStep
import logging
class AnswerParser:
    def __init__(self) -> None:
        self.logger = logging.getLogger("FinalAnswer")
    def parse_step(self, input:str) -> AgentFinalStep:
        fin_answer = input.split("Final Answer:")[-1]
        self.logger.info(fin_answer)
        return AgentFinalStep(final_answer=fin_answer)