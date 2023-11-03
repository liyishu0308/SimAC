from similarity import *
import csv
import os

def allAC(name):
    filename = "Results/turbo/test" + name + "_ac.txt"
    f = open(filename, "r")
    outputs = f.readlines()
    all_output = []
    flag = False
    for i in outputs:
        i = i.strip()
        if i=="<start>":
            flag = True
            continue
        elif i=="<end>":
            flag = False
            continue
        elif flag:
            all_output.append(i[(i.find(".")+2):])
            continue
        else:
            continue
    return all_output

def allACbyProject(projectNo, usNo, modelType):
    newpath = "Results/" + modelType + "/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = newpath + "test" + projectNo + "_" + usNo + "_ac.txt"
    f = open(filename, "r")
    outputs = f.readlines()
    all_output = []
    flag = False
    for i in outputs:
        i = i.strip()
        if i=="<start>":
            flag = True
            continue
        elif i=="<end>":
            flag = False
            continue
        elif flag:
            all_output.append(i[(i.find(".")+2):])
            continue
        else:
            continue
    return all_output


def removeSimilar(ac, ratio):
    finalAC = []
    allScore = []
    for i in ac:
        if len(finalAC) == 0:
            finalAC.append(i)
        else:
            appendFlag = True
            for j in finalAC:
                score = checkSimilarity(i,j)
                pair = [i,j,score]
                allScore.append(pair)
                if(score>ratio):
                    appendFlag = False
                    # break
            if appendFlag:
                finalAC.append(i)

    return finalAC, allScore


def saveFinalAC(us, name, final_ac, threadshold):
    filename = "Results/turbo/test" + name + "_ac_final_" + str(threadshold) + "_.txt"
    f = open(filename, "w")
    f.write(us + "\n")
    f.write("Acceptance Criteria:\n")
    idx = 1
    for i in final_ac:
        f.write(str(idx) + ". " + i+"\n")
        idx += 1

def saveScores(name, scores):
    header = ['AC_1', 'AC_2', 'Score']
    filename = "Results/turbo/test" + name + "_ac_final_scores.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for i in scores:
            writer.writerow(i)

def saveFinalACbyProject(us, projectNo, final_ac, threadshold, usNo, modelType):
    newpath = "Results/" + modelType + "/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = newpath + "/test" + projectNo + "_" + usNo + "_ac_final_" + str(threadshold) + "_.txt"
    f = open(filename, "w")
    f.write(us + "\n")
    f.write("Acceptance Criteria:\n")
    idx = 1
    for i in final_ac:
        f.write(str(idx) + ". " + i+"\n")
        idx += 1

def saveFinalACbyProjectNoRatio(us, projectNo, final_ac, usNo, modelType):
    newpath = "Results/" + modelType + "/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = newpath + "/test" + projectNo + "_" + usNo + "_ac_final_.txt"
    f = open(filename, "w")
    f.write(us + "\n")
    f.write("Acceptance Criteria:\n")
    idx = 1
    for i in final_ac:
        f.write(str(idx) + ". " + i+"\n")
        idx += 1


def saveScoresbyProject(projectNo, scores, usNo, modelType):
    newpath = "Results/" + modelType + "/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    header = ['AC_1', 'AC_2', 'Score']
    filename = newpath + "/test" + projectNo + "_" + usNo + "_ac_final_scores.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for i in scores:
            writer.writerow(i)

def processFinalAC(us, name):
    pre_ac = allAC(name)
    ratio= 0.9
    final_ac, scores = removeSimilar(pre_ac, ratio)
    print("="*30, "finalAC", "="*30)
    for i in final_ac:
        print(i)
    saveFinalAC(us, name, final_ac, ratio)
    saveScores(name, scores)

def processFinalACbyProject(us, projectNo, usNo, R):
    modelType = "turbo"
    pre_ac = allACbyProject(projectNo,usNo, modelType)
    ratio= R
    final_ac, scores = removeSimilar(pre_ac, ratio)
    print("="*30, "finalAC", "="*30)
    for i in final_ac:
        print(i)
    saveFinalACbyProject(us, projectNo, final_ac, ratio, usNo, modelType)
    saveScoresbyProject(projectNo, scores, usNo, modelType)

def processFinalACbyProjectNoRatio(us, projectNo, usNo):
    modelType = "turbo"
    pre_ac = allACbyProject(projectNo, usNo, modelType)

    print("="*30, "finalAC", "="*30)
    for i in pre_ac:
        print(i)
    saveFinalACbyProjectNoRatio(us, projectNo, pre_ac, usNo, modelType)

def processFinalACbyProjectDavinci(us, projectNo, usNo, R):
    modelType = "davinci"
    pre_ac = allACbyProject(projectNo, usNo, modelType)
    ratio= R
    final_ac, scores = removeSimilar(pre_ac, ratio)
    print("="*30, "finalAC", "="*30)
    for i in final_ac:
        print(i)
    saveFinalACbyProject(us, projectNo, final_ac, ratio, usNo, modelType)
    saveScoresbyProject(projectNo, scores, usNo, modelType)

def processFinalACbyProjectDavinciNoRatio(us, projectNo, scriptNo, usNo):
    modelType = "davinci"
    pre_ac = allACbyProject(projectNo, scriptNo, usNo, modelType)

    print("="*30, "finalAC", "="*30)
    for i in pre_ac:
        print(i)
    saveFinalACbyProjectNoRatio(us, projectNo, scriptNo, pre_ac, usNo, modelType)


def resultHandlingByProjectDavinci(numbers, R, cases):
    for projectNo in numbers:
        fn = "UserStories/g" + projectNo + ".txt"
        file = open(fn, "r")  #
        stories = file.readlines()
        for usNo in cases:
            us = "User Story: \n" + stories[usNo]
            usNo = str(usNo)
            if R==1:
                processFinalACbyProjectDavinciNoRatio(us, projectNo, usNo)
            else:
                processFinalACbyProjectDavinci(us, projectNo, usNo, R)

def resultHandlingByProject(numbers, R, cases):
    for projectNo in numbers:
        fn = "UserStories/g" + projectNo + ".txt"
        file = open(fn, "r")  #
        stories = file.readlines()
        # for usNo in cases:
        for usNo in range(len(stories)):
            if usNo != 54:
                continue
            us = "User Story: \n" + stories[usNo]
            usNo = str(usNo)
            if R==1:
                processFinalACbyProjectNoRatio(us, projectNo, usNo)
            else:
                processFinalACbyProject(us, projectNo, usNo, R)
