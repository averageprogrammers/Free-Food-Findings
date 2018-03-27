with open('org_info.dat','r') as f:
    lst = [[] for i in range(7)]
    count = 0
    for line in f:
        if line.strip():
            lst[count].append("'" + line[1:-2].strip() + "'")
            count += 1
            if count == 7:
                break
    count = 0
    for org in lst:
        org.append("''")
    for i in range(1):
        for line in f:
            if line.strip():
                lst[count].append("'" + line.strip() + "'")
                count += 1
                if count == 7:
                    break
        count = 0
    for org in lst:
        org.append("0")
    for line in f:
        if line.strip():
            lst[count].append("'" + line.strip() + "'")
            count += 1
            if count == 7:
                break
    count = 0
    print(",".join(["(" + ",".join(org) + ")" for org in lst]))
