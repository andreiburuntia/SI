import RPi.GPIO as GPIO # pentru configurarea pinilor si folosirea GPIO
import time # pentru timere, wait, etc
import smtplib # pentru email
import bluetooth # pentru bluetooth checks

# initializare
sensor = 4
led = 17
redled = 21

# setarea pinilor
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(redled, GPIO.OUT, initial=GPIO.LOW)

# initializare email service
gmail_user = 'emailsters@gmail.com'  
gmail_password = 'parolastearsa' # am sters userul si parola

sent_from = gmail_user  
to = ['andreiburuntia@gmail.com']


# starile pentru state machine
previous_state = False
current_state = False

# lookup table pentru bluetooth, un dictionar
lookup = {'C0:EE:FB:47:53:DE': 'Andrei'}

# functie care clipeste un led
def blink(pin):  
		GPIO.output(pin,GPIO.HIGH)  
		time.sleep(1)  
		GPIO.output(pin,GPIO.LOW)  
		time.sleep(1)  
		return 

# functie care trimite email
def mail_it():
	try:  
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, "Breach detected! See motion stream or check local files")
		server.close()

		print 'Email sent!'
	except:  
		print 'Something went wrong sending email...'

# functie care verifica daca sunt prezent, folosind bluetooth signature
def im_here():
	print 'Checking ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
	for key, value in lookup.items():
		result = None
		result = bluetooth.lookup_name(key, timeout=3)
		if result != None:
			print value + ' is present'
			return True
		else:
			continue
	return False

# intr-o bucla infinita, se interogheaza pinul la care s-a conectat senzorul PIR
while True:
	time.sleep(0.1)
	previous_state = current_state # tranzitie state machine
	current_state = GPIO.input(sensor) # noua stare, dupa outputul senzorului
	if im_here(): # daca cineva trusted e prezent, se incheie bucla
		break
	if current_state != previous_state:
		new_state = "HIGH" if current_state else "LOW"
		print "GPIO pin %s is %s" % (sensor, new_state)
		if new_state=="HIGH": # daca s-a detectat miscare
			mail_it()
			GPIO.output(redled,GPIO.HIGH)
			time.sleep(1)
			blink(led)

# 'cleanup' sau unbind pentru pinii GPIO
GPIO.cleanup()