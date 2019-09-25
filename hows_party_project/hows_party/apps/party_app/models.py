from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        for existing_user in User.objects.all():
            if existing_user.email == postData['email']:
                errors["email_exists"] = "We already have a user with this email"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern          
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 3:
            errors["password"] = "Password should be at least 3 characters"
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"]= "Password does not match"
        return errors

class EventManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['new_name']) < 2:
            errors["new_name"] = "Show name should be at least 2 characters"
        if len(postData['new_description']) < 1:
            errors["new_description"] = "Description should be at least 1 character"
        if len(postData['new_location']) < 1:
            errors["new_name"] = "Needs a location!"
        return errors

class User(models.Model):
    objects = UserManager()
    friends = models.ManyToManyField('self', related_name="users")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return f"<User Object: {self.first_name} {self.last_name}, email: {self.email} password: {self.password} username: {self.username}>"

class Event(models.Model):
    objects = EventManager()
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    users = models.ManyToManyField(User, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return f"<User Object: {self.name} {self.location} {self.description} {self.date}>"


class Post(models.Model):
    message = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="users_post", null=True, blank=True)
    event_post = models.ForeignKey(Event, related_name="posts", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return f"<User Object: {self.message}>"






