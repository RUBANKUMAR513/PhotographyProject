from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

class CustomAdminLoginView(LoginView):
    template_name = 'admin/Adminlogin.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        otp = request.POST.get('otp')

        if form.is_valid():
            user = form.get_user()

            # Check if OTP is provided
            if not otp:
                messages.error(request, 'OTP is required.')
            else:
                # OTP validation logic (replace with real OTP logic)
                if otp == "1234":  # Example OTP for demonstration
                    login(request, user)
                    return redirect('admin:index')
                else:
                    messages.error(request, 'Invalid OTP.')
        else:
            messages.error(request, 'Invalid username or password.')

        # Render the login form with error messages on failure
        return render(request, self.template_name, {'form': form})