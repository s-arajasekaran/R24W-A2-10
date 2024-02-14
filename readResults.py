import sys
def readResults (path):
    i = 0
    file = open(path, 'r')
    writeFile = open("formatedReport", 'w')
    for line in file:
        if i == 0:
            writeFile.write("Longest Page found was: " + line.split("|")[0] + " with " + line.split("|")[1][:-1] + " valid tokens found\n")
        
        if i ==1:
            writeFile.write("--TOP 50 TOKEN LIST-- | format: 'token' : frequency\n")
            allTokens = line.split("|")
            total = 0
            for x in allTokens:
                if not (x=='' or x=='\n'):
                    writeFile.write("\t" + x.split("-")[0] + " : " + x.split("-")[1] + "\n")
            #print("found", total, "tokens")

        if(i ==3):
            writeFile.write("--Sub Domain List-- | format: 'subDomain' : sites found\n")
            allSubDoms = line.split("|")
            total = 0
            for x in allSubDoms:
                if not (x=='' or x=='\n'):
                    total+=1
                    writeFile.write("\t" + x.split("-")[0] + " : " + x.split("-")[1] + "\n")

            writeFile.write("-------found "+ str(total)+ " different subdomains")
        
        if (i == 2):
            writeFile.write("Unique websites encountered : " + line )
        i = i+1
    
    file.close()
    writeFile.close()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Too many arguments provided. Please only provide one input file'")
    else:
        print(readResults(sys.argv[1]))