from django.shortcuts import render
from register.form import RegisterForm
from django.shortcuts import redirect
from flight_log import constant
from django.contrib import messages

# Create your views here.
def register(request):
    if request.session.get('usname', False):
        return redirect('/')
    else:
        form = RegisterForm()
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if (form.is_valid()):
                form.save()
#                 username = request.POST[constant.employee_number]
#                 request.session[constant.usernameParam] = username
                messages.success(request, 'Your account is created successfully.')
                #return redirect('/')
    
        return render(request, "accounts/register.html", {"form":form})