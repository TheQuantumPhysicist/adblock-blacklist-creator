    import string
    import urllib2
    import os
    
    response = urllib2.urlopen('https://v.firebog.net/hosts/lists.php?type=tick')
    listOfListsStr = response.read()
    listOfLists = listOfListsStr.split("\n")
    
    outfile = "blacklist.txt"
    
    try:
        os.remove(outfile)
    except OSError:
        pass
    
    finalListToBlock = []
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        
    for oneListAddress in listOfLists:
        if len(oneListAddress.replace(" ","")) == 0:
            continue
    
        req = urllib2.Request(oneListAddress, headers=hdr)
    
        try:
            response = urllib2.urlopen(req)
        except Exception as ex:
            print("Failed to download list: " + oneListAddress + " ; Reason: " + str(ex))
            continue
    
        fileLinesStr = response.read()
        fileLinesStr.replace(" ","")
        fileLines = fileLinesStr.split("\n")
    
        fileLines = list(map(lambda x: x.split("#")[0], fileLines))
        fileLines = list(map(lambda x: x.replace("\n", "").replace("\r", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("127.0.0.1 ", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("127.0.0.1\t", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("0.0.0.0 ", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("0.0.0.0\t", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("255.255.255.255 ", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("255.255.255.255\t", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("0 ", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("0\t", ""), fileLines))
        fileLines = list(map(lambda x: x.replace(":: ", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("::\t", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("localhost", ""), fileLines))
        fileLines = list(map(lambda x: x.replace("::1", ""), fileLines))
        fileLines = list(filter(None, fileLines))
        fileLines = list(filter(lambda x: x.lstrip(),fileLines))
        fileLines = list(filter(lambda x: not x.startswith("#"), fileLines))
        fileLines = list(filter(lambda x: not x.isspace(), fileLines))
        fileLines = list(filter(lambda x: "<"  not in x, fileLines))
        fileLines = list(filter(lambda x: ">"  not in x, fileLines))
        fileLines = list(filter(lambda x: "#"  not in x, fileLines))
        fileLines = list(filter(lambda x: "%"  not in x, fileLines))
        fileLines = list(filter(lambda x: "{"  not in x, fileLines))
        fileLines = list(filter(lambda x: "}"  not in x, fileLines))
        fileLines = list(filter(lambda x: "|"  not in x, fileLines))
        fileLines = list(filter(lambda x: "\\" not in x, fileLines))
        fileLines = list(filter(lambda x: "^"  not in x, fileLines))
        fileLines = list(filter(lambda x: "~"  not in x, fileLines))
        fileLines = list(filter(lambda x: "["  not in x, fileLines))
        fileLines = list(filter(lambda x: "]"  not in x, fileLines))
        
        finalListToBlock = finalListToBlock + fileLines
    
    try:
        os.remove(outfile)
    except OSError:
        pass
    
    with open(outfile,"w") as fw:
        for item in finalListToBlock:
            fw.write("%s\n" % item)
