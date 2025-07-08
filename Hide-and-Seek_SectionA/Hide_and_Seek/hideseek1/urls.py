from django.urls import path
from hideseek1 import views
from django.conf import settings
from django.conf.urls.static import static
from .views import encode, download

urlpatterns = [
    path('', views.Index,name='Index'),
    path('Signup/', views.handleSignup, name='handleSignup'),
    path('login', views.login_view, name='login_view'),
    path('regsuc/', views.regsuc, name='regsuc'),
    path('wruser/', views.wruser, name='wruser'),
    path('wremail/', views.wremail, name='wremail'),
    path('wrconpass/', views.wrconpass, name='wrconpass'),
    path('DIP/', views.DIP, name='DIP'),
    path('NIU/', views.NIU, name='NIU'),
    path('PCP/', views.PCP, name='PCP'),
    path('NPCP/', views.NPCP, name='NPCP'),
    path('NS/', views.NS, name='NS'),
    path('NEI/', views.NEI, name='NEI'),
    path('UEM/', views.UEM, name='UEM'),
    path('About/', views.About, name='About'),
    path('Gallery1/', views.Gallery1, name='Gallery1'),
    path('Gallery2/', views.Gallery2, name='Gallery2'),
    path('Home/', views.Home, name='Home'),
    path('encode', views.encode, name='encode'),
    path('download/<str:filename>/', download, name='download'),
    path('decode/', views.decode, name='decode'),
    path('loginunsuc/', views.loginunsuc, name='loginunsuc'),
    path('notsignup/', views.notsignup, name='notsignup'),
    path('Changepassword/', views.Changepassword, name='Changepassword'),
    path('incpass/', views.incpass, name='incpass'),
    path('samepass/', views.samepass, name='samepass'),
    path('successpass/', views.successpass, name='successpass'),
    path('wpass/', views.wpass, name='wpass'),
    path('validate-message/', views.message_validator_view, name='message-validator')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
