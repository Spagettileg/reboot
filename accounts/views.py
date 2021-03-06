from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm
import sweetify


def register(request):
    """
    Render the registration page
    """
    if request.user.is_authenticated:
        sweetify.info(request, "You are already logged in",
                         button='Ok', timer=3000)
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                sweetify.success(request,
                                 "You have successfully registered")
                return redirect(reverse('index'))
            else:
                sweetify.info(request,
                              "Unable to register your account at this time!",
                              button='Ok', timer=3000)
    else:
        # Create an instance of reg form
        registration_form = UserRegistrationForm()

    return render(request, 'registration.html', {
        "registration_form": registration_form})
    """
    registration_form passed through as a context dictionary.
    """


def login(request):
    """
    Return a Login page
    """
    if request.user.is_authenticated:
        sweetify.info(request, "You are already logged in!",
                         button='OK', timer=3000)
        return redirect(reverse('index'))

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                sweetify.success(request,
                                 "You have successfully logged in!")

                if request.GET.get('next', False):
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return redirect(reverse('index'))
            else:
                login_form.add_error(None,
                                     "Your username or password is incorrect!")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})


@login_required
def logout(request):
    """
    Log the user out
    """
    auth.logout(request)
    sweetify.success(request, "You have successfully been logged out!")

    return redirect(reverse('index'))


@login_required()
def profile(request):
    """
    User profile page. Filter () used to return multiple records and help
    avoid an error message is using get () instead. The latter method is
    limited to getting one result only.
    """
    user = User.objects.filter(email=request.user.email)

    context = {
        'profile': user,
    }

    return render(request, 'profile.html', context)
