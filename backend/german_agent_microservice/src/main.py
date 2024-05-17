from agent_service.agent.llm import LLMBedrock
if __name__ == "__main__":
    llm = LLMBedrock()
    llm.run("Wie benutzte ich 'weil'?")