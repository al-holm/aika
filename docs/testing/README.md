# Testing

## Goals for Test Coverage
### Code Coverage:
Our goal is to ensure that our tests cover all the possible branches and paths in the code. By focusing on branch coverage, we can identify and address any potential issues in the decision-making logic of the application. This type of coverage ensures that our tests are not just executing lines of code but are also evaluating the various conditions and outcomes that may arise during execution.

### Specification Coverage:
We aim to verify that all the specified requirements and use cases for the application are tested. By creating UI tests to cover the functional requirements, we ensure that the application is tested against its intended use cases. 

## Types of Tests Used
### Unit Tests:
- Focus on testing individual components or functions in isolation.
- Validate that each part of the code works correctly on its own.
### Integration Tests:
- Test the interactions between different components or systems.
- Ensure that the integrated parts of the application work together as expected.
### UI Tests:
- Based on our use cases, verify that the user interface behaves as expected.

## Test reports
### Agent Microservice
| Name                                                 | Stmts | Miss | Branch | BrPart | Cover |
|------------------------------------------------------|-------|------|--------|--------|-------|
| agent_service/agent/agent.py                         | 123   | 34   | 22     | 7      | 66%   |
| agent_service/agent/agent_step.py                    | 25    | 0    | 2      | 0      | 100%  |
| agent_service/agent/llm.py                           | 58    | 24   | 0      | 0      | 59%   |
| agent_service/agent/reasoning_trace.py               | 63    | 5    | 22     | 3      | 86%   |
| agent_service/agent/task_type.py                     | 5     | 0    | 0      | 0      | 100%  |
| agent_service/core/config.py                         | 31    | 10   | 6      | 1      | 65%   |
| agent_service/core/pydantic_agent.py                 | 6     | 0    | 0      | 0      | 100%  |
| agent_service/core/pydantic_llm.py                   | 13    | 0    | 0      | 0      | 100%  |
| agent_service/core/pydantic_tool.py                  | 7     | 0    | 0      | 0      | 100%  |
| agent_service/core/pydantic_tool_exe.py              | 11    | 0    | 0      | 0      | 100%  |
| agent_service/exeptions/step_exception.py            | 12    | 1    | 0      | 0      | 92%   |
| agent_service/parsers/agent_step_parser.py           | 69    | 1    | 20     | 0      | 99%   |
| agent_service/parsers/exercises_parser.py            | 36    | 0    | 10     | 1      | 98%   |
| agent_service/prompts/prompt_builder.py              | 40    | 0    | 2      | 0      | 100%  |
| agent_service/prompts/react_prompt.py                | 7     | 0    | 0      | 0      | 100%  |
| agent_service/prompts/task_generation_examples.py    | 4     | 0    | 0      | 0      | 100%  |
| agent_service/prompts/tool_prompt.py                 | 7     | 0    | 0      | 0      | 100%  |
| agent_service/prompts/trajectory_library.py          | 79    | 59   | 22     | 0      | 20%   |
| agent_service/rag/rag.py                             | 121   | 25   | 44     | 3      | 79%   |
| agent_service/tools/listening_generation_tool.py     | 15    | 8    | 2      | 0      | 41%   |
| agent_service/tools/no_answer_tool.py                | 6     | 1    | 0      | 0      | 83%   |
| agent_service/tools/phrasing_tool.py                 | 10    | 3    | 0      | 0      | 70%   |
| agent_service/tools/reading_generation_tool.py       | 10    | 4    | 0      | 0      | 60%   |
| agent_service/tools/task_generation_tool.py          | 99    | 87   | 18     | 0      | 10%   |
| agent_service/tools/tool.py                          | 33    | 3    | 6      | 1      | 90%   |
| agent_service/tools/tool_executor.py                 | 43    | 13   | 6      | 0      | 65%   |
| agent_service/tools/tool_factory.py                  | 39    | 3    | 4      | 0      | 93%   |
| agent_service/tools/translator_tool.py               | 29    | 0    | 6      | 0      | 100%  |
| agent_service/tools/web_search_tool.py               | 44    | 0    | 8      | 0      | 100%  |
| **TOTAL**                                            | **1045** | **281** | **200** | **16** | **71%** |

### Curriculum Microservice

File                   | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
-----------------------|---------|----------|---------|---------|-------------------
All files              |   93.47 |    83.33 |     100 |   92.77 |                   
 lesson                |    93.5 |    81.81 |     100 |   92.85 |                   
  lesson.controller.ts |     100 |      100 |     100 |     100 |                   
  lesson.service.ts    |   92.06 |    81.81 |     100 |   91.37 | 27,45-46,65-66    
 util                  |   93.33 |      100 |     100 |    92.3 |                   
  json.util.ts         |   93.33 |      100 |     100 |    92.3 | 16                

### API Gateway

File                | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s           
--------------------|---------|----------|---------|---------|-----------------------------
All files           |   82.14 |      100 |   83.33 |   81.25 |                             
 chat.controller.ts |   92.59 |      100 |   83.33 |      92 | 42-43                       
 chat.service.ts    |   77.19 |      100 |   83.33 |   76.36 | 66-67,91-92,115-116,139-154 

### User Microservice
