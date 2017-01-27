from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
# from .models import Email
# Create your views here.

def index(request):
    context = {
    'new_user': User.objects.all()
    }
    return render(request, 'LoginAndReg/index.html', context)

def register(request):
    if request.method == 'POST':
        print 'in process method'
        print request.POST

        response = User.objects.validate_new_user(request.POST)

        if response[0] == False:
            for error in response[1]:
                messages.error(request, error)
                print 'response[0] was False'
                print error
            return redirect('/')
        else:
            print '9'*50
            print 'got to the "else"'
            print response[1]
            # try:
            #     request.session['first_name'] = response[1].first_name
            # except MultiValueDictKeyError:
            #     pass
            return redirect('/success')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        response = User.objects.validate_login(request.POST)
        if response[0] == False:
            for error in response[1]:
                messages.error(request, error)
            return redirect('/')
        else:
            return redirect('/success')

    return redirect('/')





def success(request):
        print "*"*50
        return render(request, 'LoginAndReg/success.html')


def logout(request):
    return redirect('/')
