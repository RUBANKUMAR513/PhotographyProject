from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import OTPModel  # Adjust the import based on your project structure
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from EmailConfiguration.msg import process  # Adjust the import based on your project structure

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import OTPModel  # Make sure to import your OTPModel

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import OTPModel  # Make sure to import your OTP model


class CustomAdminLoginView(LoginView):
    template_name = 'admin/Adminlogin.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        otp = request.POST.get('otp')  
       
        if form.is_valid():
            user = form.get_user()

            
            if not otp:
                messages.error(request, 'OTP is required.')
                return self._render_login_form(request, form)

           
            return self._verify_otp(request, otp, user)
        else:
            messages.error(request, 'Invalid username or password.')
        
        return self._render_login_form(request, form)

    def _verify_otp(self, request, otp, user):
        try:
            otp_instance = OTPModel.objects.get(otp=otp)  
            
            if otp_instance.is_expired(): 
                messages.error(request, 'OTP has expired. Please request a new OTP.')
            else:
               
                login(request, user)
                return redirect('admin:index')

        except OTPModel.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please check and try again.')

        return self._render_login_form(request, None)

    def _render_login_form(self, request, form):
        return render(request, self.template_name, {'form': form})

# class CustomAdminLoginView(LoginView):
#     template_name = 'admin/Adminlogin.html'
#     form_class = AuthenticationForm

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request, data=request.POST)
#         otp = request.POST.get('otp')

#         if form.is_valid():
#             user = form.get_user()

#             # Check if OTP is provided
#             if not otp:
#                 messages.error(request, 'OTP is required.')
#             else:
#                 # OTP validation logic (replace with real OTP logic)
#                 if otp == "1234":  # Example OTP for demonstration
#                     login(request, user)
#                     return redirect('admin:index')
#                 else:
#                     messages.error(request, 'Invalid OTP.')
#         else:
#             messages.error(request, 'Invalid username or password.')

      
#         return render(request, self.template_name, {'form': form})
    

@csrf_exempt  # Use this only if CSRF protection is not needed (not recommended for production)
def send_otp(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            message = data.get('message', '')

            # Check for the specific message to trigger the OTP process
            if message == 'admin trigger otp':
                process()  # Call your process function to send the OTP
                return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})

            return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)



