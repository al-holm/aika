from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms.bedrock import Bedrock
import os
import logging
import json
import warnings
from pathlib import Path
import openai
from tool_master import ToolMaster
import re, uuid
warnings.filterwarnings("ignore")

logging.getLogger("langchain_community").setLevel(logging.CRITICAL)
logging.getLogger("langchain_core").setLevel(logging.CRITICAL)
logging.getLogger("unstructured").setLevel(logging.CRITICAL)
logging.getLogger("deepl").setLevel(logging.CRITICAL)
logging.getLogger("llama_parse").setLevel(logging.CRITICAL)
openai.api_key = os.getenv('OPENAI_API_KEY')


# The `LLMAgent` class is a Python class that represents a REACT agent responsible for interacting with a
# language model to generate responses to student queries, validate those responses using GPT-3.5, and
# provide suggestions for improvement.
class LLMAgent:
    MODEL_PATH = Path('backend/german-agent-microservice/res/models')
    OUTPUT_PATH = Path('backend/german-agent-microservice/res/output/')
    def __init__(self, model='', bedrock=None):
        logging.info('...initialising agent...')
        self.model_path = None if model=='' else os.path.join(self.MODEL_PATH, model) 
        self.bedrock = bedrock
        self.tool_master = ToolMaster(bedrock=bedrock)
        self.tools =  self.tool_master.tools
        # Get the prompt to use - you can modify this!
        #self.prompt = hub.pull("hwchase17/react")
        self.build_prompt()
        self.configure_llm()
        # Construct the ReAct agent
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        # Create an agent executor by passing in the agent and tools
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True, return_intermediate_steps=True,
                                            handle_parsing_errors="Check you output and make sure it conforms! Do not output an action and a final answer at the same time.")
        self.audio_created = False
        logging.info('...agent built...')


    def configure_llm(self):
        '''The function `configure_llm` sets the `llm` attribute of an object to an instance of the
        `Ollama` class with a specific model parameter.
        
        '''
        if self.bedrock==None:
            self.llm = Ollama(model="mixtral:8x7b")
        else:
            self.llm = Bedrock(model_id="mistral.mixtral-8x7b-instruct-v0:1", 
                    client=self.bedrock, model_kwargs={"max_tokens": 512})
            

    def run(self,  query: str):
        """
        This function takes a query as input, invokes an agent executor, validates the response.
        @param {str} query - The `query` parameter in the `run` method is a string that represents the
        input query.
        """
        response = self.agent_executor.invoke({'input' : query,})
        success, new_query = self.validate_answer(query, response['output'], response["intermediate_steps"])
        # self.tool_master.audio_created = False
        # self.tool_master.reading_task_gen.reading = False


    def validate_answer(self, query, assistant_response, intermediate_steps):
        """
        The `validate_answer` function uses OpenAI's GPT-3.5 model to evaluate the response and provide suggestions for
        improvement if needed.
        @param query - refers to the question asked by the student 
        @param assistant_response - response of agent
        @param intermediate_steps - chain of actions or steps taken by the agent
        @returns - success - boolean value - if the question was answered, new_query - if success is False, suggestion for a next query
        """
        newline = '\n'
        intermediate_steps = self.parse_react_intermediate_steps(intermediate_steps)
        prompt = f"""
Task: You are to evaluate the performance of our German assistant who has answered a student's question. You have to decide whether the answer should be generated again.

Question from the student: {query}

Answer from our assistant: {assistant_response}

An audio was generated: {self.tool_master.audio_created}
If this is a listening task, a text must be created and an audio must be generated. If, it is 'False' above, the response must be regenerated.

Intermediate steps (chain): {intermediate_steps}

The following tools are available to the system:
{ newline.join(
    f'{tool.name} : {tool.description}' for tool in self.tools
)
}
The following format is used for chains:

Question: the initial question you need to answer
Thought: you should always think about what to do
Action: the action to be taken, should be one of Tools
Action Input: the input for the action
Observation: how do you assess the result of the action?
...
... (this Thought,Action,Action Input,Observation can be repeated N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Format your answer as follows:
Success: True or False – Does the answer correspond to the question or task? If "False", the Assistant should regenerate the answer.
New query: If Success false, rephrase the task or question so that the assistant can answer better.
Answer Suggestion: Suggest your own answer for the  student question in German.
Improved Chain: Suggest improvements for the Chain and intermediate steps. Use keywords Question,Thought,Action,Action Input,Observation,...,Thought,Final Answer and the tools list above. The generated content should be in German (with English chain keywords).
"""
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=300,
             )
            print(response.choices[0])
            response = response.choices[0].text
            success, new_query, val_output, improved_chain = self.parse_validation_response(response)
            data_dict = {
                'user_query' : query,
                'agent_response' : assistant_response,
                'intermediate_steps' : intermediate_steps,
                'success' : success,
                'next_query_suggestion' : new_query,
                'answer_suggestion' : val_output,
                'improved_chain' : improved_chain
            }
            self.save_to_json(data_dict)
            return success, new_query
        except Exception as e:
            logging.ERROR(f"An error occurred: {e}")

    def parse_validation_response(self, output_string):
        """
        The function `parse_validation_response` extracts specific parts of a validation response.
        @param output_string 
        @returns The `parse_validation_response` function returns a tuple containing the following
        values:
        1. `success`: A boolean value indicating whether the validation was successful (True) or not
        (False).
        2. `new_query`: A string representing the new query extracted from the output string.
        3. `your_output`: A string representing the answer suggestion extracted from the output string.
        4. `improved_chain`: A string with suggestions how to improve the action chain.
        """
        # Use regular expressions to find the parts of the string
        success_match = re.search(r'Success: (True|False)', output_string)
        new_query_match = re.search(r'New query: (.*)', output_string)
        your_output_match = re.search(r'Answer Suggestion: (.*)', output_string)
        improved_chain_match = re.search(r'Improved Chain: (.*)', output_string)
        
        # Extracting the matched groups if found, otherwise set a default value
        success = success_match.group(1) if bool(success_match) else False
        new_query = new_query_match.group(1) if new_query_match else ""
        your_output = your_output_match.group(1) if your_output_match else ""
        improved_chain = improved_chain_match.group(1) if improved_chain_match else ""
        
        return success, new_query, your_output, improved_chain
    
    def parse_react_intermediate_steps(self, intermediate_steps):
        """
        The function `parse_react_intermediate_steps` takes a list of intermediate steps, returns a parsed string containing the extracted
        details categorized by 'Thought', 'Action', 'Action Input', and 'Observation'.
        @param intermediate_steps - list with steps of List[Set(AgentTool(), str)]
        @returns  a parsed string that includes the Thought, Action, Action Input, and Observation for each element in the `intermediate_steps`
        """
        parsed_string = ''
        for el in intermediate_steps:
            parsed_string += 'Thought: ' + str(el[0].log.split('Action')[0]) + '\n' # include only Thought
            parsed_string += 'Action: ' + str(el[0].tool) + '\n'
            parsed_string += 'Action Input: ' + str(el[0].tool_input)+ '\n'
            parsed_string += 'Observation: ' + str(el[1]) + '\n\n'
        return parsed_string


    def save_to_json(self, data_dict):
        """
        saves a dictionary as a JSON file with a unique ID in a specified output path.
        @param data_dict -  a dictionary containing the data that you want to save to a JSON file
        """
        id = str(uuid.uuid4()) + '.json'
        path = os.path.join(self.OUTPUT_PATH, id)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=4, ensure_ascii=False)
        logging.info('Written result of validation as JSON')

    def build_prompt(self):
        template = """
        [INST] 
Du bist ein Deutschlehrer. Beantworte die Fragen deines Studenten. Benutze einfache Sprache. 
Beantworte die folgenden Fragen so gut wie du kannst. Du hast Zugang zu den folgenden Tools:
{tools}

Verwende das folgende Format:

Question: die Eingangsfrage, die Du beantworten musst
Thought: Du solltest immer darüber nachdenken, was zu tun ist
Action: die zu ergreifende Maßnahme, sollte eine von [{tool_names}] sein
Action Input: die Eingabe für die Aktion
Observation: wie schätzt du das Ergebnis der Handlung ein?
...
... (dieser Thought/Action/Action Input/Observation kann N-mal wiederholt werden)
Thought: Ich kenne jetzt die endgültige Antwort
Final Answer: die endgültige Antwort auf die ursprüngliche Eingangsfrage

Beginne! Bei Erstellung von Hörtexten, benutze das 'Audio Generation' Tool. Bei Erstellung von Lesetexte, muss du KEIN Audio generieren. 
Such minimal in Lehrbücher & benutzte immer Prefixe wie Thought/Action/Action Input/Observation/Final Answer.
Wenn du die endgültige Antwort gefunden hast, gib "Final Answer: [deine Antwort]." zurück. 
[/INST]
Question: {input}

Thought:{agent_scratchpad} """

        self.prompt = PromptTemplate.from_template(template)