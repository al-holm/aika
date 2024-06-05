from agent_service.tools.tool import Tool
from agent_service.prompts.tool_prompt import WEB_SUMMARY_TEMPLATE
from agent_service.agent.llm import LLMBedrock, LLMRunPod
from agent_service.prompts.prompt_builder import PromptBuilder
import requests
import os
from time import sleep 

class WebSearch(Tool):
    PROMPT_ID = "web summary"
    TEMPLATE = WEB_SUMMARY_TEMPLATE
    def __init__(self, llm):
        self.name = "Web-Suche"
        self.description = "Hilfreich, wenn man Informationen im Internet nachschauen möchte."
        self.api_key = os.environ["RAPIDAPI_KEY"]
        self.api_host = "searxng.p.rapidapi.com"
        self.url = "https://searxng.p.rapidapi.com/search"
        self.set_llm(llm)
        self.llm.set_max_tokens(350)
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
            )

    def run(self, input_str: str):
        """
        uses the requests library to search SearxNG for results based on the input string.
        """
        def_answer = "Wiederhole die Anfrage noch mal"
        answer = def_answer
        querystring, headers = self.setup_request(input_str)
        requests_n = 0
        while requests_n < 20:
            try:
                response = requests.post(self.url, headers=headers, params=querystring)
                results = response.json()
                answer = self.parse_results(results)
                requests_n = 100
            except Exception:
                sleep(1)
            requests_n += 1  
        if answer != def_answer:
            self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, 
                                                     text=input_str,
                                                     search_results=answer)
            answer = self.llm.run(self.query) 
        return answer
    
    def parse_results(self, results):
        if len(results["answers"]) > 0 :
            return results["answers"][0]
        out = ""
        results = results["results"]
        for i in results:
            out += i["title"] 
            out += i["content"] + "\n"
        return out 

    def setup_request(self, input: str):
        """
        sets up the request parameters and headers for the SearxNG API.
        """
        querystring = {"q": input , 
                       "categories": "general",
                       "engines": "google,bing",
                       "language": "de",
                       "pageno": "1",
                       "format": "json",
                       "results_on_new_tab":"0",
                       "image_proxy":"false",
                       "safesearch":"1"
                       }

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        return querystring, headers
    
    # source: https://rapidapi.com/iamrony777/api/searxng 1000 requests a day


    