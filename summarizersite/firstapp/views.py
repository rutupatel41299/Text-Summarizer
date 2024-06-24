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