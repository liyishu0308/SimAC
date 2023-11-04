# SimAC
Repository for the paper "SimAC: Simulating Agile Collaboration to Generate Acceptance Criteria in User Story Elaboration".
## Framework of SimAC
The typical workflow of SimAC consists of four phases: I. collaboration; II. deduplication.
![alt text](https://github.com/liyishu0308/SimAC/blob/main/img/workflow.jpg?raw=true)
## Implementation
In this work, we implemented SimAC on four LLMs.
1. The prompts are specified under "./Instructions".
2. The examples are specified under "./Examples".
3. The input user stories are placed under "./UserStories".
4. Update the target user story in "./LLM/xx.py".
5. Enter folder "./LLMs", and run specific scripts for different LLMs.
### gpt-3.5-turbo
```
cd LLMs
## role-based prompt
python turbo_ro.py
## regular-prompt
python turbo_re.py
```
### text-davinci-003
```
cd LLMs
## role-based prompt
python davinci_ro.py
## regular-prompt
python davinci_re.py
```
### OpenLLaMA-7B / OpenLLaMA-13B
```
cd LLMs
## role-based prompt
python openLLaMA_ro.py ## update the preloaded model as OpenLLaMA-7B or OpenLaMA-13B
## regular-prompt
python openLLaMA_re.py ## update the preloaded model as OpenLLaMA-7B or OpenLaMA-13B
```
