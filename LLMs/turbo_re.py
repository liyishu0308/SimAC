'''
no role instruction
weighted output examples, three sets (example 7, 8, 9)
'''

import os
import openai
import configs as cf
from json import dumps
import time
from rateLimit import completions_with_backoff
from saveResults import *
from promptExamples import *
from promptInstructions import *
from promptRoles import *
from dataProccessing import *
from resultHandling import *

openai.organization = cf.OPENAI_ORG


def askGPT(prompt):
    # print(prompt)
    openai.api_key = cf.OPENAI_KEY
    completion = openai.ChatCompletion.create(
    # completion = completions_with_backoff(
      model="gpt-3.5-turbo",
      messages = prompt
    )
    ans = completion.choices[0].message.content+'\n'
    print("="*30, "completion", "="*30)
    print(completion)

    return ans, completion


def bufferedChat(us, promptInput):
    history = []
    outputs = []
    output = ''
    stage = "C"  # R for role instruction, C for create acceptance criteria, U for update acceptance criteria
    allCompletions = []

    initialPrompt = promptInput[0]
    input = promptInput[1]

    ## Pop user and assistant prompt for each iteration, with system role in first iteration
    newInput = input.pop(0)
    currentInput = initialPrompt + [newInput]  # system, user, assistant

    currentOutput, completion = askGPT(currentInput)
    currentOutput = removeBlankLines(currentOutput)

    output = output + currentOutput + '\n'
    outputs.append(currentOutput)
    history.append((currentInput, currentOutput))
    allCompletions.append(completion)


    return output, outputs, history, allCompletions



def runByProject(numbers, scriptNo, cases):
    for projectNo in numbers:

        fn = "UserStories/g" + projectNo + ".txt"
        file = open(fn, "r")  #
        stories = file.readlines()
        for usNo in cases:
            us = "User Story: \n" + stories[usNo]

            print("-" * 70)
            print(us)

            myPrompt = constructeInput(us)

            ac, all_output, all_history, all_completions = bufferedChat(us, myPrompt)
            print("=" * 20 + "AC for Group " + projectNo + "=" * 20)
            print(ac)

            usNo = str(usNo)
            writeACbyProject(us, ac, projectNo, scriptNo, usNo)
            writeAllResultsbyProject(all_history, projectNo, scriptNo, usNo)
            saveCompletionsbyProject(all_completions, projectNo, scriptNo, usNo)
            processFinalACbyProjectNoRatio(us, projectNo, scriptNo, usNo)


def constructeInput(us):
    usFile, pbExample, qaExample, pmExample = readExamplesAC("7")
    usFile2, pbExample2, qaExample2, pmExample2 = readExamplesAC("8")
    usFile3, pbExample3, qaExample3, pmExample3 = readExamplesAC("9")

    initSysContent = readInstruction("Instructions/initialSystem_7.txt")
    outputFormat = readInstruction("Instructions/outputFormat.txt")

    contextAndRole = [{"role": "system",
                       "content": initSysContent + "\n" + outputFormat + "\n"}]

    command = "Write acceptance criteria for the given user story:\n"

    learning = [{"role": "user",
                 "content": command + usFile + "\n"},
                {"role": "assistant",
                 "content": pmExample + "\n"},
                {"role": "user",
                 "content": command + usFile2 + "\n"},
                {"role": "assistant",
                 "content": pmExample2 + "\n"},
                {"role": "user",
                 "content": command + usFile3 + "\n"},
                {"role": "assistant",
                 "content": pmExample3 + "\n"}]

    prompts = contextAndRole + learning

    completionComands = [{"role": "user",
                          "content": command + "\n" + us + "\n"}
                         ]

    myInput = [prompts, completionComands]

    return myInput


# projectNumbers = ["02","03","04","05","08","10","11","12","13","14","16","17","18","19","21","22","23","24","25","26","27","28"]
# projectNumbers = ["23","24","25","26","27","28"]
projectNumbers = ["28"]
# evaluateCases = [30, 63, 53, 37, 26, 57, 65, 2, 40, 58] ## g11
# evaluateCases = [50, 27, 7, 25, 11, 26, 16, 21, 8, 1] ## g24
evaluateCases = [6, 49, 5, 20, 25, 50, 17, 3, 15,	21] ## g28
scriptNo = "22"
# usNumber = 0
# runByProject(projectNumbers, usNumber, scriptNo)
runByProject(projectNumbers, scriptNo, evaluateCases)


