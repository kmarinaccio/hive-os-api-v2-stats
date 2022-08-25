import os
import imaplib
import email
from email.header import decode_header
import traceback

USERNAME = "YOUR GMAIL"
PASSWORD = "####################" # App Password for GMAIL (setup for a Windows PC), Go to Security > App Passwords for more info. 2FA must be enabled first.

def get_otp():
    try:
        otp = []
        # create an IMAP4 class with SSL
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        imap.login(USERNAME, PASSWORD)

        status, messages = imap.select("Inbox")
        # number of top emails to fetch
        N = 1
        # total number of emails
        messages = int(messages[0])

        for i in range(messages, messages - N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments

                                # depending on your where your OTP is in the email, you will have to modify the string split method
                                body = body.split('Copy the code below and paste it into the corresponding form to continue.')[1]
                                body = body.split('This code is valid for 5 minutes')[0]
                                otp.append(int(body))
        return otp

    except Exception as ex:
        print("ERROR: THIS DIDN'T WORK!")
        print(ex.args[0])
        return ""
    