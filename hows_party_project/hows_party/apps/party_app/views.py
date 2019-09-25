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

def reg(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/register_page") 
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['confirm_password']
            new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
            messages.success(request, "User successfully registered")
            request.session['first_name']=new_user.first_name
            request.session['last_name']=new_user.last_name
            request.session['id']=new_user.id
            request.session['email']=new_user.email
            return redirect("/user_profile/"+str(new_user.id))

def user_profile(request, user_id):
    if "first_name" in request.session:
        if "last_name" in request.session:
            if "username" in request.session:
                context = {
                "all_events": Event.objects.all(),
                "all_users": User.objects.all(),
                } 
                return render(request, "party_app/user_profile.html", context)
    return redirect("/user_profile/"+str(user_id))

def add_event(request):
    return render(request, "party_app/add_event.html")


def show_event(request, event_id):
    if "first_name" in request.session:
        event_id = Event.objects.get(id=event_id)
        all_event = Event.objects.all()

        context = {
            "event": event_id,
            "all_user": User.objects.all(),

        }
        return render(request, "party_app/show_event.html", context)
    return redirect("/user_profile/"+str(user_id))


def find_friend(request):
    return render(request, "party_app/find_friend.html")

def photo(request):
    return render(request, "party_app/photo.html")

def meet_team(request):
    return render(request, "party_app/meet_team.html")

def logout(request):
    request.session.clear()
    return redirect("/") 

def remove(request, event_id):
    remove_event = Event.objects.get(id=event_id)
    remove_event.delete()
    user_id = request.session['id']
    return redirect("/user_profile/"+str(user_id))

def autocompleteModel(request, event_id):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Event.objects.filter(name=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)