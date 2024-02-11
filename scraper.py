#Test
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from PartA import tokenize, computeWordFrequencies, printTokens
import sys






    

def getStats(metaData):
    longestPage =  metaData[0]
    allWords= metaData[1]
    hist = metaData[2]
    uniqueList = metaData[3]
    subDomainList = metaData[4]

    file= open("report.txt" , 'w')
    longestPage = longestPage[0] + "|" + str(longestPage[1]) + "\n"
    if (longestPage!= None):
        file.write(longestPage)
    else:
        file.write("\n")
    if (allWords!= {}):
        file.write(printTokens(allWords))
    else:
        file.write("\n")
    if (uniqueList!= None):
        uniqueList = str(len(uniqueList)) + "\n"
        file.write(uniqueList)
    else:
        file.write("0")
    if(subDomainList !=None):
        for a in subDomainList:
            strToWrite = a[0] + " " + str(a[1]) + "|"
            file.write(strToWrite)
        file.write("\n")
    else:
        file.write("\n")
    file.close()
    #return (longestPage, allWords, uniqueList, subDomainList)


def addToHist(url, hist):
    if (len(hist) < 15):
        hist.append(url)
    else:
        hist.pop()
        hist.append(url)

def inHist(url, hist):
    similarity = 0
    total = 0
    for a in hist:
        if (url == hist):
            similarity+=1
        total+=1
    return similarity/total > (10/15)
    

def scraper(url, resp, md):
    res = extract_next_links(url, resp, md)
    links = res[0]
    return ([link for link in links if is_valid(link)], res[1])

def extract_next_links(url, resp, metaData):
    longestPage =  metaData[0]
    allWords= metaData[1]
    hist = metaData[2]
    uniqueList = metaData[3]
    subDomainList = metaData[4]
    if (resp.status !=  200):
        return (list(), metaData)
    #addToHist(url, hist)
    

    #print("Getting here")
    # Implementation required.
    # url: the URL that was used to get the page
    urlStr = urlparse(url).geturl

    #reExp = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)"
    if resp.raw_response == None:
        return (list(), metaData)
    try:
        respToStrin = resp.raw_response.content.decode('utf-8')
    except:
        #bad encoding
        return (list(), metaData)

    addToHist(url.split("?")[0], hist)

    if ("ics.uci.edu" in url):
        subDomURL = url.split(".edu")
        subDomURL = newUrl[0] + ".edu"
        if subDomURL not in subDomainList:
            subDomainList[subDomURL] = 1
        else:
            subDomainList[subDomURL] +=1
    else:
        print("URL NOT A SUBDOMAIN ========== ", url)
    soup = BeautifulSoup(respToStrin)
    #print(soup.prettify())
    allLinks = []
    for link in soup.find_all('a'):
        thisLink = link.get('href')
        #print(thisLink, end=' ')
        if (not inHist(thisLink.split("?")[0], hist)):
            allLinks.append(thisLink)
    thisPageLen = 0
    for stringa in soup.stripped_strings:
        listA = tokenize(stringa)
        thisPageLen += len(listA)
        allWords = computeWordFrequencies(listA, allWords)
    if (thisPageLen > longestPage[1]):
        longestPage = (url, thisPageLen)
        #longestPage[0] = url

    newUrl = url.split("#")
    uniqueList.add(newUrl[0])

    
    

        
    #print(respToStrin)
    #allLinks = re.findall(reExp, respToStrin)
    #print(allLinks)
    #print(len(allLinks))
    print("Crawled link # :", len(uniqueList), " : ", url)
    #if (allLinks != None):
     #   for l in allLinks:
      #      if not (is_valid(l)):
       #         allLinks.remove(l)
    
    return (allLinks, (longestPage, allWords, hist, uniqueList, subDomainList))
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
