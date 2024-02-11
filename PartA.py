import sys
import re
stopWords = "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves"
stopWords = stopWords.split()

#Tokenize is an O(n) runtime where n is the length of the file
#This is essentially reading every character in order (regex is at least)
#And it shouldnt double back
def tokenize(stringa):
    
    tokens = []
    #Using regex to make life easier
    try:
        tempList = re.findall(r"[A-Za-z0-9'`.]+", stringa.lower())
        for word in tempList:
            if not(word in stopWords) and (len(word) >= 2):
                tokens.append(word)
    except:
        #if file is not readable as a text file throw error as project specs say I only need
        #to read text files. Supported by edstem post 5
        #print("Error Reading the file - are you sure you supplied a txt file?'")
        fail = 1
    
    return tokens

#This is also O(N) in terms of the total number of tokens
#Im only checking every value once and addign to a master list
#And i dont loop for every value
def computeWordFrequencies(tokens, existingDict):
    #print(tokens)
    

    for t in tokens:
        if t not in existingDict:
            existingDict[t] = 1
        else:
            existingDict[t] +=1
    
    return existingDict

#This is O(nlogn) because of the sorting function
#pythons sort is complexity O(nlogn) and the printing is O(n) so the printing isnt considered
#when determining complexity
def printTokens(tokenDict):
    #using the sorted function. The first value compared is negative of freq, then the key value (the actual token)
    #this is so that although the frequencies are sorted in reverse order, alphabetical order is maintained
    # B) (im pretty proud of this solution)
    sortedDict = sorted(tokenDict.items(), key = lambda item: (-item[1], item[0]), reverse=False)
    maxNum = 50
    returnStr = ""
    for a in sortedDict:
        returnStr = returnStr + a[0]+'-'+str(a[1]) + "|"
        maxNum-=1
        if (maxNum == 0):
            return returnStr + "\n"
    
    
        
#This main function is Nlog(N)
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Too many arguments provided. Please only provide one input file'")
    else:
        printTokens(computeWordFrequencies(tokenize(sys.argv[1])))
    #Stub from testing
    #printTokens(computeWordFrequencies(tokenize('/Users/ajayra/Coding/cs 121/hw1/testfile.txt')))
    