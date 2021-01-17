from Message import *
from User import *

from time import sleep
import sys
import pickle, cgitb, codecs, datetime
import cgi
import os
import html





user=User()

form = cgi.FieldStorage()
action = form.getfirst("action", "")
sysmess=""

def LoadTpl(tplName):
    docrootname = 'PATH_TRANSLATED'
    with open(os.environ[docrootname]+'/tpl/'+tplName+'.tpl', 'rt') as f:
        return f.read().replace('{selfurl}', os.environ['SCRIPT_NAME'])
        
if action == "Init":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                SendMessage(s, 0, user.MyId, Messages.M_INIT)
                m=Receive(s)
                if (m.m_Header.m_Type==Messages.M_CONFIRM):
                    if (user.find):
                        user.register(m.m_Header.m_To)
                    sysmess="Succes Init"
                else:
                    sysmess="Something went wrong"
    
if action=="publish":
    m_To=form.getfirst("m_To", "")
    m_To=html.escape(m_To)
    m_Data = form.getfirst("m_Data", "")
    m_Data = html.escape(m_Data)
    if m_Data is not None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                SendMessage(s, int(m_To), int(user.MyId), Messages.M_TEXT, m_Data)
                if Receive(s).m_Header.m_Type==Messages.M_CONFIRM:
                    user.AddMessage(m_To, user.MyId, m_Data)
                    sysmess="Succes"
                else:
                    sysmess="Something went wrong"
        except:
            sysmess="Something went wrong, try to Init again"


if action=="getdata":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            SendMessage(s, 0, user.MyId, Messages.M_GETDATA)
            m=Receive(s)
            if (m.m_Header.m_Type==Messages.M_TEXT):
                user.AddMessage(m.m_Header.m_To, m.m_Header.m_From, m.m_Data.decode('utf-8'))
    except: 
        sysmess="Something went wrong, try to Init again"


if action=="delete":
    user.deleteUSerData()


deleteForm='''
<form action="/cgi-bin/Chat.py">
        <input type="hidden" name="action" value="delete">
        <input type="submit" value="Delete my history">
    </form>    
'''

if user.MyId != 0:
    pub = '''
    <form method="post" action="/cgi-bin/Chat.py">
        <input type="text" name="m_To">
        <textarea name="m_Data"></textarea>
        <input type="hidden" name="action" value="publish">
        <input type="submit" value="Send">
    </form>
    '''
    getdt='''
    <form method="get" action="/cgi-bin/Chat.py">
        <input type="hidden" name="action" value="getdata"> 
        <input type="submit" value="Get Data">
    </form>    
    '''
else:
    pub = ''
    getdt=''


print('Content-type: text/html\n')

if user.MyId != 0:
    print('Active User:', user.MyId, '<br>')
else: 
    print('Press Init For Init to Server', '<br>')
    
print(LoadTpl('index').format(posts=user.MessList(), publish=pub, getdata=getdt, delete=deleteForm))
print(sysmess)