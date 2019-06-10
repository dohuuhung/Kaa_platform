import configparser
import smtplib

from email.mime.text import MIMEText

CONFIG_FILE_PATH = '/etc/kaa/kaa_dashboard_webservice.conf'

EMAIL_INFOR = {'mail_server_address': '10.0.0.1',
               'port': '465',
               'sender_address': 'dohuuhung1234@gmail.com',
               'sender_password': 'MrJohan#))$96',
               'subject': 'KAA REGISTRY',
               'default_msg': 'This is an email from Kaa system. Contact us for more details.',
               'timeout': '10'}

MESSAGE_SAMPLE = {'send_temporary_pass': 'Hello,\n\nAn account has been created for'
                                         ' you on Kaa with the following details:\n\n'
                                         'Username: %s\nPassword (temporary): %s\n'
                                         'This is an automatically generated email.'
                                         'Please do not reply to this message.'}

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

class SendEmail:
    def __init__(self):
        self.email_infor = get_mail_info(config)

    def send_mail(self, msg, receiver_address, cc_address=[]):
        # receiver_address is a list
        # cc_address is a list
        try:
            message = None
            sender = self.email_infor['sender_address']
            if msg:
                message = MIMEText(msg)
            else:
                message = MIMEText(self.email_infor['default_msg'])
            message['Subject'] = self.email_infor['subject']
            message['From'] = sender
            message['To'] = ', '.join(receiver_address)
            message['Cc'] = cc_address
            if cc_address:
                receiver_address += cc_address
            server = smtplib.SMTP_SSL('{}:{}'.format(self.email_infor['mail_server_address'],
                                                     self.email_infor['port']),
                                      timeout=float(self.email_infor['timeout']))
            server.login(sender, self.email_infor['sender_password'])
            server.sendmail(sender, receiver_address, message.as_string())
            server.quit()
            return 0
        except Exception as e:
            return str(e.args[-1]).replace(' ', '_').replace('\n', '')

    def send_temporary_pass(self, username, temp_pass, receiver_email):
        # receiver_email is a string
        receiver_email = [receiver_email]
        msg = MESSAGE_SAMPLE['send_temporary_pass'] % (username, temp_pass)
        return self.send_mail(msg, receiver_email)

def get_mail_info(config_object):
    email_infor = {}
    for i in EMAIL_INFOR:
        try:
            if config_object['email'][i]:
                email_infor[i] = config_object['email'][i]
            else:
                email_infor[i] = EMAIL_INFOR[i]
        except:
            email_infor[i] = EMAIL_INFOR[i]
    return email_infor