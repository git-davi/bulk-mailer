import sys
import database as db
import smtplib
from filer import *
from email.mime.text import MIMEText
from multiprocessing.dummy import Pool as ThreadPool
import numpy as np
import time

N_THREADS = 4
DB_BUFFER = 5


def _login(username, password):
	try:
		print('loggin to mail server...')
		server = smtplib.SMTP(getmailserver())
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, password)
		print('connection established')

	except Exception as ex:
		print('failed to connect')
		print('Exception :', ex)
		sys.exit(2)

	return server


def mail_creator(fromaddr, subject, content):

	mail = MIMEText(content, 'html')
	mail['Subject'] = subject
	mail['From'] = fromaddr

	return mail


def change_dest(mail, toaddr):
	mail['To'] = toaddr
	return


def send_mail(server, fromaddr, toaddr, mail):
	try:
		server.ehlo()
		server.sendmail(fromaddr, toaddr, mail.as_string())
	except Exception as ex:
		print('Error occurred while sending ' + toaddr + '\'s mail')
		print('Exception :', ex)
		return 0
	return 1


def _update_iscritti(mail_list):
	db.updatesubs(mail_list)
	return


def _add_receiver(sent, mail):
	sent.append((mail,))
	return


def thread_mail_to_list(username, password, subject, content , mail_list):
	# la lista è un array numpy
	# questa funzione è eseguita in un thread

	server = _login(username, password)

	mail = mail_creator(username, subject, content)
	buffer = list()

	try:
		for toaddr in mail_list:

			if len(buffer) == DB_BUFFER:
				print('Updating db')
				_update_iscritti(buffer)
				print('Db updated')
				del buffer[:]

			change_dest(mail, toaddr)
			print('Sending to : ', toaddr, '...')
			if send_mail(server, username, toaddr, mail):
				print("Sent.")
				_add_receiver(buffer, toaddr)

	except Exception as ex:
		print('Exception occurred :', ex)
	finally:
		# if buffer size hasn't reached or some error occurred
		print('Updating db')
		_update_iscritti(buffer)
		print('Db updated')

		server.quit()
	return


def mailer(username, password, subject, filecont):

	content = contenuto(filecont)

	iscritti = db.getiscritti()

	def pool_wrapper(mail_list):
		thread_mail_to_list(username, password, subject, content, mail_list)
		return

	# liste mail è del tipo narray
	liste_mail = np.array_split(iscritti, N_THREADS)

	print('creating threads and starting emailing')
	start_time = time.time()

	pool = ThreadPool(N_THREADS)

	try:
		pool.map(pool_wrapper, liste_mail)

	except Exception as ex:
		print(ex)

	pool.close()
	pool.join()

	# db.checkend(username, password, subject, filecont)
	print('\n\n\n------------------- mails sent !!------------------------')
	print('time elapsed in seconds : ', round(time.time() - start_time, 6), '\n\n\n')
