import smtplib
from email.mime.text import MIMEText
from email.header import Header

# SMTPメール送信
def Mail_Send(h_auth, h_msg):
    """
    :param h_auth:  以下の形式 
        h_auth = {
            "IS_SSL":True,
            "SMTP":"",
            "SMTP_SSL":"smtp.gmail.com",
            "PORT":465,
            "LOGIN_MAIL":"madwolf699@gmail.com",
            "LOGIN_PASS":"chappy666",
        }
    :param h_msg:   以下の形式
        h_msg = {
            "SUBJECT":"Today\'s Tweet Search",
            "FROM":"madwolf699@gmail.com",
            "TO":"madwolf666@live.jp",
            "BODY":a_result
        }
    :return:        なし
    """
    #JP='iso-2022-jp'

    a_encoding = 'utf-8'
    message=MIMEText(
        h_msg["BODY"],
        'plain',
        a_encoding,
    )

    message['Subject'] = str(Header(h_msg["SUBJECT"], a_encoding))
    message['From'] = h_msg["FROM"]
    message['To'] = h_msg["TO"]

    if(h_auth["IS_SSL"]==True):
        gm = smtplib.SMTP_SSL(h_auth["SMTP_SSL"], h_auth["PORT"])
    else:
        gm = smtplib.SMTP_SSL(h_auth["SMTP"], h_auth["PORT"])

    gm.login(h_auth["LOGIN_MAIL"],h_auth["LOGIN_PASS"])
    gm.sendmail(h_msg["FROM"], h_msg["TO"], message.as_string())
    gm.close()
