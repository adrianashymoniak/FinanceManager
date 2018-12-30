from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from finance_manager.forms import SignUpForm
from finance_manager.models import Transaction


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.changed_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign-up.html', {'form': form})


@login_required(login_url='login/')
def home(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('operation_date')
    return render(request, 'home-page.html', {'transactions': transactions})
