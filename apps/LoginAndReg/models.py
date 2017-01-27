from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import re, bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z\-]+$')
EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
# Create your models here.
class UserManager(models.Manager):
    def validate_new_user(self, data):
        print data
        print "8"*50
        errors = []
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        confirm_pw = data['confirm_pw']

        if len(first_name) < 2:
            errors.append('first name must be at least two characters!')
        elif not NAME_REGEX.match(first_name):
            errors.append('First name may not contain any special characters or numbers!')

        if len(last_name) < 2:
            errors.append('last name must be at least two characters!')
        elif not NAME_REGEX.match(last_name):
            errors.append('Last name may not contain any special characters or numbers!')

        if len(email) < 1:
            errors.append('email field must be filled out')
        elif not re.match(EMAIL_REGEX, email):
            errors.append('email must be valid')

        if len(password) < 8:
            errors.append('Your Password must contain 8 or more characters!')

        if password != confirm_pw:
            errors.append('Confirm Password and Password must match!')

        if errors:
            print "*"*50
            print errors
            print "*"*50
            return [False, errors]
        else:
            hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            try:
                user = self.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
            except NameError:
                pass
            return [True, user]

    def validate_login(self, data):
        errors = []
        print 'Filtering for email'
        if User.objects.filter(email=data['email']):
            hashed = User.objects.get(email=data['email']).password
            hashed = hashed.encode('utf-8')
            print hashed
            password = data['password']
            password = password.encode('utf-8')
            print password
            if bcrypt.hashpw(password, hashed) == hashed:
                return (True, password)
        else:
            print 'got to else statement on validate_login'
            errors.append('Bad Email and/or Password, Please try again')
            return (False, errors)




class User(models.Model):
      first_name = models.CharField(max_length=200)
      last_name = models.CharField(max_length=200)
      email = models.EmailField()
      password = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      objects = UserManager()
