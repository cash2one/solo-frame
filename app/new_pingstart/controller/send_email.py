# coding=utf-8
import _env  # noqa
from email import encoders
from email.mime.base import MIMEBase
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(data):
    '''
    send email to every publisher about AD
    '''
    reason = True
    email_server = data.get('email_server')
    email_server_port = data.get('email_server_port')
    username = data.get('username')
    password = data.get('password')
    sender = data.get('sender')
    receiver = data.get('receiver')
    content = data.get('msg')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = content.get('subject')
    msg['From'] = sender
    msg['To'] = receiver

    if content.get('text'):
        text = MIMEText(content.get('text'), 'plain', 'utf-8')
        msg.attach(text)
    if content.get('html'):
        html = MIMEText(content.get('html'), 'html', 'utf-8')
        msg.attach(html)
    if content.get('attachment'):
        mime = MIMEBase('application', 'octet-stream', filename=content.get('attachment_name'))
        mime.add_header('Content-Disposition', 'attachment', filename=content.get('attachment_name'))
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(content.get('attachment').decode('base64'))
        encoders.encode_base64(mime)
        msg.attach(mime)

    try:
        # Create the body of the message (a plain-text and an HTML version).
        smtp = smtplib.SMTP()
        smtp.connect(email_server, int(email_server_port))
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

    except smtplib.SMTPAuthenticationError as e:
        reason = u'send email failure, error={}'.format(e)
    except smtplib.SMTPRecipientsRefused as e:
        reason = u'receiver refused, error={}'.format(e)
    except smtplib.SMTPSenderRefused as e:
        reason = u'sender refused, error={}'.format(e)
    except Exception as e:
        reason = u'unknown reason, error={}'.format(e)
    finally:
        return reason
