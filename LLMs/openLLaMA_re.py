'''
OpenLLaMA
https://huggingface.co/docs/transformers/main/model_doc/open-llama
'''
import torch
from readFiles import *
from saveResults import *
from resultHandling import *
from transformers import LlamaTokenizer, LlamaForCausalLM

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

def textGen(project, modelName, cases):
    us = readUS(project)
    initSysContent = readInstruction("initialSystem_7")
    outputFormat = readInstruction("outputFormat")

    us1 = readExampleUS("7")
    ex1_pb = readExample("example_7_PO_BA")
    ex1_qa = readExample("example_7_QA")
    ex1_pm = readExample("example_7_PM")
    us2 = readExampleUS("8")
    ex2_pb = readExample("example_8_PO_BA")
    ex2_qa = readExample("example_8_QA")
    ex2_pm = readExample("example_8_PM")
    us3 = readExampleUS("9")
    ex3_pb = readExample("example_9_PO_BA")
    ex3_qa = readExample("example_9_QA")
    ex3_pm = readExample("example_9_PM")

    contextAndRole = initSysContent + "\n" + outputFormat + "\n"

    command = "Write acceptance criteria for the given user story:\n"


    for i in cases:

        allOutput = []
        allInput = []
        originOutput = []

        request = command + "\n" + us[i] + "\n"
        # examples = command + us1 + "\n" + ex1_pb + "\n" + command + us2 + "\n" + ex2_pb + "\n" + command + us3 + "\n" + ex3_pb + "\n"
        examples = command + "\n" + us1 + "\n" + ex1_pb + "\n"

        prompt = contextAndRole + "\n" + "Here are some examples.\n\n" + examples + "\n" + request
        print("=" * 20, "Prompt for us_" + str(i), "=" * 20)
        print(prompt)
        print("=" * 20, "End of Prompt", "=" * 20)
        allInput.append(prompt)

        # model_path = 'openlm-research/open_llama_3b'
        # model_path = 'openlm-research/open_llama_7b'
        # model_path = 'openlm-research/open_llama_13b'
        model_path = 'open_llama_13b'

        tokenizer = LlamaTokenizer.from_pretrained(model_path)
        model = LlamaForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.float16, device_map='auto',
        )

        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        generation_output = model.generate(
            input_ids=input_ids.cuda(),
            # max_length=4096,
            max_new_tokens=450
        )
        output = tokenizer.decode(generation_output[0])

        originOutput.append(output)

        print("="*20, "Results for us_" + str(i), "="*20)
        print(output)
        tmpId = output.find(us[i])
        tmpOutput = output[tmpId:]


        # print("=" * 50)
        # print("=" * 20, "tmpOutput", "=" * 20)
        # print(tmpOutput)

        idx1 = tmpOutput.find("<start>")
        idx2 = tmpOutput.find("<end>")
        currentOutput = "Acceptance Criteria:\n" + tmpOutput[idx1:idx2]
        preAC = acProcessing(currentOutput) + "<end>" + "\n"

        # print("=" * 50)
        # print("=" * 20, "Output Only", "=" * 20)
        # print(preAC)
        allOutput.append(preAC)

        # print("=" * 20, "AllOutput", "=" * 20)
        # for i in allOutput:
        #     print(i)
        #     print("\n")

        saveAllInput(allInput, modelName, project, str(i), us[i])
        saveAllOuput(allOutput, modelName, project, str(i), us[i])
        saveAllOriginOuput(allInput, modelName, project, str(i), us[i])

        # processFinalACbyProject(us[i], project, modelName, i, ratio)

        # return allInput, allOutput
    return

# modelName = "OpenLLaMA_nr_2" # open_llama_7b
modelName = "OpenLLaMA_nr_3" # open_llama_13b

project = "28"
evaluateCases = [21]
# evaluateCases = [30, 63, 53, 37, 26, 57, 65, 2, 40, 58] ## g11
# evaluateCases = [50, 27, 7, 25, 11, 26, 16, 21, 8, 1] ## g24
# evaluateCases = [6, 49, 5, 20, 25, 50, 17, 3, 15, 21] ## g28
ratio = 0.99

textGen(project, modelName, evaluateCases)

# saveOuput(output, modelName, project, str(i), us[i])