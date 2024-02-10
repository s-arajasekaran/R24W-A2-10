#Test
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from PartA import tokenize, computeWordFrequencies, printTokens
import sys

global longestPage

global allWords

global hist

global uniqueList

global subDomainList


def setup():
    longestPage =  ("", 0)
    allWords= {}
    hist = []
    uniqueList = set()
    subDomainList = {}

def getStats():
    file= open("report.txt" , 'w')
    longestPage = "Longest Page was : "+ longestPage[0] + " with " + str(longestPage[1]) + " words\n"
    file.write(longestPage)
    file.write(printTokens(allWords))
    uniqueList = "Unique pages visited = " + str(len(uniqueList)) + "\n"
    file.write(uniqueList)
    for a in subDomainList:
        strToWrite = a[0] + " " + str(a[1]) + "\n"
    close(file)
    #return (longestPage, allWords, uniqueList, subDomainList)

def addToHist(url):
    if (len(hist) < 15):
        hist.append(url)
    else:
        hist.pop()
        hist.append(url)

def inHist(url):
    similarity = 0
    for i in hist:
        lent = max(len(url), len(i))
        for z in range(min(len(url), len(i))):
            if url[z] == i[z]:
                similarity +=1
        if similarity / lent >= 0.9:
            return True
    return False

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    addToHist(url)
    #print("Getting here")
    # Implementation required.
    # url: the URL that was used to get the page
    urlStr = urlparse(url).geturl
    #reExp = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)"
    if resp.raw_response == None:
        return list()
    try:
        respToStrin = resp.raw_response.content.decode('utf-8')
    except:
        #bad encoding
        return list()
    soup = BeautifulSoup(respToStrin)
    #print(soup.prettify())
    allLinks = []
    for link in soup.find_all('a'):
        thisLink = link.get('href')
        if not (thisLink in hist):
            allLinks.append(thisLink)
    thisPageLen = 0
    for stringa in soup.stripped_strings:
        listA = tokenize(stringa)
        thisPageLen += len(listA)
        allWords = computeWordFrequencies(listA, allWords)
    if (thisPageLen > longestPage[1]):
        longestPage[1] = thisPageLen
        longestPage[0] = url

    newUrl = url.split("#")
    uniqueList.append(newUrl[0])

    if ("ics.uci.edu" in url):
        newUrl = url.split(".edu")
        newUrl = newUrl[0] + ".edu"
        if newUrl not in subDomainList:
            subDomainList[newUrl] = 1
        else:
            subDomainList[newUrl] +=1
    

        
    #print(respToStrin)
    #allLinks = re.findall(reExp, respToStrin)
    #print(allLinks)
    #print(len(allLinks))
    print("Crawled link :", url, "Found :",len(allLinks), "Links" )
    #if (allLinks != None):
     #   for l in allLinks:
      #      if not (is_valid(l)):
       #         allLinks.remove(l)
    
    return allLinks
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

def helper(url):
    if ".ics.uci.edu/" in url or ".cs.uci.edu/" in url or ".informatics.uci.edu/" in url  or ".stat.uci.edu/" in url:
        return True
    else:
        return False

def is_valid(url):
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
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
