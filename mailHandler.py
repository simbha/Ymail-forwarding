import imaplib, email, os, sys
from google.appengine.api import mail
sys.path.append('./models')
import models

class MailHandler():
    def imapDate(date):
        # converts google date format to imap date format
        months = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May',
                '06':'June', '07':'July', '08':'Aug', '09':'Sept', '10':'Oct',
                '11':'Nov', '12':'Dec' }
        date = date.split('-')
        return date[2] + '-' + months[date[1]]  + '-' + date[0]


    user = 'mihai_mv13@yahoo.com'
    passwd = '' ###########

    def mailHandler(user, passwd, send_to, send_spam, date):
        server = 'imap.mail.yahoo.com'
        imap = imaplib.IMAP4(server)
        successful = imap.login(user, passwd)

        if not successful:
            # write sth to log file
            mail.send_mail( sender = 'ymailforwarding@gmail.com', # fake email
                    to = send_to,
                    subject = 'Y! Mail Forwarding Error',
                    body = ('''It seems like your email address (%s) could not 
                    be accesed, please update your credentials''') % user)
            return

        for folder in ['Inbox', 'Bulk Mail']:
            if folder == 'Inbox' or (folder == 'Bulk Mail' and send_spam):
                imap.select(folder)
            else:
                # no spam this time
                break;

            typ, data = imap.search(None, '(ALL SINCE "%s")' % imapDate(date)) 
            for num in data[0].split():
                #########################################################
                ################ Fetch yahoo email #######################
                #########################################################
                typ, data = imap.fetch(num, '(RFC822)')
                mail_ = email.message_from_string(data[0][1])

                text = ''
                html = ''
                attachments = []
                for part in mail_.walk():
                    if part.get_content_type() == 'text/plain':
                        # if the attachment contains a .txt file, it is labeled as
                        # text/plain so a file check is necessary
                        if not part.get_filename(None):
                            text += part.get_payload(decode=True)
                            continue
                    if part.get_content_type() == 'text/html':
                        html += part.get_payload(decode=True)
                        continue
                    if part.get_content_type().split('/')[0] is not 'multipart':
                        file_name =  part.get_filename(None)
                        if file_name:
                            attachments.append((file_name, part.get_payload(decode=True)))
                            #open(part.get_filename(), 'wb').write(part.get_payload(decode=True))

                print mail_['From']
                #print email['Subject']
                #print email['Date']
                #print text
                #print attachments
                #print '------------------------------------------------'
                #########################################################
                ################## Mail sender ##########################
                #########################################################

                mail.send_mail( sender = mail_['From'],
                        to = send_to,
                        subject = ('From: %s | ' + mail_['Subject']) %user,
                        body = text,
                        html = html,
                        attachments = attachments)

        imap.close()
        imap.logout()

    mailHandler(user, passwd, 'mihai.mv13@gmail.com', False, '2013-06-19')

