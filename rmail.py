import requests
import json
import time
import os
import html2text
import argparse

apiBaseURL = "https://www.1secmail.com/api/v1/"
domainList = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net",
    "wwjmp.com",
    "esiix.com",
    "xojxe.com",
    "yoggm.com",
    "oosln.com",
    "vddaz.com"
]
prefFilePath = "pref.json"

def banner():
    print('''

        ██████╗░░░░░░░███╗░░░███╗░█████╗░██╗██╗░░░░░
        ██╔══██╗░░░░░░████╗░████║██╔══██╗██║██║░░░░░
        ██████╔╝█████╗██╔████╔██║███████║██║██║░░░░░
        ██╔══██╗╚════╝██║╚██╔╝██║██╔══██║██║██║░░░░░
        ██║░░██║░░░░░░██║░╚═╝░██║██║░░██║██║███████╗
        ╚═╝░░╚═╝░░░░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚══════╝
                               written by @annomroot 
    =--------------------------------------------------=
''')
    
def endLine():
    print('''
    =-------------------------------------------------------=
    ''')

def heading(headtxt):
    print('''
    =-[ '''+headtxt+''' ]------------------------------=
    ''')

def welcome():
    print('''
    =--[WELCOME]-----------------------------------------------=

    Hello world!! 

    This tool is here to help you in receiving E-mails.
    N0 Logins, N0 Signups

    Just think your username@our_domains and use it anywhere, 
    and receive mails in your Terminal.
''')

def domains():
    print('''
    =--[DOMAIN]------------------------------------------------=

    => Domains you can use : 
        - 1secmail.com
        - 1secmail.org
        - 1secmail.net
        - wwjmp.com
        - esiix.com
        - xojxe.com
        - yoggm.com
        - oosln.com
        - vddaz.com
''')

def notice():
    print('''
    =--[NOTICE]------------------------------------------------=

    [ Points to Remember ]

    => E-mails will be vanished within hour automatically
    => DON't use these usernames : 
        * abuse@domain
        * webmaster@domain
        * contact@domain
        * postmaster@domain
        * hostmaster@domain
        * admin@domain
    
    => YOU'RE SOLELY RESPONSIBLE FOR EVERY ACTIONS.
    => WE DO NOT TAKE ANY RESPONSIBILITY REGARDING THE USE OF 
       THIS R-MAIL.
''')

def showHelpMenu():
    welcome()
    domains()
    notice()
    print('''
    =-------------------------------------------------------=
                       !! ENJOY YOUR DAY !!                                  
    =-------------------------------------------------------=
    ''')

def wait(t):
    print()
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("\t"+timer, end="\r")
        time.sleep(1)
        t -= 1

def updateSettings():
    username = input("\tEnter username : ")
    if len(username)<1:
        print("\n\tPlease give a user name")
        updateSettings()
    while True:
        domain = input("\tEnter domain : ")
        if(domain in domainList):
            print("\n\tThis will check for new mails every few secs.")
            c = input("\n\tRun in background to receive mails live : [y/n] : ")

            if(c=="Y" or c=="y"):
                runbg = True
                recheck = int(input("\n\tEnter time intervel (in secs.) : ")) 
            else:
                recheck = 0
                runbg = False

            d = input("\n\tAuto Download attachments if available [y/n] : ")
            if(d=="Y" or d=="y"):
                download = True
            else:
                download = False   

            e = input("\n\tCheck for updates [y/n] : ")
            if(e=="Y" or e=="y"):
                update = True
            else:
                update = False  
            f = input("\n\tUse these settings as master settings [y/n] : ")
            if(f=="Y" or f=="y"):
                autoLoadp = True
            else:
                autoLoadp = False  
            break            
        else:
            domains()
            updateSettings()
            
    prefDict = {
        "pref":{
            "username":username,
            "domain":domain,
            "runInBg":runbg,
            "rewoke":recheck,
            "downloadAttach":download,
            "checkUpdate":update,
            "autoLoadPref":autoLoadp,
        },
        "about":{
            "version":"1.1",
            "author":"annomroot",
            "lastUpdated":"",
            "publishedOn":"Dec-25-2021"
        }
    }

    print("\n\tYour Preferences : ")
    print('''
        Username : '''+prefDict["pref"]["username"]+'''
        Domain   : '''+prefDict["pref"]["domain"]+'''
        Run in background    : '''+str(prefDict["pref"]["runInBg"])+'''
        Check for new mails  : '''+str(prefDict["pref"]["rewoke"])+''' sec.
        Download Attachments : '''+str(prefDict["pref"]["downloadAttach"])+'''
        Check for updates    : '''+str(prefDict["pref"]["checkUpdate"])+'''
        Use as master Settings  : '''+str(prefDict["pref"]["autoLoadPref"])+'''s
    ''')
    endLine()
    conf = input("\tIs this Correct - [y/n] : ")
    if (conf =="y" or conf =="Y"):
        pref = json.dumps(prefDict, indent = 2)
        if os.path.isfile(prefFilePath):
            os.remove(prefFilePath)
        with open(prefFilePath, "w") as prefFile:
            prefFile.write(pref)
        print("\tSettings updated.")
        endLine()
        exit(0)
    else:
        updateSettings()

def loadSettings():
    with open(prefFilePath,'r') as prefFile:
        pref = json.load(prefFile)
        return pref

def downloadAttachments(rawMail,username,domain):
    fileNames = []
    action = "download"
    id = str(rawMail["id"])
    attachments = rawMail["attachments"]
    if(len(attachments) != 0):
        for attachment in attachments:
            fileNames.append(attachment["filename"])
        for filename in fileNames:
            downloadURL = apiBaseURL+'?action='+action+'&login='+username+'&domain='+domain+'&id='+id+'&file='+filename
            try:
                response = requests.get(downloadURL, allow_redirects=True)
                sCode = response.status_code
                if(sCode != 200):
                    print("Something not right... e.c z :",sCode)
                else:
                    if os.path.isfile(filename):
                        print("\n\t [ This file already downloaded. ] Skiping... ")
                    else:
                        open(str(filename), 'wb').write(response.content)
                        print("\n\t [ Attachment downloaded successfully ] ")
            except Exception as e:
                print(e)
    else:
        print("\tN0 Attachments found in mail id :",id)


def jsonPraser(data):
    da = json.loads(data)
    return da

def mailFormatter(rawMail):
    mId = rawMail["id"]
    mFrom = rawMail["from"]
    mSubject = rawMail["subject"]
    mDate = rawMail["date"]
    mAttachments = rawMail["attachments"] # this is in list format 
    mBody = rawMail["body"]
    mTextBody = rawMail["textBody"]
    mHtmlBody = rawMail["htmlBody"]
    print('''
        ID      : '''+str(mId)+'''
        From    : '''+mFrom+'''  
        Subject : '''+mSubject+'''
        Date    : '''+mDate+'''
        Attachments : '''+str(mAttachments)+'''
        Body : '''+html2text.html2text(mHtmlBody)+'''
    ''')

#read email by id
def getEmailById(username,domain,id):
    emailReadURL = apiBaseURL+'?action=readMessage'+'&'+'login='+username+'&'+'domain='+domain+'&'+'id='+id
    response = requests.get(emailReadURL, allow_redirects=True)
    statusCode = response.status_code
    if statusCode != 200:
        print("\n\t\tEncountered an Error with err code : ",statusCode)    
    else:
        content = response.content
        data = jsonPraser(content)
    return data
                                                                                                                                                                                                                                            #Author : @annomroot

#get list of emails
def getEmails(username, domain, download):
    print("\t    Checking for mails...")
    global emailData
    emailData = []
    action = "getMessages"
    emailListURL = apiBaseURL+'?action='+action+'&'+'login='+username+'&'+'domain='+domain
    response = requests.get(emailListURL, allow_redirects=True)
    statusCode = response.status_code
    if statusCode != 200:
        print("\tEncountered an Error with err code : ",statusCode)    
    else:
        content = response.content
        emails = jsonPraser(content)
        if len(emails) != 0:
            print("\t\t"+str(len(emails)),"Mails found...")
            for email in emails:
                id = str(email["id"])
                rawData = getEmailById(username,domain,id)
                mailFormatter(rawData)
                emailData.append(rawData)
            #for downloading attachments
            if(download):
                for mail in emailData:
                    downloadAttachments(mail,username,domain)
        else:
            print("\n\tNo New Mails.")

def operate(loadPrefs):
    username = input("\tUsername : ")
    if username == "help":
        showHelpMenu()
        operate(loadPrefs)
    elif username == "pref":
        heading("Update Pref")
        updateSettings()
    elif username == "notice":
        notice()
        endLine()
        operate(loadPrefs)
    elif len(username)<1:
        print("\n\tPlease give a username")
        endLine()
        operate(loadPrefs)
    else:
        domain = input("\tDomain : ")
        if(len(domain)<1):
            print("\n\tPlease give a domain\n\ttype help in domain field to list all the domains.")
            endLine()
            operate(loadPrefs)
        else:
            if (domain in domainList):
                print("\n\tYour Email :",username+"@"+domain)
                endLine()
                if (loadPrefs):    
                    pref = loadSettings()
                    download = pref["pref"]["downloadAttach"]
                    rewoke = pref["pref"]["rewoke"]
                    runBg = pref["pref"]["runInBg"]
                    if(runBg):
                        while True:
                            getEmails(username,domain,download)
                            endLine()
                            print("\n\tRechecking for mails in...")
                            wait(rewoke)
                    else:
                        getEmails(username,domain,download)
                else:
                    download = False
                    d = input("\tDownload attachments if available [y/n] : ")
                    if(d=="Y" or d=="y"):
                        download = True
                    else:
                        download = False
                    print("\n\tThis will check for new mails every few secs.")
                    c = input("\n\tRun in background to receive mails live : [y/n] : ")
                    if(c=="Y" or c=="y"):
                        rewoke = int(input("\n\tEnter time intervel (in secs.) : "))
                        while True:
                            getEmails(username,domain,download)
                            endLine()
                            print("\n\tRechecking for mails in...")
                            wait(rewoke)
                    else:
                        getEmails(username,domain,download)
            else:
                print("\n\tYou can't use "+domain+" as domain...")
                domains()
                endLine()
                operate(loadPrefs)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",nargs="?",default="default")
    parser.add_argument("-d",nargs="?",default="default")
    parser.add_argument("pref",nargs="?",default="default")
    value = parser.parse_args()

    if(value.pref=="pref"):
        banner()
        heading("Update Pref")
        updateSettings()
    if (value.u == "default"):
        banner()
        if os.path.isfile(prefFilePath):
            print("\tRunning with saved prefs...")
            spref = loadSettings()
            loadPrefs = spref["pref"]["autoLoadPref"]
            username = spref["pref"]["username"]
            domain = spref["pref"]["domain"]
            download = spref["pref"]["downloadAttach"]
            rewoke = spref["pref"]["rewoke"]
            runBg = spref["pref"]["runInBg"]
            if(loadPrefs):
                print("\n\tYour Email :",username+"@"+domain)
                endLine()
                if(runBg):
                    while True:
                        getEmails(username,domain,download)
                        endLine()
                        print("\n\tRechecking for mails in...")
                        wait(rewoke)
                else:
                    getEmails(username,domain,download)
                    endLine()
            else:
                print("\tMaster Setting is OFF")
                endLine()
                loadPrefs = False
                operate(loadPrefs)   
        else:
            loadPrefs = False
            heading("Welcome")
            operate(loadPrefs)
    else:
        banner()
        if(value.d == "default"):
            print("\tYou forgot to give domain")
            endLine()
            exit(0)
        if(value.d in domainList):
            if os.path.isfile(prefFilePath):
                spref = loadSettings()
                loadPrefs = spref["pref"]["autoLoadPref"]
                print("\tRunning with saved prefs...")
                username = value.u
                domain = value.d
                download = spref["pref"]["downloadAttach"]
                rewoke = spref["pref"]["rewoke"]
                runBg = spref["pref"]["runInBg"]
                print("\n\tYour Email :",username+"@"+domain)
                endLine()
                if (loadPrefs):    
                    if(runBg):
                        while True:
                            getEmails(username,domain,download)
                            endLine()
                            print("\n\tRechecking for mails in...")
                            wait(rewoke)
                    else:
                        getEmails(username,domain,download)
                else:
                    download = False
                    print("\tIf you don't want to do this every time,\n\tgo in the settings and turn On use as master setting.")
                    endLine()
                    d = input("\n\tDownload attachments if available [y/n] : ")
                    if(d=="Y" or d=="y"):
                        download = True
                    else:
                        download = False
                    print("\n\tThis will check for new mails every few secs.")
                    c = input("\n\tRun in background to receive mails live : [y/n] : ")
                    if(c=="Y" or c=="y"):
                        rewoke = int(input("\n\tEnter time intervel (in secs.) : "))
                        while True:
                            getEmails(username,domain,download)
                            endLine()
                            print("\n\tRechecking for mails in...")
                            wait(rewoke)
                    else:
                        getEmails(username,domain,download)
                    if(runBg):
                        while True:
                            getEmails(username,domain,download)
                            endLine()
                            print("\n\tRechecking for mails in...")
                            wait(rewoke)
                    else:
                        getEmails(username,domain,download)
                        endLine()
            else    :
                print("\n\tUpdate settings to do this, to Update settings\n\trun - `rmail.py pref`")
                endLine()
        else:
            print("\tThis domain is not valid.")
            domains()
