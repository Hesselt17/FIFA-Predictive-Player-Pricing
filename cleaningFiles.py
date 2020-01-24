'''
Created on Apr 16, 2019

@author: sarasklenka
'''
import csv

import unicodedata
from curses.ascii import isdigit
from tkinter.tix import ROW

def strip_accents(text):
    """
    Strip accents from input String.
    :param text: The input string.
    :type text: String.
    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def writeFileAsLines(fname,lines):
    """
    fname is a String, a path to a file that
    will be created.
    lines is a list of line-lists, where each line-list
    is a list of words (representing lines in a file)
    
    Create a file with fname and write
    each element/sub-list of lines to the file as a line
    Each line written will have a single space between
    the words on the line
    """
    f = open(fname,"w", encoding="utf-8")
    for line in lines:
        line = [str(x) for x in line]
        f.write(' '.join(line))
        f.write("\n")
    f.close()

def process(fut, fifa):
    playerD = {}
    csvfFifa = open(fifa, 'r', encoding='utf8')
    freaderFifa = csv.reader(csvfFifa,delimiter=',',quotechar='"')
    headerFifa = next(freaderFifa)
    print(headerFifa)
    csvfFut = open(fut, 'r', encoding='utf8')
    freaderFut = csv.reader(csvfFut,delimiter=',',quotechar='"')
    headerFut = next(freaderFut)
    print(headerFut)
    for row in freaderFifa:
        name = row[2]
        name = name.split()
        for i in range(len(name)):
            name[i] = strip_accents(name[i])
        name = " ".join(name)
        release = row[-1]
        if len(release) != 0:
            if isdigit(release[0]) == False: #euro sign
                release = release[1:]
            if "M" in release:
                release = float(release[:-1])*1000000
            elif "K" in release:
                release = float(release[:-1])*1000
            else:
                release = float(release)
        row[-1] = release
        height = row[26]
        height1= row[26]
        height = height.split("'")
        if len(height) == 2:
            height = int(height[0])*12 + int(height[1])
        row[26] = height
        country = row[5]
        c = ""
        for i in country:
            if i != " ":
                c += i 
        country = c
        name = name + " " + country
        if name not in playerD:
            playerD[name] = row + [0] + [0] #initialize spot for FUT price and occurences

    names = set(playerD.keys())
    ret = 0
    ouch = 0
    ct = 0

    print()
    missing = []
    countries2 = set()
    for row in freaderFut:
        name = row[1]
        name = name.split()
        for i in range(len(name)):
            name[i] = strip_accents(name[i])
        name = " ".join(name)
        country = row[20]
        countries2.add(country)
        c = ""
        for i in country:
            if i != " ":
                c += i 
        country = c
        if country == 'Holland':
            country = 'Netherlands'
        name = name + " " + country
        
        price = row[3]
        for i in range(len(price)):
            if price[i] == 'K':
                price = float(price[:i])*1000
            elif price[i] == 'M':
                price = float(price[:i])*1000000
        price = float(price)
        check = False
        if name in playerD: #only add highest price
            check = True
            playerD[name][-2] += price
            playerD[name][-1] += 1
        elif " ".join(name.split()[1:]) in playerD:
            ct += 1
            check = True
            playerD[" ".join(name.split()[1:])][-2] += price
            playerD[" ".join(name.split()[1:])][-1] += 1
        else: #name doesn't match exactly
            nameSplit = name.split()
            if len(nameSplit) != 2: #2 because we name name + club
                initial = nameSplit[0][0] + ". " + " ".join(nameSplit[1:])
            if len(nameSplit) == 2 and nameSplit[0] not in playerD:
                if name not in playerD:
                    ouch += 1
            elif initial in names: #initial is first name
                check = True
                if initial in playerD: #only add highest price
                    playerD[initial][-2] += price
                    playerD[initial][-1] += 1
                ret += 1
        if not check:
            missing.append(name)
            
    for k, v in playerD.items():
        if v[-1] != 0:
            playerD[k] = v[:-2] + [float(v[-2])/float(v[-1])]

    with open('processed.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        header = ['place'] + headerFifa[1:] + ['FUT Price']
        print(header)
        wr.writerow(header)
        for k, v in sorted(playerD.items(), key = lambda x: x[1][-1], reverse = True):
            if v[-1] != 0:
                v = [strip_accents(str(x)) for x in v]
                wr.writerow(v)
        myfile.close()
        
    print('done')
    
def changePostions(fname):
    csvf = open(fname, 'r', encoding='utf8')
    freader= csv.reader(csvf,delimiter=',',quotechar='"')
    header = next(freader)
    d = {}
    for row in freader:
        for i in range(28,54):
            if "+" in row[i]:
                row[i] = sum([int(x) for x in row[i].split("+")])
        release = row[-3]
        if len(release) != 0:
            if isdigit(release[0]) == False: #euro sign
                release = release[1:]
            if "M" in release:
                release = float(release[:-1])*1000000
            elif "K" in release:
                release = float(release[:-1])*1000
            else:
                release = float(release)
        row[-3] = release
        value = row[11]
        if len(value) != 0:
            if isdigit(value[0]) == False: #euro sign
                value = value[1:]
            if "M" in value:
                value = float(value[:-1])*1000000
            elif "K" in value:
                value = float(value[:-1])*1000
            else:
                value = float(value)
            row[11] = value
        d[row[1]] = row    
    print(d['20801'])    
    with open('finalProcessed.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        header = ['place'] + header[1:] + ['FUT Price']
        
        wr.writerow(header)
        for k, v in sorted(d.items(), key = lambda x: x[1][-1], reverse = True):
            if v[-1] != 0:
                v = [strip_accents(str(x)) for x in v]
                wr.writerow(v)
        myfile.close()
    print('done')
    
def attachCards(fname, cards):
    csvf = open(fname, 'r', encoding='utf8')
    freader= csv.reader(csvf,delimiter=',',quotechar='"')
    header = next(freader)
    d = {}
    cd = {}
    csvfC = open(cards, 'r', encoding='utf8')
    freaderC= csv.reader(csvfC,delimiter=',',quotechar='"')
    headerC = next(freaderC)

    for row in freader:
        d[row[2]] = row + [0]
    for row in freaderC:
        fin = []
        for i in row: 
            i = strip_accents(str(i))
            fin.append(i)
        cd[fin[1]] = fin
    ct = 0
    for k,v in cd.items():
        if k in d:
            d[k][-1] = cd[k][3]
        else:
            bool = False
            initialDisplay = k.split()
            if len(initialDisplay) > 1:
                initialDisplay = initialDisplay[0][0] + ". " + " ".join(initialDisplay[1:])
                if initialDisplay in d:
                    d[initialDisplay][-1] = cd[k][3]
                    bool = True
            initialFull = cd[k][2].split()
            if len(initialFull) > 1:
                initialFull = initialFull[0][0] + ". " + " ".join(initialFull[1:])
                if initialFull in d:
                    d[initialFull][-1] = cd[k][3]
                    bool = True
        
    with open('cardProcessed.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        header = ['place'] + header[1:-1] + ['card']
        print()
        wr.writerow(header)
        for k, v in d.items():
            if v[-1] != 0:
                v = [strip_accents(str(x)) for x in v]
                wr.writerow(v)
        myfile.close()
    print('done')

if __name__ == '__main__':
    process("fut.csv", "fifa.csv")
    changePostions("processed.csv")
    attachCards("finalProcessed.csv", "cards.csv")
    
    