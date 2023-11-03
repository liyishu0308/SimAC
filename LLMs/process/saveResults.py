from json import dumps
import os

def writeAllResults(history, name):
    filename = "Results/turbo/test" + name + ".txt"
    f = open(filename, "w")
    result = ''
    for pairs in history:
        result += "="*30 + "Input" + "="*30 + "\n"
        for i in pairs[0]:
            result += dumps(i) + "\n"
        result += "=" * 30 + "Output" + "=" * 30 + "\n"
        result += pairs[1] + "\n"
    f.write(result)

def writeAC(us, output, name):
    filename = "Results/turbo/test" + name + "_ac.txt"
    f = open(filename, "w")
    f.write(us + "\n" + output)

def saveCompletions(completions,name):
    filename = "Results/turbo/test" + name + "_cp.txt"
    f = open(filename, "w")
    for i in completions:
        f.write(dumps(i) + "\n")

def writeAllResultsbyProject(history, projectNo, usNo):
    newpath = "Results/turbo/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = newpath +  "/test" + projectNo + "_" + usNo + ".txt"
    f = open(filename, "w")
    result = ''
    for pairs in history:
        result += "="*30 + "Input" + "="*30 + "\n"
        for i in pairs[0]:
            result += dumps(i) + "\n"
        result += "=" * 30 + "Output" + "=" * 30 + "\n"
        result += pairs[1] + "\n"
    f.write(result)

def writeAllResultsbyProjectDavinci(history, projectNo, usNo):
    newpath = "Results/davinci/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = newpath + "/test" + projectNo + "_" + usNo + ".txt"
    f = open(filename, "w")
    result = ''
    for pairs in history:
        result += "=" * 30 + "Input" + "=" * 30 + "\n"
        result += pairs[0] + '\n'
        result += "=" * 30 + "Output" + "=" * 30 + "\n"
        result += pairs[1] + "\n"
    f.write(result)


def writeACbyProject(us, output, projectNo, usNo):
    newpath = "Results/turbo/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = newpath + "/test" + projectNo + "_" + usNo + "_ac.txt"
    f = open(filename, "w")
    f.write(us + "\n" + output)

def writeACbyProjectDavinci(us, output, projectNo, usNo):
    newpath = "Results/davinci/g" + projectNo + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = newpath + "/test" + projectNo + "_" + usNo + "_ac.txt"
    f = open(filename, "w")
    f.write(us + "\n" + output)
