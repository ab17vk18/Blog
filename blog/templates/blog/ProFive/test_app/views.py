from django.shortcuts import render
from test_app.forms import UserForm, UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'test_app/index.html')

def register(request):

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Save userform to db
            user.set_password(user.password) # Hashing password
            user.save() #Update with hashed password

            profile = profile_form.save(commit=False)
            # Set one to one relationship bw profile and user
            profile.user = user

            # Check if profile picture is provided
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'test_app/registration.html',
                        {'user_form':user_form,
                        'profile_form':profile_form,
                        'registered':registered})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You're logged in")

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #django default authentication
        user = authenticate(username=username, password=password)

        # authentication success
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Inactive account. Contact the administrator")

        else:
            print("Login error. Username: {}, Password: {}".format(username,password))
            return HttpResponse("Username and/or password invalid")

    else:
        return render(request, 'test_app/login.html', {})
