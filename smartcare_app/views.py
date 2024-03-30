import json
from telnetlib import LOGOUT
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Task, Prescription
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from smartcare_app_api import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from smartcare_app.models import Booking
from django.utils import timezone



def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        usertype = request.POST['usertype']
        
        if User. objects.filter(username=username).exists():
            messages.error(request, "Username already exists!! Please try another username.")
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!! Please try another email.")
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters!!")
            
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!!")
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers!!")
            return redirect('home')
        
       


        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_staff = "t"
        
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to SmartCare"
        message = "Hello " + myuser.first_name + "!!\n" + "Welcome to SmartCare.\n Thank you for visiting our website \n We have also sent you a confirmation email. Please confirm your email address to activate your account."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        #send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        
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
            return render(request, "authentication/index.html",{"fname":fname})
        
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sucessfully!!")
    return redirect('home')

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

#Function to create a users booking
@ csrf_protect
def booking(request):
    user_id = request.user.id
    if request.method == 'POST':
        Subject = request.POST['Subject']
        date = request.POST['date']                               
        time = request.POST['time']
        comment = request.POST['comment']
        doctor = request.POST['doctor']

        # Get the current date and time
        current_date = datetime.now()
        current_time = datetime.now().time()

        #Format the date and time
        formated_date = datetime.strptime(date, '%Y-%m-%d')
        formated_time = datetime.strptime(time, '%H:%M').time()                                 

        #making sure the booking isnt in the past
        if formated_date < current_date and formated_time <= current_time:
            messages.error(request, "the booking date is in the past")
            return redirect('booking')
        
        #It should be let through the form but checking to make sure its not null
        if Subject == None or date == None or time == None or comment == None:
            messages.error(request, "Not all data has been added")
            return redirect('booking')
        
        #Making sure that the doctor doesnt have a booking at this time

        #making sure the sure that the user is signed in
        if user_id is None:
            messages.error(request, "You Must login first to make a booking")
            return redirect('booking')


        #Making sure that the user doesnt already have a booking at that time
        if Booking.objects.filter(user=user_id, appointment_date=formated_date, appointment_time=formated_time).exists():
            messages.error(request, "You already have a booking at this time and date")
            return redirect('booking')


        #Send data to the Database
        booking = Booking(subject=Subject, appointment_date=formated_date, appointment_time=formated_time, comments=comment, doctor=doctor, user_id=user_id)
        booking.save()

        #Send data to the google calender api

        #Passin booking information to the template
        context = {
            'booking_subject': Subject,
            'booking_date': date,
            'booking_time': time,
            'booking_comment': comment,
            'booking_doctor': doctor,
        }
        #If no problems take user to success page
        return render(request, "authentication/bookingsuccess.html", context)
    #Load the html page when url is called
    return render(request, "authentication/booking.html")


def bookingSuccess(request):
    return render(request, "authentication/bookingsuccess.html")

#Function to cancel a users booking
def bookingCancel(request, ):
    user = request.user
    current_datetime = timezone.now()
    bookings = Booking.objects.filter(user=user, appointment_date__gte=current_datetime.date())
    return render(request, "authentication/bookingcancel.html", {'bookings': bookings})


    #Get the futures bookings of the current user
def bookingCancelMethod(request, date, time):
    user = request.user
    current_datetime = timezone.now()
    if request.method == 'POST':
        post_date = request.POST.get('date')
        post_time = request.POST.get('time')
        user_id = User.objects.get(username=user).id  
        print("date:" + str(post_date) + "Time:" + str(post_time))
        bookings = Booking.objects.filter(user=user_id, appointment_date=date, appointment_time=time)
        print(bookings)
        if bookings.exists():  
            booking = bookings.first()  
            # Delete the booking from the database
            booking.delete()
            # Retrieve updated bookings after deletion
            messages.error(request,"booking deleted")
            bookings = Booking.objects.filter(user=user, appointment_date__gte=current_datetime.date())
            return render(request, "authentication/bookingcancel.html", {'bookings': bookings})
        else:
            # Handle case where no matching booking is found 
            messages.error(request, "The booking you are trying to cancel does not exist.")
            bookings = Booking.objects.filter(user=user, appointment_date__gte=current_datetime.date())
            return render(request, "authentication/bookingcancel.html", {'bookings': bookings})
    
    #If it's a GET request, retrieve and render bookings
    bookings = Booking.objects.filter(user=user, appointment_date__gte=current_datetime.date())
    return render(request, "authentication/bookingcancel.html", {'bookings': bookings})
    
    
def BookingScheduelView(request):
    user = request.user
    if request.user.is_staff:

        #Get all of the bookings schedueled for today
        current_date = datetime.now().date()
    
        # Query bookings for the current day
        bookings = Booking.objects.filter(appointment_date=current_date)
    
        #Send todays bookings and its details to the view page
        return render(request, "authentication/bookingScheduel.html", {'bookings': bookings})
    else:
        messages.error(request, "You must be a member of staff to view this")
        return redirect('home')
    
def prescription(request):
    user = request.user
    if request.user.is_staff:
        if request.method == 'POST':
            post_fname = request.POST.get('fname')
            post_lname = request.POST.get('lname')
            post_email = request.POST.get('email')
            post_medicine = request.POST.get('medicine')
            post_dosage = request.POST.get('dosage')  # Corrected field name
            post_duration = request.POST.get('duration')  # Corrected field name

            patient_user = User.objects.filter(first_name=post_fname, last_name=post_lname, email=post_email).first()
            if patient_user is not None:
                prescription = Prescription.objects.create(
                    medicine=post_medicine,
                    dosage=post_dosage,
                    duration=post_duration,
                    user=patient_user
                )
                message = {'text': 'Prescription has been saved successfully!', 'type': 'success'}
            else:
                message = {'text': 'User not found or invalid user details.', 'type': 'error'}
        else:
            message = {'text': 'An error occurred. Please try again.', 'type': 'error'}
        
        context = {'message': message}
        return render(request, 'authentication/prescription.html', context)
    else:
        messages.error(request, "You must be a member of staff to view this")
        return redirect('home')

def displayprescription(request):
    user = request.user   
    user_id = request.user.id
    prescriptions = Prescription.objects.filter(user_id=user_id)
    return render(request, "authentication/displayprescription.html", {'prescriptions': prescriptions})






def addBookingToCalander(request):
    None
    
def removeBookingToCalander(request):
    None


