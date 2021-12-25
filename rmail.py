import requests
import json
import time
import os.path
from bs4 import BeautifulSoup

apiBaseURL = "https://www.1secmail.com/api/v1/"
domainList = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net",
    "wwjmp.com",
    "esiix.com",
    "xojxe.com",
    "yoggm.com"
]

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

def welcome():
    print('''
    =--[WELCOME]-----------------------------------------------=

    Hello world!! 

    This tool is here to help you in recieving E-mails.
    N0 Logins, N0 Signups

    Just think your username@our_domains and use it anywhere, 
    and recieve mails in your Terminal.
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
                    print("Something not right... e.c:",sCode)
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
    dat = data.decode('utf8').replace("'", '"')
    da = json.loads(dat)
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
    soup = BeautifulSoup(mBody,features="html5lib")
    print('''
        ID      : '''+str(mId)+'''
        From    : '''+mFrom+'''  
        Subject : '''+mSubject+'''
        Date    : '''+mDate+'''
        Attachments : '''+str(mAttachments)+'''
        Body : '''+soup.get_text()+'''
    ''')

#read email by id
def getEmailById(username,domain,id):
    emailReadURL = apiBaseURL+'?action=readMessage'+'&'+'login='+username+'&'+'domain='+domain+'&'+'id='+id
    response = requests.get(emailReadURL, allow_redirects=True)
    statusCode = response.status_code
    if statusCode != 200:
        print("\n\t\tEncountered an Error with err code :",statusCode)    
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
        print("\tEncountered an Error with err code :",statusCode)    
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

def operate():
    username = input("\tUsername : ")
    domain = input("\tDomain : ")
    if username == "help":
        showHelpMenu()
        operate()
    elif username == "notice":
        notice()
        endLine()
        operate()
    elif len(username)<1:
        print("\n\tPlease give a username")
        endLine()
        operate()
    elif domain == "h" or len(domain)<1:
        domains()
        endLine()
        operate()
    else:
        if( len(username)<1 or len(domain)<1 ):
            print("\n\tPlease give a username and domain")
            operate()
        else:
            if (domain in domainList):
                download = False
                d = input("\tDownload attachments if available [y/n] : ")
                if(d=="Y" or d=="y"):
                    download = True
                else:
                    download = False
                print("\n\tThis will check for new mails every few secs.")
                c = input("\n\tRun in background to recieve mails live : [y/n] : ")
                if(c=="Y" or c=="y"):
                    rewoke = int(input("\n\tEnter time interver (in secs.) :"))
                    while True:
                        getEmails(username,domain,download)
                        print("\n\twating for "+str(rewoke)+" seconds...")
                        time.sleep(rewoke)
                else:
                    getEmails(username,domain,download)
            else:
                print("\n\tYou can't use "+domain+" as domain...")
                domains()
                endLine()
                operate()

if __name__=="__main__":
    banner()
    print("\ttype help for help menu\n")
    operate()
    