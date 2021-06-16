from django.db import models
import bcrypt
from datetime import datetime
from time import strptime
import re


INTAKE_METHODS = (
    ("OR", 'Oral'),
    ("INJ", 'Injection'),
    ("RE", 'Rectal'),
    ("PA", 'Patch'),
    ("GE", 'Gel'),
    ("IH", 'Inhaling'),
    ("OC", 'Ocular'),
)

class MedicationManager(models.Manager):
    def med_validator(self, post_data):
        errors = {}

        if len(post_data['doctor']) < 2:
            errors['doctor'] = "Must enter a provider name" 
        if len(post_data['name']) < 2:
            errors['name'] = "Must enter a medication name"
        if len(post_data['common_name']) < 2:
            errors['common_name'] = "Must enter a medication name"
        if len(post_data['dose']) < 2:
            errors['dose'] = "Must enter a dosage"
        if 'intake_method' not in post_data:
            errors['intake_method'] = "Must enter an intake method"
        if 'description' not in post_data:
            errors['description'] = "Must enter a description"
        elif len(post_data['description']) < 10:
            errors['description'] = "Description must be at least 10 characters"
        if len(post_data['frequency']) < 5:
            errors['frequency'] = "Must enter an intake frequency"
        if 'starting_count' not in post_data:
            errors['starting_count'] = "Must enter a dose count"
        if 'notes' not in post_data:
            errors['notes'] = "Must enter medication notes"
        elif len(post_data['notes']) < 8:
            errors['notes'] = "Notes must be at least 8 characters in length"
        return errors


class Medication(models.Model):
    doctor = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    common_name = models.CharField(max_length=30)
    dose = models.CharField(max_length=20)
    intake_method = models.CharField(max_length=2, choices=INTAKE_METHODS)
    description = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50)
    starting_count = models.IntegerField(null=True)
    end_date = models.CharField(max_length=25)
    notes = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MedicationManager()
    def __repr__(self):
        return f"User: {self.name} {self.common_name} {self.dose} {self.frequency}"


class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "INVALID CREDENTIALS!"
        else:
            errors['email'] = "INVALID CREDENTIALS!"
        return errors


    def registration_validator(self, post_data):
        SpecialSym = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

        errors = {}
        if 'first_name' not in post_data:
            errors['first_name'] = "Must enter a first name"
        elif len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be more than 2 characters."
        if 'last_name' not in post_data:
            errors['last_name'] = "Must enter a last name"
        elif len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be more than 2 characters."
        if 'preferred_name' not in post_data:
            errors['preferred_name'] = "Must enter a preferred name"    
        elif len(post_data['preferred_name']) < 2:
            errors['preferred_name'] = "Preferred name must be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid Email Address."
        else:
            user_list = User.objects.filter(email = post_data['email'])
            if len(user_list) > 0:
                errors['email'] = 'Email already exists.'

        if 'password' not in post_data:
            errors['password'] = 'Must enter a password'
        if len(post_data['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters long."
        if not any(char.isdigit() for char in (post_data['password'])):
            errors['password'] = "Passwords must contain at least 1 number"
        if len(post_data['password']) > 50:
            errors['password'] = "Passwords must be less than 50 characters"
        if not any(char.isupper() for char in (post_data['password'])):
            errors['password'] = "Passwords must have at least 1 uppercase letter"
        if not any(char.islower() for char in (post_data['password'])):
            errors['password'] = "Passwords must have at least 1 lowercase letter"
        if not any(char in SpecialSym for char in (post_data['password'])):
            errors['password'] = "Passwords must have at least 1 special character"


        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Password and Confirm Password must match."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    preferred_name = models.CharField(max_length=20)
    pronouns = models.CharField(max_length=25, blank=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


    def __repr__(self):
        return f"User: {self.first_name} {self.last_name} {self.preferred_name} {self.pronouns}"


    # TODO- add in clinics, specialties, contact info, notes, REPR commands
    # TODO- add allergies, info to track, birth date, next appointment tracker
    # TODO- pill counter button, reminder interface, user avatar, file uploads?
    # TODO- doctors get admin/elevated priveleges

class Rx(models.Model):
    patient = models.ForeignKey(User, related_name="my_prescriptions", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="rx_given", on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medication, related_name="rxs", on_delete=models.CASCADE)
    doseage = models.CharField(max_length=60)
    frequency = models.CharField(max_length=25)
    quantity = models.CharField(max_length=35)
    refills = models.IntegerField()
    date_filled = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)