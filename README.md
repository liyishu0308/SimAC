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
4. Enter folder "./LLMs", and run specific scripts for different LLMs.
### gpt-3.5-turbo
```
cd LLMs
python turbo.py
```
### text-davinci-003
```
cd LLMs
python davinci.py
```
### OpenLLaMA-7B
```
cd LLMs
python openLLaMA_7B.py
```
### OpenLLaMA-13B
```
cd LLMs
python openLLaMA_13B.py
```
