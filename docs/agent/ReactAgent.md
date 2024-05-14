# German Chat ReAct Agent

ReAct Agent is a thought-action-observation loop that enables a LLM to use external tools such as web-searching, retireving information from data bases, browsing, and to reason over a context provided from those tools ("observations") in order to solve diverse decision-making and language tasks.

## Introduction

Solving complex interactive tasks requires the ability to reason in multiple steps preserving the intermediate conclusions. 

Complex reasoning, reasoning in interactive enviroments. 

Few shot prompting -> Chain-Of-Thoughts

CoT vs React

## ReAct Agent : Definition

The classical reinforcement learning setting implies that given an action space $\mathcal{A}$, an observation space $\mathcal{O}$ and a time step $t$, the agent recieves an einviroment observation $o_t \in \mathcal{O}$ and use a policy $π(a_t|c_t)$ to generate an action $a_t \in \mathcal{A}$, where the $c_t$ - the context - is a sequence of actions and observations. 

In the ReAct setting the action space is extended with unlimited language space $\mathcal{L}$. The elements of $\mathcal{L}$ are refered to as thoughts, or reasoning traces. A thought $\hat{a_t}$ is a reasoning step over a context $c_t$. (Yao et al., 2023)[[1]](#1)

## German Chat ReAct Agent 


## References
<a id="1">[1]</a> 
S. Yao et al., “ReAct: Synergizing Reasoning and Acting in Language Models.” arXiv, Mar. 09, 2023. Accessed: May 14, 2024. [Online]. Available: http://arxiv.org/abs/2210.03629
