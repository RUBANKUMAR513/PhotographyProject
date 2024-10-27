# UserPage/views.py

from django.shortcuts import render

def user_profile_view(request):
    return render(request, 'UserPage.html')  





# UserPage/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def User_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                messages.error(request, 'Admin users are not allowed to log in here.')
                return render(request, 'Userlogin.html')  # Render the login template again

            login(request, user)
            messages.success(request, 'Login successful! Welcome to Vickyneo Photography.')  # Success message
            return redirect('/userpage/')  # Redirect to the user page
        else:
            messages.error(request, 'Invalid username or password.')  # Add error message

    return render(request, 'Userlogin.html')  # Ensure this matches your template name
