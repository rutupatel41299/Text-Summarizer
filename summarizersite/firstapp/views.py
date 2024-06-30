from django.shortcuts import render, redirect
from .models import Registration, Login, DocumentInfo, SummaryInfo, Feedback
import datetime
from .module import main, handle_uploaded_file
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from summarizersite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
import PyPDF2

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

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


def subscribe(request):
    print(1)
    if request.method == 'GET':
        print(2)
        email_id = request.GET.get('email_id')
        print(email_id)
        subject = 'subscription mail'
        message = 'welcome there!'
        try:
            send_mail(subject, message, EMAIL_HOST_USER, [email_id], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        print(3)
        return HttpResponseRedirect('index')

    else:
        print(4)
        return render(request, 'feedback.html')


def summarizer(request):
    if request.method == 'POST':
        print(request.method)
        threshold = int(request.POST['threshold'])
        pdffile = request.FILES['getFile']
        pdfname = pdffile.name

        # using pypdf
        pdfReader = PyPDF2.PdfFileReader(pdffile)
        pages = pdfReader.numPages
        userinput = ''
        for p in range(pages):
            pageObj = pdfReader.getPage(p)
            userinput = userinput + pageObj.extractText()
        print("data which read by pypdf2:------", userinput)

        # using pdfminer
        # output_string = StringIO()
        # parser = PDFParser(pdffile)
        # doc = PDFDocument(parser)
        # rsrcmgr = PDFResourceManager()
        # device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        # interpreter = PDFPageInterpreter(rsrcmgr, device)
        # for page in PDFPage.create_pages(doc):
        #     interpreter.process_page(page)
        # userinput = output_string.getvalue()

        current_time = datetime.datetime.now()
        document_title = current_time.strftime("%d-%m-%Y_%H-%M-%S")
        document_path = 'C:/Users/rutup/PycharmProjects/final_summarizer_project/summarizersite/files/user_documents/'

        try:
            fh = open(document_path+document_title+'.txt', 'w')
            fh.write(userinput)
        except:
            fh = open(document_path + document_title + '.txt', 'wb')
            fh.write(userinput.encode('utf8'))

        fh.close()
        summary, doc_length = main(userinput, threshold)
        print(summary)
        summary_title = document_title+'_summary'
        summary_path = 'C:/Users/rutup/PycharmProjects/final_summarizer_project/summarizersite/files/generated_summaries/'
        try:
            percentage = (len(summary)/doc_length)*100
        except:
            percentage = None
        print(percentage)

        try:
            fhs = open(summary_path + summary_title + '.txt', 'w')
            for s in summary:
                fhs.write(s)
                fhs.write('\n')
        except:
            fhs = open(summary_path + summary_title + '.txt', 'wb')
            for s in summary:
                fhs.write(s.encode('utf8'))
                fhs.write(b"\n")
        docobj = DocumentInfo(document_title=document_title, document_path=document_path, document_type='text', document_size=doc_length)
        summaryobj = SummaryInfo(summary_title=summary_title, summary_path=summary_path, summary_type='text', summary_size=len(summary), Percentage=percentage)
        s = ' '.join(summary)

        try:
            docobj.save()
            summaryobj.save()
            return render(request, 'summarizer.html', {'summary': s})
        except:
            return render(request, 'summarizer.html')
    else:
        print(request.method)
        try:
            if request.session['email_id']:
                return render(request, 'summarizer.html')
        except:
            return redirect('login_request')


def summarizer1(request):
    if request.method == 'POST':
        print(request.method)
        threshold = int(request.GET['threshold'])
        if request.GET['directinput']:
            directinput = request.GET['directinput']
        else:
            directinput = request.GET['pdfdata']

        print("data which read by javascript:------", directinput)
        userinput = directinput

        current_time = datetime.datetime.now()
        document_title = current_time.strftime("%d-%m-%Y_%H-%M-%S")
        document_path = 'C:/Users/rutup/PycharmProjects/final_summarizer_project/summarizersite/files/user_documents/'

        try:
            fh = open(document_path+document_title+'.txt', 'w')
            fh.write(userinput)
        except:
            fh = open(document_path + document_title + '.txt', 'wb')
            fh.write(userinput.encode('utf8'))

        fh.close()
        summary, doc_length = main(userinput, threshold)
        print(summary)
        summary_title = document_title+'_summary'
        summary_path = 'C:/Users/rutup/PycharmProjects/final_summarizer_project/summarizersite/files/generated_summaries/'
        try:
            percentage = (len(summary)/doc_length)*100
        except:
            percentage = None
        print(percentage)

        try:
            fhs = open(summary_path+summary_title+'.txt', 'w')
            for s in summary:
                fhs.write(s)
                fhs.write('\n')
        except:
            fhs = open(summary_path + summary_title + '.txt', 'wb')
            for s in summary:
                fhs.write(s.encode('utf8'))
                fhs.write(b"\n")
        docobj = DocumentInfo(document_title=document_title, document_path=document_path, document_type='text', document_size=doc_length)
        summaryobj = SummaryInfo(summary_title=summary_title, summary_path=summary_path, summary_type='text', summary_size=len(summary), Percentage=percentage)

        try:
            docobj.save()
            summaryobj.save()
            return HttpResponse(summary)
        except:
            return render(request, 'summarizer.html')
    else:
        print(request.method)
        try:
            if request.session['email_id']:
                return render(request, 'summarizer.html')
        except:
            return redirect('login_request')