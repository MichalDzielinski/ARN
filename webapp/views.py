from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages

def home(request):

    context = {}
    return render(request, 'webapp/index.html', context)

#Register
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request,'Account created successfully!')
            return redirect('my-login')
    
    context = {'form': form}

    return render(request, 'webapp/register.html',context)

#login
def my_login(request):

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                
                messages.success(request,'You have logged in!')


                return redirect('dashboard')

    context = {'form': form}

    return render(request, 'webapp/my-login.html', context)

#logout
def user_logout(request):
    auth.logout(request)
    messages.success(request,'You had been logged-out successfully!')

    return redirect('my-login')

@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'my_records': my_records}
    return render(request, 'webapp/dashboard.html', context)

#create a record
@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'A record had been created!')

            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'webapp/create-record.html', context)

#
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request,'Your record has been updated!')

            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context)

@login_required(login_url='my-login')
def singular_record(request, pk):
    
    all_records = Record.objects.get(id=pk)
    context ={'record': all_records}

    return render(request, 'webapp/view-record.html', context )
        
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request,'The record had been deleted!')

    return redirect('dashboard')