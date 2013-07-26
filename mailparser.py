import imaplib, email 

user = 'some_user'
passwd = 'some_pw'

def mailHandler(user, passwd, send_to, send_spam):
    server = 'imap.mail.yahoo.com'
    imap = imaplib.IMAP4_SSL(server)
    successful = imap.login(user, passwd)
    if not successful:
        # write sth to log file
        print 'this is bad'

    imap.select() # gets the inbox
    typ, data = imap.search(None, '(UNSEEN)')

    for num in data[0].split():
        #########################################################
        ################ Fetch yahoo mail #######################
        #########################################################
        typ, data = imap.fetch(num, '(RFC822)')
        mail = email.message_from_string(data[0][1])

        text = ''
        html = ''
        attachments = []
        for part in mail.walk():
            print part.get_content_type()
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
                    attachments.append(file_name)
                    open(part.get_filename(), 'wb').write(part.get_payload(decode=True))

        print mail['From']
        print mail['Subject']
        print mail['Date']
        #print text
        print attachments
        print '------------------------------------------------'
        #########################################################
        ################## Mail sender ##########################
        #########################################################

    imap.close()
    imap.logout()

mailHandler(user, passwd, 'me', False)
