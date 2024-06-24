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