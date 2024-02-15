#Test
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from PartA import tokenize, computeWordFrequencies, printTokens, checkSum
import sys






    
#Function to write out final statistics based on metaData Gathered
def getStats(metaData):
    longestPage =  metaData[0]
    allWords= metaData[1]
    hist = metaData[2]
    uniqueList = metaData[3]
    subDomainList = metaData[4]

    file= open("report.txt" , 'w')
    longestPage = longestPage[0] + "|" + str(longestPage[1]) + "\n"

    #write longest page
    if (longestPage!= None):
        file.write(longestPage)
    else:
        file.write("\n")

    #write 50 top tokens
    if (allWords!= {}):
        file.write(printTokens(allWords))
    else:
        file.write("\n")

    #print num unique sites
    if (uniqueList!= None):
        uniqueList = str(len(uniqueList)) + "\n"
        file.write(uniqueList)
    else:
        file.write("0")
    
    #print subdomain list
    if(subDomainList !=None):
        returnStr = ''
        for a in subDomainList:
            returnStr = returnStr + a +'-'+str(subDomainList[a]) + "|"
        returnStr += '\n'
        file.write(returnStr)
    else:
        file.write("\n")
    file.close()
    #return (longestPage, allWords, uniqueList, subDomainList)

#Function to turn a list (in this case hist) into essentially a queue
#Holds up to the last 15 links
def addToHist(url, hist):
    if (len(hist) < 15):
        hist.append(url)
    else:
        hist.pop()
        hist.append(url)

#Compares two strings and returns whether they have more than a single character different
#originally intended as a 90% rule but changed as we realized that % depend on the length of the 
#string itself, so percentage cutoff is determined by 1/len(str)
def ninetyRule(urlA, urlB):
    #return Flase
    if (len(urlA) != len(urlB)):
        return False
    else:
        i = 0
        sim = 0
        while (i < len(urlA)):
            if urlA[i] == urlB[i]:
                sim+=1
            i+=1
        if (i == 0):
            return False
        return (sim/i) >= (1 - 1/i)

#Check if a link is in the history
#Url is passed as a path url (the url minus the query/fragment)
def inHist(url, hist):
    #First 15 websites ignored
    if (len(hist) < 15):
        return False
    similarity = 0
    total = 0
    #how many path urls are the same over the last 15 links visited
    for a in hist:
        if (url == hist):
            similarity+=1
        total+=1
    
    #if the path url matches at least 10 of the last links then it is technically a trap
    if similarity/total > (10/15):
        return True
    else:
        #Redundant checking based on last part of the url
        #print(url.split("/"))
        #print(a.split("/"))
        #get last part of path and check if 90% similar with ANY of the last 15 links - if yes then consider it a trap
        #meant to catch calander links with path based dates such as ics.uci.edu/2021-04-02/ etc
        

        #in case link ends in a / get path before
        splturl = url.split("/")[-1]
        if (len(url.split("/"))<=1):
            return False
        if splturl == '':
            splturl =url.split("/")[-2]

        for a in hist:
            aSplit = a.split("/")[-1]
            if (len(url.split("/"))>1):
                if aSplit == '':
                    aSplit = a.split("/")[-2]
                if (ninetyRule(splturl, aSplit)):
                    return True
        return False
    

def scraper(url, resp, md):
    res = extract_next_links(url, resp, md)
    links = res[0]
    return ([link for link in links if is_valid(link)], res[1])

def extract_next_links(url, resp, metaData):
    #extract metaData tuple into variables so we can alter without changing the passed metadata
    #in case we determine a website is invalid- in which case we would return teh original
    #metadata without added stats from this page
    print(url)
    longestPage =  metaData[0]
    allWords= metaData[1]
    hist = metaData[2]
    uniqueList = metaData[3]
    subDomainList = metaData[4]
    checkSumAll = metaData[5]

    #early return and dont crawl if response is not 200
    if (resp.status !=  200):
        print("---------------------Page Cut for non-200 response----------------")
        return (list(), metaData)
    #addToHist(url, hist)
    

    #print("Getting here")
    # Implementation required.
    # url: the URL that was used to get the page
    urlStr = urlparse(url).geturl

    #early return and dont crawl if response is invalid sometimes (edge case that we encountered testing)
    if resp.raw_response == None:
        print("---------------------Page Cut for no Response----------------")
        return (list(), metaData)
    try:
        respToStrin = resp.raw_response.content.decode('utf-8')
    except:
        print("---------------------Page Cut for bad encoding----------------")
        #bad encoding
        return (list(), metaData)

    #get the path url and check if in history - to help in case one link adds 100 calander links
    #the links may not get stopped when checking  below so we catch them here
    if (inHist(url.split("?")[0], hist)):
        print("---------------------Page Cut for trap Detection----------------")
         return (list(), metaData)

    addToHist(url.split("?")[0], hist)

    
    
    soup = BeautifulSoup(respToStrin)
    #print(soup.prettify())

    #cut out any links that may be traps
    allLinks = []
    for link in soup.find_all('a'):
        thisLink = link.get('href')
        #print(thisLink, end=' ')
        if (thisLink != None) and (not inHist(thisLink.split("?")[0], hist)):
            allLinks.append(thisLink)
    thisPageLen = 0
    numTokens = 0
    #parse the page fro non html element strings
    #count unique tokens at the same time
    #if unique tokens under 50 (not includign stop words) we consider a page low information
    #dont crawl (although we already did) we just dont include the information in statistics
    #and dont add any new links found
    for stringa in soup.stripped_strings:
        tokenizeRes  = tokenize(stringa)
        listA = tokenizeRes[0]

        thisPageLen += tokenizeRes[1]
        numTokens += len(set(listA))
        allWords = computeWordFrequencies(listA, allWords)
    
    #checksum implementation
    checkSumRes = checkSum(allWords, checkSumAll)
    if not (checkSumRes[1]):
        #sum was in history exact duplicate found
        return (list(), metaData)
    else:
        checkSumAll = checkSumRes[0]
    

    if (thisPageLen > longestPage[1]):
        longestPage = (url, thisPageLen)
        #longestPage[0] = url
    


    if(numTokens < 50 ):
        #print(numTokens)
        print("---------------------Page Cut for Inssufficent Information----------------")
        return (list(), metaData)
    
    
    #subdomain adder
    if ("ics.uci.edu" in url):
        subDomURL = url.split(".edu")
        subDomURL = subDomURL[0] + ".edu"
        if subDomURL not in subDomainList:
            subDomainList[subDomURL] = 1
        else:
            subDomainList[subDomURL] +=1
    
    #unique URL adder
    newUrl = url.split("#")
    uniqueList.add(newUrl[0])
    

    #fragment from early build
    #print(respToStrin)
    #allLinks = re.findall(reExp, respToStrin)
    #print(allLinks)
    #print(len(allLinks))
    #print("Crawled link # :", len(uniqueList), " : ", url)
    #if (allLinks != None):
     #   for l in allLinks:
      #      if not (is_valid(l)):
       #         allLinks.remove(l)
    
    #rebuild metadata tuple with all new information to reflect a successfull crawl
    return (allLinks, (longestPage, allWords, hist, uniqueList, subDomainList, checkSumAll))
    #re.match(".ics.uci.edu/")

    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page! 
    # we will use the beautifulSoup to get the html content
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    #return list()

#just adding to is_valid to check if the link is within the restricted domains
def helper(url):
    if ".ics.uci.edu" in url or ".cs.uci.edu" in url or ".informatics.uci.edu" in url  or ".stat.uci.edu" in url:
        return True
    else:
        return False

def is_valid(url):
    #print(url)
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
#         *.ics.uci.edu/*
# *.cs.uci.edu/*
# *.informatics.uci.edu/*
# *.stat.uci.edu/*
        if parsed.scheme not in set(["http", "https"]) or not(helper(url)) :
            return False
        return (not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())) and (not ".pdf" in url) and (not ".txt" in url)

    except TypeError:
        print ("TypeError for ", parsed)
        raise
