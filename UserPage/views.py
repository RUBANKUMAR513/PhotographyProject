# UserPage/views.py

from django.shortcuts import render

def user_profile_view(request):
    return render(request, 'UserPage.html')  

def User_login_view(request):
    return render(request,'Userlogin.html')