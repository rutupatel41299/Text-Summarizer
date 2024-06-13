from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_request, name='login_request'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('logout_request', views.logout_request, name='logout_request'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('summarizer/', csrf_exempt(views.summarizer), name='summarizer'),
    path('summarizer1/', csrf_exempt(views.summarizer1), name='summarizer1'),
    path('feedback/', views.feedback, name='feedback'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('subscribe/', views.subscribe, name='subscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
