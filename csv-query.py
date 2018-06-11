# AUTHOR: Joshua Ortiz; 38 non-comment lines
# Script to query multiple CSV's and populate a list of servers that are
# ready to be updated. 
import csv
import string
querylist = []
fieldnames=[]
InMemoryCopy = []
# 'with open' statement auto closes the file handler; file.close() not needed
with open('SEP_CR_Uploads.csv', newline='') as csvfile:
    # To attempt to avoid encoding issues we could set a Dialect; skipped
    docreader = csv.DictReader(csvfile)
    fieldnames = docreader.fieldnames
    for row in docreader:
        # query each Title in the file, then slice the string to get
        # the values that we want to match in serverlist.csv
        querylist.append(row['[required] Title'][41:])

# With the querylist extracted from the first file we can now use it to
# query the the serverlist csv to to pull the server names to be added to .csv
serverList = []

# Intially There was an error with .csv encoding, causing  the machine name to be 
# prepended with 'ï»¿", to ignore this we would have to change the file format,
#  but instaed we can just slice the first entry if we're expecting this
#
# Initial issues were encountered because the reader is torn down after it's
# thus we have to point the reader back to the beginning of the file af
ServerDict = {}
ServerDict.setdefault('', [])
with open('serverlist.csv', newline='') as csvfile1:
    docreader1 = csv.DictReader(csvfile1)
    #i = 0
    for row in docreader1:
        if row['Patch Group'].upper() in ServerDict:
            ServerDict[row['Patch Group'].upper()].append(row["ï»¿Machine Name"])
        else:
            ServerDict[row['Patch Group'].upper()] = [row["ï»¿Machine Name"]]
# Now that we have our in-memory data structure (dictionary) created with a 
# 1:Many relationship for Group:[Servers] we can loop through the original CSV
#  again and add the servernames to  their designated spots. 
# Recall that we will now nead a DictWriter instead of DictReader
with open('SEP_CR_Uploads.csv', newline='') as csvToCopy:
    docreader = csv.reader(csvToCopy)
    for row in docreader:
        InMemoryCopy.append(row)

#Loops through the in memory copy of our orginal CSV appending the valid server
# names to their appropriate location 
EndAdd = 1
while EndAdd < len(InMemoryCopy):
    for x in querylist:
        # convert both strings to uppercase to make th
        if x.upper() in InMemoryCopy[EndAdd][1].upper():
            ListOfServers = '' 
            for i in ServerDict[x.upper()]:
                #InMemoryCopy[EndAdd][2] += (" "+ i +",")
                ListOfServers += (" "+ i + ", ")
            # .replace() doesn't alter the value of the string it's used on
            # but returns a copy, thus we have to assign this string
            InMemoryCopy[EndAdd][2] = InMemoryCopy[EndAdd][2].replace('XXXXXXXXX\n', ListOfServers+'\n')
            InMemoryCopy[EndAdd][2] = InMemoryCopy[EndAdd][2].replace('XXXXXXXXX', '')
            InMemoryCopy[EndAdd][2] = InMemoryCopy[EndAdd][2].replace('APP_GROUP_ENV', str(x))
    EndAdd += 1

with open('test.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(InMemoryCopy)
