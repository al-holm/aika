import serpapi
import os
from agent_service.tools.tool import Tool

class WebSearch(Tool):
    def __init__(self, k:int=5):
        self.name = "Web-Suche"
        self.description = "Hilfreich, wenn man Informationen im Internet nachschauen möchte"
        self.k = k

    def run(self, input:str):
        """
        The function uses the SerpApi library to search Google for results based on the input string.
        """
        out = serpapi.search(q=input, engine="google", location="Marburg, Germany", hl="de", gl="de")
        return self.parse_results(out)

    
    def parse_results(self, results : dict):
        """
        The function `parse_results` extracts and formats snippets and attributes from a dictionary of
        search results, returning a concatenated string of the extracted information or a message if no
        relevant results are found.
        """
        snippets = []
        for result in results["organic_results"][:self.k]:
            if "snippet" in result:
                snippets.append(result["snippet"])
            for attribute, value in result.get("attributes", {}).items():
                snippets.append(f"{attribute}: {value}.")

        if len(snippets) == 0:
            return "No good Google Search Result was found"
        return " ".join(snippets)