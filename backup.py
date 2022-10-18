
from datetime import date, datetime
from http import cookies
import logging
from time import sleep
import pip._vendor.requests as requests
import os

jar = []

customerlisturl = "http://brqassociates.in/webapp/backup/customer_list.php"
generatedbbackupurl = "http://brqassociates.in/webapp/backup/generate_database_backup_link.php"
zipurlinitpart = "http://brqassociates.in/webapp/backup/"
directorypath = str(date.today())

headers = {'user-agent': 'BRQ Glob Tech'}
respo = requests.get(customerlisturl,headers=headers)
jar = respo.cookies
cont = str(respo.content)
cidArrays = cont.split("c_id=\"")
cnameArrays = cont.split("c_com_name=\"")
cidArrays.pop(0)
cnameArrays.pop(0)
cidcnameArray = []
# print("Start Time: " + str(datetime.now()))
for indx,cid in enumerate(cidArrays):
    cidcnameArray.append({'cid': cid.split("\"")[0], 'cname': cnameArrays[indx].split("\"")[0]})
for idx,cidcname in enumerate(cidcnameArray):
    try:
        payload = {'c_id':cidcname.get('cid'), 'c_com_name': cidcname.get('cname')}
        respogenerateclick = requests.post(generatedbbackupurl, headers=headers, data=payload, cookies=jar)
        zipurlfinalpart = str(respogenerateclick.content).split("<a href=\"")[1].split("\" download class")[0]
        responseZIP = requests.get(zipurlinitpart+zipurlfinalpart, headers=headers, cookies=jar)
        isExist = os.path.exists(directorypath)
        if not isExist:
            os.makedirs(directorypath)
        file = open(directorypath + "/" + zipurlfinalpart, "wb")
        file.write(responseZIP.content)
        file.close()
        print("Downloaded " + str(idx+1) + " of " + str(len(cidcnameArray)))
    except Exception as e:
        # creating/opening a file
        f = open("exceptions.txt", "a")
        # writing in the file
        f.writelines("Error creating backup of "
            + cidcname.get('cname')
            + "( " + cidcname.get('cid') + " )"
            + ": " + str(e) + "\n\n")
        # closing the file
        f.close()
print("Done !")
print("End Time: " + str(datetime.now()))