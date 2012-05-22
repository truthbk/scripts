import imaplib
import datetime

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
