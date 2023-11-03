def readExamplesAC(id):

    usFile = open("Examples/example_"+id+"_US.txt", "r", encoding="utf8")
    us = usFile.read()

    examplePB = open("Examples/example_"+id+"_PO_BA.txt", "r", encoding="utf8")
    pb = examplePB.read()

    exampleQA = open("Examples/example_" + id + "_QA.txt", "r", encoding="utf8")
    qa = exampleQA.read()

    examplePM = open("Examples/example_" + id + "_PM.txt", "r", encoding="utf8")
    pm = examplePM.read()

    return us, pb, qa, pm