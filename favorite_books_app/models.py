from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        user = User.objects.filter(email=post_data['email'])

        # Check first name length
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters long"
        # Check last name length
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters long"
        # Check if email is in valid format
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not post_data['email']:
            errors['email'] = "Please enter an email address."
        elif not email_regex.match(post_data['email']):
            errors['email'] = "Email is not valid."
        # Email unique check
        elif user:
            errors['unique'] = "Email address already in use"
        # Check password length
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
            # Check if confirm password was entered
        elif not post_data['c_password']:
            errors['c_password'] = "You must confirm your password."
        # Check if passwords match
        elif post_data['password'] != post_data['c_password']:
            errors['mismatch'] = "Passwords do not match."


        return errors

    def login_validator(self, post_data):
        errors = {}

        user = User.objects.filter(email=post_data['email'])
        # Check if email was entered
        if len(post_data['email']) < 1:
            errors['email'] = "Please enter an email address."
        # Check if user exists
        elif not user:
            errors['email'] = "Email address has not been registered."
        else:
            # Check if password has been entered
            if len(post_data['password']) < 1:
                errors['password'] = "Password not entered."
            # Check credentials
            elif not bcrypt.checkpw(post_data['password'].encode(), user[0].password.encode()):
                errors['credentials'] = "Invalid credentials."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, post_data):
        errors = {}

        # Check if title is empty
        if len(post_data['title']) < 1:
            errors['title'] = "Title is empty."
        # Check description length
        if len(post_data['description']) < 5:
            errors['description'] = "Description must be at least 5 characters long."

        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ForeignKey(User, related_name="created_books", max_length=255, on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_books", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()