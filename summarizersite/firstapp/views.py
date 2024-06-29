from django.shortcuts import render, redirect
from .models import Registration, Login, DocumentInfo, SummaryInfo, Feedback
import datetime
from .module import main, handle_uploaded_file
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from summarizersite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError

def index(request):
    try:
        if request.session['email_id']:
            return render(request, 'index.html')
    except:
        return redirect('login_request')

def register(request):
    if request.method == 'POST':
        email_id = request.POST['email_id']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birth_date = request.POST['birth_date']
        contact_no = request.POST['contact_no']
        occupation = request.POST['occupation']
        country = request.POST['country']
        regobj = Registration(first_name=first_name, last_name=last_name, occupation=occupation, email_id=email_id, contact_no=contact_no, birth_date=birth_date, country=country)
        loginobj = Login(email_id=email_id, password=password, active_inactive=True)

        try:
            regobj.save()
            loginobj.save()
            return redirect('login_request')
        except:
            return render(request, 'auth-multi-step-sign-up.html')
    else:
        return render(request, 'auth-multi-step-sign-up.html')
    
def login_request(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        print(email_id, password)
        users = Login.objects.all()
        for user in users:
            print(user.email_id, user.password)
            if user.email_id == email_id and user.password == password:
                print(user.email_id, user.password)
                userobj = Registration.objects.get(email_id=email_id)
                user_session = dict()
                user_session['first_name'] = userobj.first_name
                user_session['last_name'] = userobj.last_name
                user_session['email_id'] = userobj.email_id
                request.session['fname'] = user_session['first_name']
                request.session['lname'] = user_session['last_name']
                request.session['email_id'] = user_session['email_id']
                return redirect('index')
        return render(request, 'auth-multi-step-sign-in.html')

    else:
        try:
            if request.session['email_id']:
                return redirect('index')
        except:
            return render(request, 'auth-multi-step-sign-in.html')

def forgotpassword(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        subject = "Your old password for summarizer"
        userobj = Login.objects.get(email_id=email_id)
        message = userobj.password
        send_mail(subject, message, EMAIL_HOST_USER, [email_id], fail_silently=False)
        return redirect('login_request')
    else:
        return render(request, 'forgotpassword.html')
    
def logout_request(request):
    try:
        del request.session['fname']
        del request.session['lname']
        del request.session['email_id']
    except:
        return redirect('index')

    return redirect('login_request')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        message = email + ' ' + message
        recepient = 'learn.code.630@gmail.com'
        print(name, email, subject, message)
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
        return render(request, 'contact.html')
    else:
        try:
            if request.session['email_id']:
                return render(request, 'contact.html')
        except:
            return redirect('login_request')

def about(request):
    try:
        if request.session['email_id']:
            return render(request, 'about.html')
    except:
        return redirect('login_request')

def feedback(request):
    print(11)
    if request.method == 'POST':
        email_id = request.session['email_id']
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')
        print(rating, email_id)
        print(12)
        feedbackobj = Feedback(email_id=email_id, rating=rating, comments=comments)
        try:
            feedbackobj.save()
            return render(request, 'feedback.html', {'feedback': 'Thanks For Your Precious Feedback!'})
        except:
            return render(request, 'feedback.html')
    else:
        try:
            if request.session['email_id']:
                return render(request, 'feedback.html')
        except:
            return redirect('login_request')