# UserPage/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from website.models import CompanyInfo
from django.contrib.auth import logout

@login_required  # Ensures that only logged-in users can access this view
def user_profile_view(request):
    company_info = CompanyInfo.objects.first()
   
    # print(company_info)  # Check if the company info is being fetched
    # print(sliders)       # Check if sliders are being fetched
    
    context = {
        'company_info': company_info,
       
    }
    # You can pass additional context to the template if needed
    return render(request, 'UserPage.html',context)  # Ensure this matches your template name


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
            # messages.success(request, 'Login successful! Welcome to Vickyneo Photography.')
            return redirect('UserPage:user_profile')  # Redirect to the user profile page

        messages.error(request, 'Invalid username or password.')  # Add error message

    return render(request, 'Userlogin.html')  # Render the login template for GET requests


def user_logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, 'You have been logged out successfully.')  # Optional success message
    return redirect('UserPage:user_login')  # Redirect to the login page