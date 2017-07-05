from __future__ import unicode_literals
from django.contrib import messages
import re
import datetime
import os, binascii
import md5
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z_-]*$')

# Create your models here.
class UserManager(models.Manager):
      def login(self, postData, sessionData, request):
            error = False
            email = postData['email']
            password = postData['psw']
            try:
                  user = User.objects.get(email=email)
                  encrypted_password = bcrypt.hashpw(str(password).encode(), str(user.salt).encode())
                  if user.password == encrypted_password:
                        sessionData['logged_in'] = email
                        print sessionData['logged_in']
                        error = False
                  else:
                        messages.error(request, 'Invalid Password!')
                        error = True
                        sessionData['logged_in'] = False
            except:
                  messages.error(request, 'Invalid Email Address!')
                  error = True 
                  sessionData['logged_in'] = False 
            if error:
                  return False
            else: 
                  return True
          
      # for now i am passing in the entire request object for the sake of the django messages, and i am using session to repopulate the fields
      def register(self, postData, sessionData, request):
            error = False
            sessionData['first_name'] = postData['first_name']
            sessionData['last_name'] = postData['last_name']
            sessionData['email'] = postData['email'] 
            password = postData['psw']
            password_rpt = postData['psw-repeat']
            if len(sessionData['email']) < 1:
                  messages.error(request, 'Email cannot be blank!')
                  error = True
            if len(password) < 9:
                  messages.error(request, 'Password must be at least 8 charachters!')
                  error = True
            if password != password_rpt:
                  messages.error(request, 'Password does not match!')        
                  error = True
            if len(sessionData['first_name']) < 2:
                  messages.error(request, 'Name must have at least 2 letters!') 
                  error = True
            if len(sessionData['last_name']) < 2:
                  messages.error(request, 'Name must have at least 2 letters!')  
                  error = True
            if not NAME_REGEX.match(sessionData['first_name']):
                  messages.error(request, 'Only letters please!')
                  error = True
            if not NAME_REGEX.match(sessionData['last_name']):
                  messages.error(request, 'Only letters please!')
                  error = True
            if not EMAIL_REGEX.match(sessionData['email']):
                  messages.error(request, 'Invalid Email Address!')
                  error = True
            else:
                  if User.objects.filter(email=sessionData['email']).exists():
                        email_exists =  True
                        error = True
                        messages.error(request, 'Email address not available, choose a different one, or click login to go to login') 
                  else:
                        email_exists = False
                        messages.success(request, 'Success!')
                        error = False
                        salt =  bcrypt.gensalt()
                        hashed_pw = bcrypt.hashpw(str(password).encode(), str(salt).encode())
                        User.objects.create(first_name = sessionData['first_name'], last_name= sessionData['last_name'], email = sessionData['email'],  password=hashed_pw, salt = salt)
                        sessionData['logged_in'] = sessionData['email']
                        sessionData.pop('first_name')
                        sessionData.pop('last_name')
                        sessionData.pop('email')
            if error:
                  return False
            else: 
                  return True

class User(models.Model):
      first_name = models.CharField(max_length=45)
      last_name = models.CharField(max_length=45)
      email = models.CharField(max_length=100)
      password = models.CharField(max_length=100)
      salt = models.CharField(max_length=100)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()
      def __str__(self):
        return self.first_name + " " + self.last_name

class Message(models.Model):
      user = models.ForeignKey(User)
      message = models.TextField()
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
      user = models.ForeignKey(User)
      message = models.ForeignKey(Message)
      comment = models.TextField()
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)