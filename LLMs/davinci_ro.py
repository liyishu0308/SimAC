'''
danvinci model
roles with examples
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
# from resultHandling import *

openai.organization = cf.OPENAI_ORG


def askGPT(prompt):
    # time.sleep(60)
    openai.api_key = cf.OPENAI_KEY
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=2048)

    ans = completion.choices[0].text + '\n'
    print("=" * 30, "completion", "=" * 30)
    print(completion)

    return ans, completion

def bufferedChat(us, promptInput):
    history = []
    outputs = []
    output = ''
    stage = "C" # R for role instruction, C for create acceptance criteria, U for update acceptance criteria
    allCompletions = []

    initialPrompt = promptInput[0]
    input = promptInput[1]
    preOutput = ''

    ## Pop user and assistant prompt for each iteration, with system role in first iteration
    while(input):

        if stage == "C":
            newInput = input.pop(0)
            currentInput = initialPrompt + "\n" + newInput

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
            updatedInput = preOutput + "\n" + newInput
            currentInput = initialPrompt + "\n\n" + updatedInput
            currentOuput, completion = askGPT(currentInput)
            currentOuput = removeBlankLines(currentOuput)
            preOutput = currentOutput

            output = output + currentOuput + '\n'
            outputs.append(currentOuput)
            history.append((currentInput, currentOuput))
            allCompletions.append(completion)
            continue


    return output, outputs, history, allCompletions

def runByProject(numbers, scriptNo, ratio, cases):

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

            writeACbyProjectDavinci(us, ac, projectNo, scriptNo, usNo)
            writeAllResultsbyProjectDavinci(all_history, projectNo, scriptNo, usNo)
            saveCompletionsbyProjectDavinci(all_completions,projectNo, scriptNo, usNo)
            # processFinalACbyProjectDavinci(us, projectNo, scriptNo, usNo, ratio)



def constructeInput(us):
    usFile, pbExample, qaExample, pmExample = readExamplesAC("7")
    usFile2, pbExample2, qaExample2, pmExample2 = readExamplesAC("8")
    usFile3, pbExample3, qaExample3, pmExample3 = readExamplesAC("9")
    initSysContent = readInstruction("Instructions/initialSystem_4.txt")
    roleDes = readRoleInstruction("Instructions/Roles_2.txt")
    outputFormat = readInstruction("Instructions/outputFormat.txt")

    command_1 = "Write acceptance criteria for the given user story as the Product Owner and Business Analyst:\n"
    command_2 = "Update or supplement the above acceptance criteria for the given user story as a Quality Analyst if necessary.\n"
    command_3 = "Update or supplement the above acceptance criteria for the given user story as other team members if necessary.\n"
    commands = []
    commands.append(command_1)
    commands.append(command_2)
    commands.append(command_3)

    learnings = [
        command_1 + "\n" + usFile + "\n" + pbExample + "\n" + command_2 + usFile + "\n" + qaExample + "\n" + command_3 + usFile + "\n" + pmExample,
        command_1 + "\n" + usFile2 + "\n" + pbExample2 + "\n" + command_2 + usFile2 + "\n" + qaExample2 + "\n" + command_3 + usFile2 + "\n" + pmExample2,
        command_1 + "\n" + usFile3 + "\n" + pbExample3 + "\n" + command_2 + usFile + "\n" + qaExample3 + "\n" + command_3 + usFile + "\n" + pmExample3]

    contextAndRole = initSysContent + "\n" + outputFormat + "\n" + "Here are role instructions in this activity.\n" + roleDes + "\n"

    prompts = contextAndRole + "Here are some examples.\n" + learnings[1]

    completionComands = [command_1 + "\n" + us + "\n", command_2 + "\n" + us + "\n", command_3 + "\n" + us + "\n"]

    myInput = [prompts, completionComands]

    # myInput = initSysContent + "\n" + outputFormat + "\n" + "Here are role instructions in this activity.\n"  + roleDes + "\n" + \
    #           "Here are some examples.\n" + learnings[1]

    return myInput


# projectNumbers = ["02","03","04","05","08","10","11","12","13","14","16","17","18","19","21","22","23","24","25","26","27","28"]
# projectNumbers = ["23","24","25","26","27","28"]
projectNumbers = ["28"]
# evaluateCases = [30, 63, 53, 37, 26, 57, 65, 2, 40, 58] ## g11
# evaluateCases = [50, 27, 7, 25, 11, 26, 16, 21, 8, 1] ## g24
evaluateCases = [6, 49, 5, 20, 25, 50, 17, 3, 15,	21] ## g28
scriptNo = "3"
ratio = 0.9
runByProject(projectNumbers, scriptNo, ratio, evaluateCases)


