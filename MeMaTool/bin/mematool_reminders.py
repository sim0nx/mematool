#!/usr/bin/python

import smtplib
import string
import random
from email.mime.text import MIMEText

import sys
sys.path.append('/home/sim0n/MeMaTool/MeMaTool')


import ConfigParser
from mematool.model import Payment, Member
import pylons


from mematool.model.ldapModelFactory import LdapModelFactory
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_
from datetime import date, datetime



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for x in range(size))


def sendReminder(mail):
  body = '''Hi,

--- Automatic mail ... do not reply to this mail directly ! ---


This is a reminder for paying your syn2cat membership fee.
If you are sure you have already paid, please ignore this mail...
bank<->mematool synchronization is a manual task.
BTW, you can see the status of your received payments in mematool[0] or contact me[1]
if you wish.

Please consider setting up a standing order or paying at least on a 6month 
basis.
If possible also think about managing your payments autonomously so we don\'t 
have to bug you each time 

For those being late already a couple of months, I urge you to get in contact 
with me else we will have to consider your silence as a wish to leave the 
association.

As always....payment troubles are ok and we are understanding....just let us 
know.


Payment information:
- 1 year fee = 114euro
- Bank account:
    Holder:    syn2cat a.s.b.l.
    Bank:      BCEE
    IBAN:      LU93 0019 3255 6612 9000
    BIC/SWIFT: BCEELULL



cheerz.... see you and thanks for your continuing support



[0]:  https://mematool.hackerspace.lu:8443
[1]:  treasurer-payments@hackerspace.lu'''


  msg = MIMEText(body)

  from_ = 'syn2cat treasurer <' + id_generator(8) + '@hackerspace.lu>'
  to_ = mail
  msg['Subject'] = 'syn2cat membership fee'
  msg['From'] = from_
  msg['To'] = to_

  s = smtplib.SMTP('localhost')
  s.sendmail(from_, [to_], msg.as_string())
  s.quit()


def printOutstanding(member, date):
  d = date
  today = datetime.now().date()

  print member
  print d.year, today.year
  print d.month, today.month
  print today.day
  print

def getOutstanding(lmf):
  activeMembers = lmf.getActiveMemberList()
  members = {}

  for uid in activeMembers:
    last_payment = None

    try:
      last_payment = Session.query(Payment).filter(and_(Payment.uid == uid, Payment.verified == 1)).order_by(Payment.date.desc()).limit(1)[0]
    except:
      ''' Don't care if there is no payment '''
      pass


    m = lmf.getUser(uid)

    if last_payment:
      d = last_payment.date
      today = datetime.now().date()

      if d.year > today.year or (d.year == today.year and d.month >= today.month):
        pass
      elif d.year == today.year:
        if today.month - d.month == 1:
          if today.day == 28:
            members[m.uid] = [d, m.mail]
          else:
            pass
        else:
          if today.day % 7 == 0:
            members[m.uid] = [d, m.mail]
          else:
            pass
      else:
        if today.day % 7 == 0:
          members[m.uid] = [d, m.mail]
        else:
          pass

  return members


config_global = ConfigParser.RawConfigParser()
config_global.read('/home/sim0n/MeMaTool/MeMaTool/production.ini')
cnf = {}
cnf['mematool'] = {}
cnf['ldap.basedn_users'] = config_global.get('app:main', 'ldap.basedn_users')
cnf['ldap.basedn_groups'] = config_global.get('app:main', 'ldap.basedn_groups')
cnf['ldap.server'] = config_global.get('app:main', 'ldap.server')

db_url = config_global.get('app:main', 'sqlalchemy.url')
__all__ = ['Session']
db = sqlalchemy.create_engine(db_url)
connection = db.connect()
Session = sessionmaker(bind=db)()


lmf = LdapModelFactory(cnf)
members = getOutstanding(lmf)

for k, v in members.items():
  printOutstanding(k, v[0])
  sendReminder(v[1])
