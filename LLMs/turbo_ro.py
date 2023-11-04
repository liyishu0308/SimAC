'''
turbo with role-based prompt
'''

import os
import openai
import configs as cf
import time
from process.saveResults import *
from prompt.promptExamples import *
from prompt.promptInstructions import *
from prompt.promptRoles import *
from process.dataProccessing import *
from process.resultHandling import *

openai.organization = cf.OPENAI_ORG


def askGPT(prompt):
    time.sleep(30)
    openai.api_key = cf.OPENAI_KEY
    completion = openai.ChatCompletion.create(
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
    stage = "C" # C for create acceptance criteria, U for update acceptance criteria
    allCompletions = []

    initialPrompt = promptInput[0]
    input = promptInput[1]
    preOutput = ''

    ## Pop user and assistant prompt for each iteration, with system role in first iteration
    while(input):

        if stage == "C":
            newInput = input.pop(0)
            currentInput = initialPrompt + [newInput]  # system, user, assistant

            currentOutput, completion = askGPT(currentInput)
            currentOutput = removeBlankLines(currentOutput)
            preOutput = currentOutput
            stage = "U"

            output = output + currentOutput + '\n'
            outputs.append(currentOutput)
            history.append((currentInput, currentOutput))
            allCompletions.append(completion)
            continue

        else:
            newInput = input.pop(0)
            updatedInput = preOutput + newInput["content"]
            newInput["content"] = updatedInput
            currentInput = initialPrompt + [newInput]  # system, user, assistant
            currentOuput, completion = askGPT(currentInput)
            currentOuput = removeBlankLines(currentOuput)
            preOutput = currentOutput

            output = output + currentOuput + '\n'
            outputs.append(currentOuput)
            history.append((currentInput, currentOuput))
            allCompletions.append(completion)
            continue


    return output, outputs, history, allCompletions



def runByProject(numbers, ratio, cases):
    for projectNo in numbers:

        fn = "UserStories/g" + projectNo + ".txt"
        file = open(fn, "r")  #
        stories = file.readlines()
        # for usNo in range(len(stories)):
        for usNo in cases:
            us = "User Story: \n" + stories[usNo]

            print("-" * 70)
            print(us)

            myPrompt = constructeInput(us)

            ac, all_output, all_history, all_completions = bufferedChat(us, myPrompt)
            print("=" * 20 + "AC for Group " + projectNo + "=" * 20)
            print(ac)
            usNo = str(usNo)
            writeACbyProject(us, ac, projectNo, usNo)
            processFinalACbyProject(us, projectNo, usNo, ratio)


def constructeInput(us):
    usFile, pbExample, qaExample, pmExample = readExamplesAC("1")
    usFile2, pbExample2, qaExample2, pmExample2 = readExamplesAC("2")
    usFile3, pbExample3, qaExample3, pmExample3 = readExamplesAC("3")

    initSysContent = readInstruction("../Instructions/initialSystem.txt")
    roleDes = readRoleInstruction("../Instructions/Roles.txt")
    outputFormat = readInstruction("../Instructions/outputFormat.txt")

    contextAndRole = [{"role": "system",
                 "content": initSysContent + "\n" + outputFormat + "\n" + "Here are role instructions in this activity.\n"  + roleDes + "\n"}]

    command_1 = "Write acceptance criteria for the given user story as the Product Owner and Business Analyst:\n"
    command_2 = "Update or supplement the above acceptance criteria for given user story as a Quality Analyst if necessary.\n"
    command_3 = "Update or supplement the above acceptance criteria for given user story as other team members if necessary.\n"

    learning = [{"role": "user",
                 "content": command_1 + usFile + "\n" },
                {"role": "assistant",
                 "content": pbExample + "\n"},
                {"role": "user",
                 "content": command_2 + usFile + " \n" },
                {"role": "assistant", "content": qaExample + "\n"},
                {"role": "user",
                 "content": command_3 + usFile + " \n" },
                {"role": "assistant","content": pmExample + "\n"},
                {"role": "user",
                 "content": command_1 + usFile2 + "\n" },
                {"role": "assistant",
                 "content": pbExample2 + "\n"},
                {"role": "user",
                 "content": command_2+ usFile2 + " \n"},
                {"role": "assistant", "content": qaExample2 + "\n"},
                {"role": "user",
                 "content": command_3 + usFile2 + " \n" },
                {"role": "assistant", "content": pmExample2 + "\n"},
                {"role": "user",
                 "content": command_1+ usFile3 + "\n"},
                {"role": "assistant",
                 "content": pbExample3 + "\n"},
                {"role": "user",
                 "content": command_2 + usFile3 + " \n"},
                {"role": "assistant", "content": qaExample3 + "\n"},
                {"role": "user",
                 "content": command_3 + usFile3 + " \n"},
                {"role": "assistant", "content": pmExample3 + "\n"}]

    prompts = contextAndRole + learning

    completionComands = [{"role": "user",
                          "content": command_1 + "\n" + us + "\n"},
                         {"role": "user",
                          "content": command_2 + "\n" + us + "\n"},
                         {"role": "user",
                          "content":  command_3 + "\n" + us + "\n"},
                         ]

    myInput = [prompts, completionComands]

    return myInput

projectNumbers = ["28"]
# evaluateCases = [30, 63, 53, 37, 26, 57, 65, 2, 40, 58] ## g11
# evaluateCases = [50, 27, 7, 25, 11, 26, 16, 21, 8, 1] ## g24
evaluateCases = [6, 49, 5, 20, 25, 50, 17, 3, 15, 21] ## g28
ratio = 0.95

runByProject(projectNumbers, ratio, evaluateCases)


