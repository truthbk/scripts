#!/usr/bin/python

import imaplib
import datetime

import getopt
import sys

class IMAPQuery:

    def from(self, email):
        query = '(FROM "{email}")'.format(email=email)
        return query

    def bcc(self, email):
        query = '(BCC "{email}")'.format(email=email)
        return query

    def cc(self, email):
        query = '(CC "{email}")'.format(email=email)
        return query

    def subject(self, subject):
        query = '(HEADER Subject "{subject}")'.format(subject=subject)
        return query

    def afterDate(self, year, month, day):
        date = datetime.date(year, month, date).strftime("%d-%b-%Y")
        query = '(SENTSINCE {date})'.format(date=date)
        return query

    def beforeDate(self, year, month, day):
        date = datetime.date(year, month, date).strftime("%d-%b-%Y")
        query = '(BEFORE {date})'.format(date=date)
        return query

    #applies to single queries...
    def not(self, query):
        q = query[1:]
        return "(NOT " + q

    def union(self, queries):
        qlist = []
        for query in queries:
             q = query[1:]
             q = q[:-1]
             qlist.append(q)

        query ="(" + ' '.join(qlist) + ")"
        return query


class MailSession:
    mail = None
    servername = None
    username = None
    password = None

    def __init__(self, user, passwd, server="imap.gmail.com"):
        self.servername = server
        self.username = user
        self.password = passwd

    def login(self):
        self.mail = imaplib.IMAP4_SSL(self.servername)
        self.mail.login(self.username, self.password)

    def logout(self):
        self.mail.logout()

    def folders(self):
        self.mail.list()

    def chgfolder(self, folder="inbox"):
        self.mail.select(folder)

    def search(self, query="ALL"):
        return self.mail.uid('search', None, query);

    def delete(self, messages);
        for uid in messages[0].split():
            self.mail.store(uid, '+FLAGS', '\\Deleted')
        self.mail.expunge()


def main(argv):

    user = None
    passwd = None
    server = None
    folder = None
    cmd = None
    cmd_args = None

    valid_cmds = [];
    valid_cmds.append("LIST");
    valid_cmds.append("READ");
    valid_cmds.append("DELETE");

    try:
        opts, args = getopt.getopt(
                argv, 
                "hu:p:s:f:c:a:", 
                ["help", "username=","password=","server=","folder=","command=","args="])
    except getopt.GetoptError:
        usage()
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            exit(2)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            passwd = arg
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-f", "--folder"):
            folder = arg
        elif opt in ("-c", "--command"):
            cmd = arg
            if cmd not in valid_cmds:
                usage()
                exit(1)
        elif opt in ("-a", "--args"):
            cmd_args = arg

    mail = MailSession(user, passwd, server)
    mail.login()
    if folder is None:
        print "you must specify a folder to act on"
        mail.folders()
        mail.logout()
        exit(0)



if __name__ == "__main__":
    main(sys.argv[1:])
