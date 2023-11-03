def readRoleInstruction(filename):
    sign = "==========="
    f = open(filename, "r")
    roles = f.read()

    return roles

def readRoleInstructionByRole(filename):
    sign = "==========="
    f = open(filename, "r")
    ins = f.readlines()
    roles = []
    role = ''
    for i in ins:
        # print(role)
        if i.strip() == sign:
            roles.append(role)
            role = ''
            continue
        else:
            role += i

    roles = roles[1:]


    print(roles)

    return roles