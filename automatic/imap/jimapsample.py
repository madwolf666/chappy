import imapclient
from backports import ssl
import pyzmail

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#imap_obj = imapclient.IMAPClient('imap.gmail.com', ssl=True, ssl_context=context)
#imap_obj.login('madwolf699@gmail.com', 'chappy666')

imap_obj = imapclient.IMAPClient('imap.mail.yahoo.co.jp', ssl=True, ssl_context=context)
imap_obj.login('madwolf666@yahoo.ne.jp', 'chappy666')

#imap_obj = imapclient.IMAPClient('imap.outlook.com', ssl=True, ssl_context=context)
#imap_obj.login('madwolf666@live.jp', 'harry666')

imap_obj.select_folder('INBOX', readonly=True)

UIDs = imap_obj.search('(SINCE 01-Apr-2000)')

print(UIDs)
#print(len(UIDs))
#raw_messages = imap_obj.fetch(UIDs[0], ['BODY[]', 'FLAGS'])
for a_idx in range(len(UIDs)):
    raw_messages = imap_obj.fetch(UIDs[a_idx], ['BODY[]', 'FLAGS'])
    print('****** {uid} ******'.format(uid=UIDs[a_idx]))
    message = pyzmail.PyzMessage.factory(raw_messages[UIDs[a_idx]][b'BODY[]'])
    print(message.get_subject())
    print(message.get_addresses('from'))
    print(message.get_addresses('to'))
    print(message.get_addresses('cc'))
    print(message.get_addresses('bcc'))
    if (message.text_part != None):
        print(message.text_part.get_payload().decode(message.text_part.charset))
    if (message.html_part != None):
        print(message.html_part.get_payload().decode(message.html_part.charset))

imap_obj.logout()

