from abc import ABC, abstractmethod
from agent_service.agent.llm import LLMBedrock, LLMRunPod
from agent_service.prompts.prompt_builder import PromptBuilder


class Tool(ABC):
    """
    Base class for tools using LLMs and prompt templates.

    Attributes
    ----------
    name : str
        The name of the tool.
    description : str
        A brief description of the tool.
    llm : str
        The type of LLM to use ('bedrock' or 'runpod').
    prompt_id : str
        The ID of the prompt template.
    prompt_template : str
        The template for creating prompts.
    max_tokens : int
        The maximum number of tokens for the output.
    """

    def __init__(
        self,
        name: str,
        description: str,
        llm: str,
        prompt_id: str,
        prompt_template: str,
        max_tokens: int,
    ) -> None:
        self.name = name
        self.description = description
        self.max_tokens = max_tokens
        self.set_llm(llm)
        self.prompt_id = prompt_id
        self.prompt_template = prompt_template
        self.prompt = ""
        self.init_prompt()

    @abstractmethod
    def run(self, input: str):
        """
        Abstract method to run the tool with given input.

        Parameters
        ----------
        input : str
            The input string for the tool to process.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass.
        """
        pass

    def __str__(self) -> str:
        res = "Tool: " + self.name
        res += " : " + self.description + "\n"
        return res

    def set_llm(self, llm):
        """
        Sets the LLM based on the provided type.

        Parameters
        ----------
        llm : str
            The type of LLM to use ('bedrock' or 'runpod').
        """
        if llm == "bedrock":
            self.llm = LLMBedrock()
            self.llm.set_max_tokens(self.max_tokens)
        elif llm == "runpod":
            self.llm = LLMRunPod()
            self.llm.set_max_tokens(self.max_tokens)
        else:
            self.llm = None

    def init_prompt(self):
        """
        Initializes the prompt using the prompt builder if an LLM is set.
        """
        if self.llm is not None:
            self.prompt = PromptBuilder()
            self.prompt.create_prompts({self.prompt_id: self.prompt_template})
        else:
            self.prompt = None
