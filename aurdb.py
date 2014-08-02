#!/usr/bin/python3

import AUR
import urllib.request
import gzip
import io
import sqlite3
import os

aur = AUR.RPC.AUR()

gzdata=urllib.request.urlopen("http://cryptocrack.de/files/aurpkglist.txt.gz").read()
gz=gzip.GzipFile(fileobj=io.BytesIO(gzdata))
gz.readline() #Skip first line
data=gz.read().decode().replace("%2B","+")

#Ther must be a better way to do this
packages=[j[0] for j in (i.split(' ') for i in data.split('\n'))]

#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

os.remove('/tmp/aur.db')
con = sqlite3.connect('/tmp/aur.db')
cur = con.cursor()    

cur.execute("CREATE TABLE packages(Depends TEXT, Provides TEXT, Name TEXT PRIMARY KEY, URL TEXT, Maintainer TEXT, URLPath TEXT, MakeDepends TEXT, Replaces TEXT, PackageBaseID INT, OptDepends TEXT, License TEXT, OutOfDate INT, FirstSubmitted INT, CategoryID INT, CheckDepends TEXT, Conflicts, Description TEXT, NumVotes INT, Groups, LastModified INT, ID INT, PackageBase TEXT, Version TEXT)")

for chunk in chunks(packages, 100): 
    for pkg in aur.info(list(chunk)):
        l=[]
        for i in ['Depends', 'Provides', 'Name', 'URL', 'Maintainer', 'URLPath', 'MakeDepends', 'Replaces', 'PackageBaseID', 'OptDepends', 'License', 'OutOfDate', 'FirstSubmitted', 'CategoryID', 'CheckDepends', 'Conflicts', 'Description', 'NumVotes', 'Groups', 'LastModified', 'ID', 'PackageBase', 'Version']:
            if i not in pkg:
                l.append('')
            elif isinstance(pkg[i],list):
                l.append(','.join(pkg[i]))
            else:
                l.append(pkg[i])
        cur.execute("INSERT INTO packages VALUES (?"+22*',?'+")", l)
        con.commit()

con.close()