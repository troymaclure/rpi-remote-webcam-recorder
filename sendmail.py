import smtplib
import pendulum
import json
import fire


class Mail(object):
	
	def __init__(self):
		with open('config.json') as f:
			data = json.load(f)
			self.address = data["mailaddress"]
			self.passwd = data["mailpassword"]
		self.subject = ''
		self.message = ''
		self.body = ''
	
	def __send__(self):
		self.body = '\r\n'.join(
			['To: %s' % self.address, 'From: %s' % self.address, 'Subject: %s' % self.subject, '', self.message])
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(self.address, self.passwd)
		try:
			server.sendmail(self.address, self.address, self.body)
			print('email sent')
		except:
			print('error sending mail')
		server.quit()

	def webcamstarted(self):
		now = pendulum.now('Europe/Brussels')
		date = now.ctime()
		self.subject = 'Webcam-Google-Recorder Started.'
		self.message = 'Webcam-Google-Recorder Started at ' + date
		self.__send__()
		
	def webcamerror(self):
		now = pendulum.now('Europe/Brussels')
		date = now.ctime()
		self.subject = 'Webcam-Google-Recorder Error.'
		self.message = 'Webcam-Google-Recorder Error at ' + date
		self.__send__()

	def videouplaoded(self, filename):
		now = pendulum.now('Europe/Brussels')
		date = now.ctime()
		self.subject = 'Video ' + filename + ' uploaded.'
		self.message = 'Record ' + filename + ' uploaded at ' + date
		self.__send__()
		
	def uploadfailled(self, filename):
		now = pendulum.now('Europe/Brussels')
		date = now.ctime()
		self.subject = filename + ' upload failed.'
		self.message = filename + ' upload failed at ' + date
		self.__send__()
		
	


#m = Mail()
#m.webcamstarted()
if __name__ == '__main__':
  fire.Fire(Mail)