import string

class PromptBuidler:
    def __init__(self, prompt : str):
        self.template = string.Template(prompt)

    def update(self, *args, **kws):
        return self.template.safe_substitute(*args, **kws)
    

        
