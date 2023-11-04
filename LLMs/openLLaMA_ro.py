'''
OpenLLaMA
'''
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = "0, 1"
import torch
from readFiles import *
from saveResults import *
from resultHandling import *
from transformers import LlamaTokenizer, LlamaForCausalLM
import time


def acProcessing(ac):
    result = ''
    lines = ac.split('\n')
    cnt = 0
    for i in lines:
        if cnt < 5:
            cnt += 1
            result += i + "\n"
            continue

        if len(i)<15:
            break

        cnt += 1
        result += i + "\n"

    return result

def textGen(project, modelName, cases, ratio, status):
    us = readUS(project)
    initSysContent = readInstruction("initialSystem_4")
    outputFormat = readInstruction("outputFormat")
    roleDes = readRoleInstruction("Instructions/Roles_2.txt")

    us1 = readExampleUS("7")
    ex1_pb = readExample("example_7_PO_BA")
    ex1_qa = readExample("example_7_QA")
    ex1_pm = readExample("example_7_PM")

    contextAndRole = initSysContent + "\n" + outputFormat + "\n" + "Here are role instructions in this activity.\n" + roleDes + "\n"

    command_1 = "Write acceptance criteria for the given user story as the Product Owner and Business Analyst:\n"
    command_2 = "Update or supplement the above acceptance criteria for the given user story as a Quality Analyst if necessary.\n"
    command_3 = "Update or supplement the above acceptance criteria for the given user story as other team members if necessary.\n"

    for i in cases:

        commands = []
        commands.append(command_1)
        commands.append(command_2)
        commands.append(command_3)

        if status == "C":
            command = commands[0]
            request = command + "\n" + us[i] + "\n"
        elif status == "U1":
            command = commands[1]
            filename = "Results/OpenLLaMA_3_2" + "/g" + project + "/" + modelName + "_" + str(i) + "_output_C.txt"
            f = open(filename, "r")
            preAC = f.read()
            request = preAC + "\n" + command + "\n" + us[i] + "\n"
        else:
            command = commands[2]
            filename = "Results/OpenLLaMA_3_2" + "/g" + project + "/" + modelName + "_" + str(i) + "_output_U1.txt"
            f = open(filename, "r")
            preAC = f.read()
            request = preAC + "\n" + command + "\n" + us[i] + "\n"

        examples = command_1 + us1 + "\n" + ex1_pb + "\n" + command_2 + us1 + "\n" + ex1_qa + "\n" + command_3 + us1 + "\n" + ex1_pm + "\n\n"

        prompt = contextAndRole + "Here are some examples.\n\n" + examples + request
        print("=" * 20, "Prompt for us_" + str(i), "=" * 20)
        print(prompt)
        print("=" * 20, "End of Prompt", "=" * 20)

        saveCurrentInput(prompt, modelName, project, str(i), status)

        # model_path = 'openlm-research/open_llama_7b'
        # model_path = 'openlm-research/open_llama_13b'
        model_path = 'open_llama_13b'

        tokenizer = LlamaTokenizer.from_pretrained(model_path)

        model = LlamaForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16,
            # device_map={"transformer.wte":0, "transformer.wpe":0, "transformer.h":3, "transformer.ln_f":3, "lm_head":3}
            device_map='auto'
        )

        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        generation_output = model.generate(
            input_ids=input_ids.cuda(),
            # max_length=4096,
            max_new_tokens=450
        )
        output = tokenizer.decode(generation_output[0])

        print(output)

        tmpId = output.find(us[i])
        tmpOutput = output[tmpId:]
        idx1 = tmpOutput.find("<start>")
        idx2 = tmpOutput.find("<end>")
        print(us[i])
        print(tmpOutput)
        print(idx1, idx2)
        currentOutput = "Acceptance Criteria:\n" + tmpOutput[idx1:idx2]
        preAC = acProcessing(currentOutput) + "<end>" + "\n"


        saveCurrentOutput(preAC, modelName, project, str(i), status)



        if status== "U2":
            allInput = []
            allOutput = []

            path =  "Results/OpenLLaMA_3_2"
            f1 = "/g" + project + "/" + modelName + "_" + str(i) + "_input_C.txt"
            f2 = "/g" + project + "/" + modelName + "_" + str(i) + "_input_U1.txt"
            f3 = "/g" + project + "/" + modelName + "_" + str(i) + "_input_U2.txt"

            f11 = "/g" + project + "/" + modelName + "_" + str(i) + "_output_C.txt"
            f22 = "/g" + project + "/" + modelName + "_" + str(i) + "_output_U1.txt"
            f33 = "/g" + project + "/" + modelName + "_" + str(i) + "_output_U2.txt"

            file1 = open(path+f1, "r")
            allInput.append(file1.read())
            file2 = open(path + f2, "r")
            allInput.append(file2.read())
            file3 = open(path + f3, "r")
            allInput.append(file3.read())

            file11 = open(path + f11, "r")
            allOutput.append(file11.read())
            file22 = open(path + f22, "r")
            allOutput.append(file22.read())
            file33 = open(path + f33, "r")
            allOutput.append(file33.read())

            saveAllInput(allInput, modelName, project, str(i), us[i])
            saveAllOuput(allOutput, modelName, project, str(i), us[i])

    return

# modelName = "OpenLLaMA_2_2" # open_llama_7b
modelName = "OpenLLaMA_3_2" # open_llama_13b

project = "28"
status = "U2" # C/U1/U2
evaluateCases = [21]
# evaluateCases = [30, 63, 53, 37, 26, 57, 65, 2, 40, 58] ## g11
# evaluateCases = [50, 27, 7, 25, 11, 26, 16, 21, 8, 1] ## g24s
# evaluateCases = [6, 49, 5, 20, 25, 50, 17, 3, 15,	21] ## g28
ratio = 0.98

textGen(project, modelName, evaluateCases, ratio, status)

# saveOuput(output, modelName, project, str(i), us[i])