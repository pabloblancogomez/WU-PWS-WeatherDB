#!/usr/bin/env python
# encoding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
import getweather
from getweather import resuls

_NIVEL = getweather.resuls([0])
_temp_dewpt = getweather.resuls([1])
_humedad = getweather.resuls([2])


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails
def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
print(_NIVEL)
names, emails = get_contacts('mycontacts.txt')  # read contacts
message_template = read_template('message.txt')

for name, email in zip(names, emails):
	message = message_template.substitute(PERSON_NAME=name.title(), NIVEL=_NIVEL, temp_dewpt=_temp_dewpt, humedad=_humedad)
	print(message)
	#The mail addresses and password
	sender_address = 'pableras84@hotmail.com'
	sender_pass = 'Ra2013bL'
	receiver_address = email
	#Setup the MIME
	msg = MIMEMultipart()
	msg['From'] = sender_address
	msg['To'] = receiver_address
	#sub_temp_str = 'Alerta roja de precipitación'
	#sub_temp_obj = Template(sub_temp_str)
	#asunto = sub_temp_obj.substitute(NIVEL='John Doe') 
	#asunto = 'Alerta roja de precipitación'
	msg['Subject'] = 'Alerta de precipitación'   #The subject line
	#The body and the attachments for the mail
	msg.attach(MIMEText(message, 'plain'))
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.live.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = msg.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent')


