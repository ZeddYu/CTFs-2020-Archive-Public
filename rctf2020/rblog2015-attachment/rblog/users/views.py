from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


def registerView(req):
    # users funcs is only for admin(xss bot)
    return HttpResponse(status=503)

    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(req, 'users/sign_up.html', {'form': form})
