from agent_service.agent.agent_step import AgentValidationStep 
import logging
class ValidationParser:
    def __init__(self) -> None:
        self.logger = logging.getLogger("FinalAnswer")
         
    def parse_step(self, input:str) -> AgentValidationStep:
        validation_thought = input.split("\n")[0]
        self.logger.info(validation_thought)
        return AgentValidationStep(validation_thought=validation_thought)
    
