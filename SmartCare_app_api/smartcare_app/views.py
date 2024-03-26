import json
from telnetlib import LOGOUT
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import Task
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from smartcare_app_api import settings
from django.core.mail import send_mail



def Home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User. objects.filter(username=username).exists():
            messages.error(request, "Username already exists!! Please try another username.")
            return redirect('Home')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!! Please try another email.")
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters!!")
            
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!!")
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers!!")
            return redirect('Home')
        
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to SmartCare"
        message = "Hello " + myuser.first_name + "!!\n" + "Welcome to SmartCare.\n Thank you for visiting our website \n We have also sent you a confirmation email. Please confirm your email address to activate your account."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('Home')
    
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sucessfully!!")
    return redirect('Home')

def Contact(request):
    return render(request, "contact.html")

def About(request):
    return render(request, "about.html")

    
def tasks(request):
    """
    Return a JSON response with all tasks
    """
    # Query all tasks
    tasks_queryset = Task.objects.all()
    # Serialize the queryset to JSON
    tasks_json = serializers.serialize("json", tasks_queryset, fields=(
        "title", "description", "completed", "created_at"))
    return HttpResponse(tasks_json, content_type="application/json")


@ csrf_protect
@ csrf_exempt
def create_task(request):
    """
    Create a new task and returns a JSON response with the new task
    """
    # Get the title from the POST request
    title = request.POST["title"]
    # Get the description from the POST request
    description = request.POST["description"]
    # Create a new task
    task = Task(title=title, description=description)
    # Save the task to the database
    task.save()
    # Return a JSON response with the new task
    return JsonResponse({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
    })


@ csrf_protect
@ csrf_exempt
def update_task(request, pk):
    """
    Update a task and returns a JSON response with the updated task
    """
    task = Task.objects.get(pk=pk)
    if request.POST.get("title"):
        task.title = request.POST["title"]
    if request.POST.get("description"):
        task.description = request.POST["description"]
    if request.POST.get("completed"):
        task.completed = json.loads(request.POST["completed"].lower())
    task.save()
    return JsonResponse({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
    })


def delete_task(request, pk):
    """
    Delete a task and returns a JSON response with the status
    """
    task = Task.objects.get(pk=pk)
    task.delete()
    return JsonResponse({"status": "Successfully deleted task."})
