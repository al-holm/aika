from agent_service.tools.tool import Tool
import requests
import os
from time import sleep 

class WebSearch(Tool):
    def __init__(self):
        self.name = "Web-Suche"
        self.description = "Hilfreich, wenn man Informationen im Internet nachschauen möchte."
        self.api_key = os.environ["RAPIDAPI_KEY"]
        self.api_host = "searxng.p.rapidapi.com"
        self.url = "https://searxng.p.rapidapi.com/search"

    def run(self, input: str):
        """
        The function uses the requests library to search SearxNG for results based on the input string.
        """
        answer = "Request time out"
        
        querystring, headers = self.setup_request(input)
        requests_n = 0
        while requests_n < 10:
            try:
                response = requests.post(self.url, headers=headers, params=querystring)
                results = response.json()
                answer = self.parse_results(results)
                requests_n = 100
            except Exception:
                sleep(2)
            requests_n += 1           
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
        The function sets up the request parameters and headers for the SearxNG API.
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


    