import smtplib,email
from email.mime.text import MIMEText


CLIENT_NOT_LOGIN_ERROR="The client didn't login,please login it"
RECEIVERS_IS_AN_EMPTY_LIST="The receivers is an empty list,can't send the E-mail"
VALUE_TYPE_WRONG="The values type is wrong"

class SMTPClient(object):
    '''
    SMTP Email Client
    '''
    def __init__(self,host="localhost",port=25):
        self.mail=None
        self.smtpObj=smtplib.SMTP(host=host,port=port)
        self.smtpObj.connect(host,port)
    def login(self,mail,password=""):
        self.mail=mail
        self.smtpObj.login(user=mail,password=password)

def sendPlain(client:SMTPClient,
              receivers,
              text="",
              subject="",
              sender_name=None,
              receivers_name=None,
              encoding="utf-8"
              ):
    '''
    Send Plain Email
    :param client:EMAIL CLIENT(SMTPClient)
    :param receivers:the Receivers(str or list or tuple or frozenset)
    :param text:Email HTML Body
    :param subject:Email Subject
    :param sender_name:Email Sender's Name(From,Default value is sender Email Address)
    :param receivers_name:Email Receivers' Name(To,Default value is 1st Receivers)
    :param encoding:Text,Subject,sender_name,receivers_name 's encoding,default is 'utf-8'
    :return:Hasn't return
    '''
    if sender_name == None:
        if client.mail == None:
            raise ValueError(CLIENT_NOT_LOGIN_ERROR)
        else:
            sender_name=client.mail
    if receivers_name == None:
        if len(receivers) < 1:
            raise ValueError(RECEIVERS_IS_AN_EMPTY_LIST)
        else:
            if isinstance(receivers,str):
                receivers_name=receivers
                receivers=[receivers]

            else:
                receivers_name = receivers[0]
    if isinstance(receivers, (set, tuple, frozenset)):
        receivers = list(receivers)
    if not (isinstance(client,SMTPClient) or
            isinstance(receivers_name,str) or
            isinstance(receivers,list) or
            isinstance(text,str) or
            isinstance(subject,str) or
            isinstance(sender_name,str) or
            isinstance(receivers_name,str) or
            isinstance(encoding,str)):
        raise ValueError(VALUE_TYPE_WRONG)

    msg=MIMEText(text,'plain',encoding)
    msg["From"]=email.header.Header(sender_name,encoding)
    msg["To"]=email.header.Header(receivers_name,encoding)
    msg["Subject"]=email.header.Header(subject,encoding)
    client.smtpObj.sendmail(client.mail,receivers,msg.as_string())
    return True

def sendHTML(client:SMTPClient,
              receivers,
              text="",
              subject="",
              sender_name=None,
              receivers_name=None,
              encoding="utf-8"
              ):
    '''
    Send Plain Email
    :param client:EMAIL CLIENT(SMTPClient)
    :param receivers:the Receivers(str or list or tuple or frozenset)
    :param text:Email Body
    :param subject:Email Subject
    :param sender_name:Email Sender's Name(From,Default value is sender Email Address)
    :param receivers_name:Email Receivers' Name(To,Default value is 1st Receivers)
    :param encoding:Text,Subject,sender_name,receivers_name 's encoding,default is 'utf-8'
    :return:Hasn't return
    '''
    if sender_name == None:
        if client.mail == None:
            raise ValueError(CLIENT_NOT_LOGIN_ERROR)
        else:
            sender_name=client.mail
    if receivers_name == None:
        if len(receivers) < 1:
            raise ValueError(RECEIVERS_IS_AN_EMPTY_LIST)
        else:
            if isinstance(receivers,str):
                receivers_name=receivers
                receivers=[receivers]

            else:
                receivers_name = receivers[0]
    if isinstance(receivers, (set, tuple, frozenset)):
        receivers = list(receivers)
    if not (isinstance(client,SMTPClient) or
            isinstance(receivers_name,str) or
            isinstance(receivers,list) or
            isinstance(text,str) or
            isinstance(subject,str) or
            isinstance(sender_name,str) or
            isinstance(receivers_name,str) or
            isinstance(encoding,str)):
        raise ValueError(VALUE_TYPE_WRONG)

    msg=MIMEText(text,'html',encoding)
    msg["From"]=email.header.Header(sender_name,encoding)
    msg["To"]=email.header.Header(receivers_name,encoding)
    msg["Subject"]=email.header.Header(subject,encoding)
    client.smtpObj.sendmail(client.mail,receivers,msg.as_string())
    return True
def sendAnyText(client:SMTPClient,
              receivers,
                typeof="plain",
              text="",
              subject="",
              sender_name=None,
              receivers_name=None,
              encoding="utf-8"
              ):
    '''
    Send Plain Email
    :param client:EMAIL CLIENT(SMTPClient)
    :param receivers:the Receivers(str or list or tuple or frozenset)
    :param typeof:Mail Body Type(default:plain)
    :param text:Email Body
    :param subject:Email Subject
    :param sender_name:Email Sender's Name(From,Default value is sender Email Address)
    :param receivers_name:Email Receivers' Name(To,Default value is 1st Receivers)
    :param encoding:Text,Subject,sender_name,receivers_name 's encoding,default is 'utf-8'
    :return:Hasn't return
    '''
    if sender_name == None:
        if client.mail == None:
            raise ValueError(CLIENT_NOT_LOGIN_ERROR)
        else:
            sender_name=client.mail
    if receivers_name == None:
        if len(receivers) < 1:
            raise ValueError(RECEIVERS_IS_AN_EMPTY_LIST)
        else:
            if isinstance(receivers,str):
                receivers_name=receivers
                receivers=[receivers]

            else:
                receivers_name = receivers[0]
    if isinstance(receivers, (set, tuple, frozenset)):
        receivers = list(receivers)
    if not (isinstance(client,SMTPClient) or
            isinstance(receivers_name,str) or
            isinstance(receivers,list) or
            isinstance(text,str) or
            isinstance(subject,str) or
            isinstance(sender_name,str) or
            isinstance(receivers_name,str) or
            isinstance(encoding,str)):
        raise ValueError(VALUE_TYPE_WRONG)

    msg=MIMEText(text,typeof,encoding)
    msg["From"]=email.header.Header(sender_name,encoding)
    msg["To"]=email.header.Header(receivers_name,encoding)
    msg["Subject"]=email.header.Header(subject,encoding)
    client.smtpObj.sendmail(client.mail,receivers,msg.as_string())
    return True

client=SMTPClient("smtp.126.com")
client.login("billy_0328@126.com","billy0328")
sendPlain(client,["billy_0328@126.com"],"老师您好","抱歉，作业没交","billy_0328@126.com","billy_0328@126.com","utf-8")