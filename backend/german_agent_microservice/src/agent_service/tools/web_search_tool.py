import serpapi
import os
from tool import Tool

class WebSearch(Tool):
    def __init__(self, k:int=5):
        self.name = "Web-Suche"
        self.description = "Hilfreich, wenn man Informationen im Internet nachschauen möchte"
        self.k = k

    def run(self, input:str):
        out = serpapi.search(q=input, engine="google", location="Marburg, Germany", hl="de", gl="de")
        return self.parse_results(out)

    
    def parse_results(self, results : dict):
        snippets = []
        for result in results["organic_results"][:self.k]:
            if "snippet" in result:
                snippets.append(result["snippet"])
            for attribute, value in result.get("attributes", {}).items():
                snippets.append(f"{attribute}: {value}.")

        if len(snippets) == 0:
            return "No good Google Search Result was found"
        return " ".join(snippets)