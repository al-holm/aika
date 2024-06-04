import string

class PromptBuilder:
    def __init__(self) -> None:
        self._prompts = {}

    def create_prompts(self, prompt_dict:dict):
        """
        initializes prompts based on a dictionary input.
        
        Parameters
        ----------
        prompt_dict : dict
            a dictionary that contains prompts where the keys are the names
        of the prompts and the values are the actual prompt content.
        
        """
        self._prompts = {}
        for name, prompt in prompt_dict.items():
            prompt = Prompt(name, prompt)
            self._prompts[name] = prompt

    def generate_prompt(self, name_id, *args, **kwargs) -> str:
        """ 
        gets the prmopt by name id & substitutes the keywords from the kwargs
        with values from the kwargs

        Returns
        -------
        new_prompt : str 
            substitued prompt
        """
        prompt = self._prompts[name_id].prompt
        new_prompt = string.Template(prompt).safe_substitute(**kwargs)
        return new_prompt
    
    def update_prompt(self, name_id, *args, **kwargs) -> str:
        """ 
        gets the prmopt by name id, substitutes the keywords from the kwargs
        with values from the kwargs, updates the prompt in the Prompt object
        """ 
        new_prompt = self.generate_prompt(name_id=name_id, **kwargs)
        self._prompts[name_id].prompt = new_prompt 
        return new_prompt
    
    def get_prompt(self, name):
        """  
        returns the prompt by name id
        """ 
        prompt = self._prompts[name].prompt
        return prompt
    
    def set_prompt(self, name, prompt:str):
        """  
        sets the new prompt by name id
        """ 
        self._prompts[name].prompt = prompt

        
class Prompt:
    """
    represents a prompt with a name and a message
    """
    def __init__(self, name: str, prompt : str):
        self._name = name
        self._prompt = prompt

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        self._prompt = value

    def __str__(self) -> str:
        return self._prompt
