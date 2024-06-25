from agent_service.prompts.tool_prompt import READING_TEMPLATE
from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder

class ReadingGenerator(Tool):
    """
    a tool for the reading text generation
    """
    ROOT_DIR = 'agent_service/tools/res/profiles/'
    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)
        self.load_profiles()
        self.current_profile = 'Mo'

    def run(self, input:str):
        """
        runs LLM with input. 
        """
        name, story = self.get_story()
        self.query = self.prompt.generate_prompt(
            name_id=self.prompt_id, topic=input, 
            person_name=name, person_story=story
            )
        answer = self.llm.run(self.query)
        answer = '.'.join(answer.split('.')[:-1]) + '.'
        return answer
    
    def load_profiles(self):
        with open(self.ROOT_DIR + 'mo.md', 'r') as f:
            mo_story = f.readlines()
        with open(self.ROOT_DIR + 'layla.md', 'r') as f:
            layla_story = f.readlines()
        self.profiles = {'Mo': mo_story, 'Layla' : layla_story}

    def get_story(self):
        story = self.profiles[self.current_profile]
        name = self.current_profile
        if  self.current_profile == 'Layla':
            self.current_profile = 'Mo'
        else:
            self.current_profile = 'Layla'
        return name, story