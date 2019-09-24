from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "party_app/login.html")

def login(request):
    errors={}
    if request.method == "POST":
        other_user = User.objects.filter(email = request.POST['email'])
        try:
            this_user = other_user[0]
            print(this_user)
            if request.POST['password'] == this_user.password:
                request.session['username'] = this_user.username
                request.session['first_name'] = this_user.first_name
                request.session['email'] = this_user.email
                request.session['id'] = this_user.id
                request.session['last_name'] = this_user.last_name
                return redirect("/user_profile/"+str(this_user.id))
            errors["password_error"] = "You forgot your password. Please try again!"
        except:
            errors['email_error']= "No user exists here, go ahead and register"
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
        return redirect("/")


def register_page(request):
    return render(request, "party_app/register.html")

def user_profile(request, user_id):
    return render(request, "party_app/user_profile.html")

def add_event(request):
    return render(request, "party_app/add_event.html")

def show_event(request):
    return render(request, "party_app/show_event.html")

def find_friend(request):
    return render(request, "party_app/find_friend.html")

def photo(request):
    return render(request, "party_app/photo.html")

def meet_team(request):
    return render(request, "party_app/meet_team.html")