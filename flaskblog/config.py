import os
import json

with open('/etc/config.json') as config_file:
	config = json.load(config_file)

class Config:
	SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
	SECRET_KEY = config.get('FLASK_SECRET_KEY')
	RECAPTCHA_PUBLIC_KEY = config.get('RECAPTCHA_PUBLIC_KEY')
	RECAPTCHA_PRIVATE_KEY = config.get('RECAPTCHA_PRIVATE_KEY')
	#TESTING = True
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = config.get('EMAIL_USER')
	MAIL_PASSWORD = config.get('EMAIL_PASS')
	
