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
                "all_events": User.objects.get(id=user_id).events.all(),
                "all_users": User.objects.all(),
                } 
                return render(request, "party_app/user_profile.html", context)
    return redirect("/user_profile/"+str(user_id))

def add_event(request):
    return render(request, "party_app/add_event.html")

def create_event(request):
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        errors = Event.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            # restful = Restful.objects.all()
            return redirect("/add_event")
        else:
            name = request.POST['new_name']
            description = request.POST['new_description']
            date = request.POST['new_date']
            location = request.POST['new_location']
            
            event = Event.objects.create(name=name, description=description, date = date, location=location)
            this_user = User.objects.get(id=request.session['id'])
            event.users.add(this_user)
        return redirect("/show_event/"+str(event.id))


def show_event(request, event_id):
    if request.method == "GET":
        this_user = User.objects.get(id=request.session['id'])
        friends = this_user.friends.all()
        event = Event.objects.get(id=event_id)
        guests = event.users.all()
        all_event = Event.objects.all()
        context = {
            "friends": friends,
            "event": event,
            "guests": guests,
            "all_messages": Post.objects.all(),
        }
        return render(request, "party_app/show_event.html", context)
    elif request.method == "POST":
        find_friend = User.objects.get(id=request.POST['friend_id'])
        find_event = Event.objects.get(id=event_id)
        find_event.users.add(find_friend)
        return redirect("/show_event/"+str(event_id))

def add_message(request):
    if request.method == "POST":
        posted = User.objects.get(first_name = request.session['first_name'], last_name=request.session['last_name'])
        event = Post.objects.create(message=request.POST['message'], posted_by=posted)
        return redirect("/show_event/"+str(event.id))

# def remove_friend(request):
#     remove = User.objects.get(id=event_id)
#     remove_event.delete()
#     user_id = request.session['id']
#     return redirect("/user_profile/"+str(user_id))

def find_friend(request):
    context = {
        'friends':User.objects.all()
    }
    return render(request, "party_app/find_friend.html", context)

def add_friend(request):
    this_user = User.objects.get(id=request.session['id'])
    if request.method == "POST":
        friends = this_user.friends.all()
        others = User.objects.all()
        main_list = [friend for friend in others if friend not in friends]
        context = {
            "friends": friends,
            "all_users": User.objects.all(),
            "guests": main_list,
        }
        return render(request, "party_app/find_friend.html", context)
    elif request.method == "POST":
        find_friend = User.objects.get(id=request.POST['friend_id'])
        this_user.friends.add(find_friend)
        return redirect("/find_friend")

def photo(request):
    return render(request, "party_app/photo.html")

def add_image(request):
    if request.method == "POST":
        this_user = User.objects.get(id=request.session['id'])
        this_user.image = request.POST["image"]
        this_user.save()
        print(this_user.image)
        return redirect("/photo")
    return redirect('/photo')

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