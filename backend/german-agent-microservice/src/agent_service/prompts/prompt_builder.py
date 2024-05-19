import string

class PromptBuidler:
    def __init__(self, prompt : str):
        self.template = string.Template(prompt)
        self.prompt = prompt

    def update(self, *args, **kws):
        # Update the prompt with the new substitution
        new_prompt = string.Template(self.prompt).safe_substitute(**kws)
        self.prompt = new_prompt  # Update the internal prompt to reflect the new state
        return new_prompt
    
    def get_prompt(self):
        return str(self.prompt)
    
    def set_prompt(self, prompt:str):
        self.prompt = prompt

        
