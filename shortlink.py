import dbm
import random

dbName = "data/shortLink"
uppercase_letters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def keyExists(key):
    with dbm.open(dbName, 'c') as db:
        if key in db:
            return True
        else:
            return False


def keyGen(length:int=5):
    random_letters = ""
    for i in range(length):
        random_letter = random.choice(uppercase_letters)
        random_letters += random_letter
    return random_letters

def genUniqueKey(length:int=5):
    key = keyGen(length)
    #print(key)
    while keyExists(key) == True:     
        key = keyGen(length)
        print(key)
    return key
        
def addKey(key,url):
    with dbm.open(dbName, 'w') as db:
        db[key] = url 
        print(getURL(key))

def getURL(key):
    with dbm.open(dbName, 'r') as db:
        return str(db[key],encoding='utf-8')

def createURL(url,customkey:str=False,length:int=5):
    if customkey == False:
        key = genUniqueKey(length)
    else:
        key = customkey
    if keyExists(url) == False:       
        addKey(key,url)
        addKey(url,key)
        print("Adding:",f"{key}:{url}")
        return(key)
    else:
        output = getURL(url)
        print("Found existing URL:",output)
        return(output)

